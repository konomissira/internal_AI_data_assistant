-- 03_semantic_layer.sql
-- Semantic layer tables (governed metrics, dimensions, joins)

CREATE TABLE
IF NOT EXISTS semantic_metrics
(
  metric_name       TEXT PRIMARY KEY,
  description       TEXT NOT NULL,
  sql_expression    TEXT NOT NULL,
  default_table     TEXT NOT NULL
);

CREATE TABLE
IF NOT EXISTS semantic_dimensions
(
  dimension_name    TEXT PRIMARY KEY,
  description       TEXT NOT NULL,
  table_name        TEXT NOT NULL,
  column_name       TEXT NOT NULL,
  data_type         TEXT NOT NULL
);

CREATE TABLE
IF NOT EXISTS semantic_joins
(
  join_name         TEXT PRIMARY KEY,
  left_table        TEXT NOT NULL,
  right_table       TEXT NOT NULL,
  join_condition    TEXT NOT NULL
);

-- Metrics
INSERT INTO semantic_metrics
  (metric_name, description, sql_expression, default_table)
VALUES
  ('total_sales', 'Total revenue (sum of total_amount)', 'SUM(f.total_amount)', 'fact_sales f'),
  ('total_orders', 'Number of distinct orders', 'COUNT(DISTINCT f.order_id)', 'fact_sales f'),
  ('avg_order_value', 'Average order value', 'AVG(f.total_amount)', 'fact_sales f'),
  ('total_quantity', 'Total quantity sold', 'SUM(f.quantity)', 'fact_sales f')
ON CONFLICT DO NOTHING;

-- Dimensions
INSERT INTO semantic_dimensions
  (dimension_name, description, table_name, column_name, data_type)
VALUES
  ('date', 'Order date', 'dim_date d', 'date_value', 'date'),
  ('year', 'Year', 'dim_date d', 'year', 'int'),
  ('month', 'Month', 'dim_date d', 'month', 'int'),
  ('region', 'Region name', 'dim_region r', 'region_name', 'text'),
  ('product', 'Product name', 'dim_product p', 'product_name', 'text'),
  ('category', 'Product category', 'dim_product p', 'product_category', 'text')
ON CONFLICT DO NOTHING;

-- Joins (fact -> dims)
INSERT INTO semantic_joins
  (join_name, left_table, right_table, join_condition)
VALUES
  ('fact_to_date', 'fact_sales f', 'dim_date d', 'f.date_id = d.date_id'),
  ('fact_to_region', 'fact_sales f', 'dim_region r', 'f.region_id = r.region_id'),
  ('fact_to_product', 'fact_sales f', 'dim_product p', 'f.product_id = p.product_id')
ON CONFLICT DO NOTHING;
