SELECT
   LOWER(table_name) AS object_name,
   view_definition AS ddl_content,
   CURRENT_TIMESTAMP() as generated_at
FROM  `[PROJECT].[DATASET].INFORMATION_SCHEMA.VIEWS` 
WHERE table_catalog = '[PROJECT]'
AND table_schema  = '[DATASET]'
