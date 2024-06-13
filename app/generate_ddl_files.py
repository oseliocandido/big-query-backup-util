from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
import os
import sys

# Constants for directories
BASE_INPUT_DIR = Path("/app/Input")
VIEWS_DIR = BASE_INPUT_DIR / "Views"
TABLE_FUNCTIONS_DIR = BASE_INPUT_DIR / "Table_Functions"
BASE_OUTPUT_DIR = Path("/app/Output")


class DDLProcessor(ABC):
    def __init__(self, directory: Path, backup_date: str):
        self.directory = directory
        self.backup_date = backup_date
        self.output_dir = BASE_OUTPUT_DIR / directory.name / backup_date

    def process_csv_files(self):
        for csv_file in self.directory.glob("*.csv"):
            print(f"Processing file: {csv_file}")
            df = pd.read_csv(filepath_or_buffer=csv_file)
            self.output_dir.mkdir(parents=True, exist_ok=True)
            for index, row in df.iterrows():
                self.process_type(row)

    @abstractmethod
    def process_type(self, row: pd.Series) -> None:
        pass


class ViewProcessor(DDLProcessor):
    def process_type(self, row: pd.Series) -> None:
        view_name = f"vf-pt-datahub.vfpt_dh_lake_processed_dhmgmt_olap_s.{row['object_name']}"
        first_line = f"CREATE OR REPLACE VIEW `{view_name}` AS\n"
        with open(self.output_dir / f"{row['object_name']}.sql", "w") as file:
            file.write(first_line)
            file.write(row['ddl_content'])


class RoutineProcessor(DDLProcessor):
    def process_type(self, row: pd.Series) -> None:
        with open(self.output_dir / f"{row['object_name']}.sql", "w") as file:
            file.write(row['ddl_content'])


class BackupManager:
    def __init__(self, backup_date: str):
        self.backup_date = backup_date
        self.processors = []

    def add_processor(self, processor):
        self.processors.append(processor)

    def backup_exists(self):
        return any((BASE_OUTPUT_DIR / directory.name / self.backup_date).exists() for directory in [VIEWS_DIR, TABLE_FUNCTIONS_DIR])

    def confirm_operation(self):
        return input("Do you want to proceed with the operation? (y/n): ").strip().lower() == 'y'

    def process_folders(self):
        for processor in self.processors:
            print(f"\nProcessing {processor.__class__.__name__}...")
            processor.process_csv_files()
        print(f"Backup process completed successfully!")


if __name__ == "__main__":
    backup_date = os.getenv('BACKUP_DATE')
    manager = BackupManager(backup_date)

    manager.add_processor(ViewProcessor(VIEWS_DIR, backup_date))
    manager.add_processor(RoutineProcessor(TABLE_FUNCTIONS_DIR, backup_date))

    if manager.backup_exists():
        print("Backup for the given date already exists. Operation aborted.")
        sys.exit(1)

    if not manager.confirm_operation():
        print("Operation aborted by user.")
        sys.exit(1)

    manager.process_folders()
