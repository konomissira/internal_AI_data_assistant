-- 04_roles.sql
-- Create read-only role for query execution (simulated governance)

DROP ROLE IF EXISTS readonly_user;

CREATE ROLE readonly_user
LOGIN PASSWORD 'readonly_password';

GRANT CONNECT ON DATABASE analytics TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;

GRANT SELECT ON dim_date, dim_region, dim_product, fact_sales TO readonly_user;
GRANT SELECT ON semantic_metrics, semantic_dimensions, semantic_joins TO readonly_user;
