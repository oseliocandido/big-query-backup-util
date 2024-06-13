#  Big Query Backup Util

`The Big Query Backup Util` is a solution to create backup of Big Query Objects DDL of Views and Table Functions. Pulls the contents of CSV files exported from BQ, creating backup files in appropriate directories without overwriting.

## Prerequisites

- 🐳 Docker

## How to Use

1. **Clone the Repository 🔄**
   ```bash
   git clone https://github.com/oseliocandido/big-query-backup-util.git && cd big-query-backup-util
    ```
2.  **Get CSV Files 📄**

    Place CSV files containing DDL statements in the `Input/Views` and `Input/Table_Functions` directories accordingly.

3. **Start the Container ▶️**

    Run the container with your backup timestamp, overwriting the `BACKUP_DATE` environment variable.

   ```bash
    docker-compose run -e BACKUP_DATE=[YOUR_TIMESTAMP_HERE] gcp-backup-ddls
    ```

4.  **Confirm Operation ✅** 
    
    It will prompt for confirmation. Type `y` to proceed.

5. **Output 📂**

    Navigate to the `Output` directory where the backup files are saved.

## Notes
- In the [aux/](aux/) folder, there are the scripts to generate the CSV to be used. Replace the placeholders for actual Big Query `PROJECT` and `DATASET`.
