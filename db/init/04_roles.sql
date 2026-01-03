-- 04_roles.sql
-- Create read-only role for query execution (simulated governance)

DO $
$
BEGIN
    IF NOT EXISTS (SELECT 1
    FROM pg_roles
    WHERE rolname = 'readonly_user') THEN
    CREATE ROLE readonly_user
    LOGIN PASSWORD 'readonly_password';
END
IF;
END $$;

GRANT CONNECT ON DATABASE analytics TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;

-- Grant SELECT on tables
GRANT SELECT ON dim_date, dim_region, dim_product, fact_sales TO readonly_user;
GRANT SELECT ON semantic_metrics, semantic_dimensions, semantic_joins TO readonly_user;
