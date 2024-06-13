SELECT 										
	LOWER(routine_name) AS object_name,
  ddl AS ddl_content,
  CURRENT_TIMESTAMP() as generated_at
FROM  `[PROJECT].[DATASET].INFORMATION_SCHEMA.ROUTINES` 
WHERE specific_catalog = '[PROJECT]'
AND specific_schema  = '[DATASET]'
AND routine_type = 'TABLE FUNCTION'
