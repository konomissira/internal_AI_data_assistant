-- 01_schema.sql
-- Core star schema for analytics

CREATE TABLE
IF NOT EXISTS dim_date
(
  date_id      INTEGER PRIMARY KEY,
  date_value   DATE NOT NULL,
  year         INTEGER NOT NULL,
  month        INTEGER NOT NULL,
  day          INTEGER NOT NULL,
  week         INTEGER NOT NULL
);

CREATE TABLE
IF NOT EXISTS dim_region
(
  region_id    INTEGER PRIMARY KEY,
  region_name  TEXT NOT NULL
);

CREATE TABLE
IF NOT EXISTS dim_product
(
  product_id       INTEGER PRIMARY KEY,
  product_name     TEXT NOT NULL,
  product_category TEXT NOT NULL
);

CREATE TABLE
IF NOT EXISTS fact_sales
(
  sale_id      BIGSERIAL PRIMARY KEY,
  date_id      INTEGER NOT NULL REFERENCES dim_date
(date_id),
  region_id    INTEGER NOT NULL REFERENCES dim_region
(region_id),
  product_id   INTEGER NOT NULL REFERENCES dim_product
(product_id),
  order_id     TEXT NOT NULL,
  quantity     INTEGER NOT NULL CHECK
(quantity >= 0),
  unit_price   NUMERIC
(12,2) NOT NULL CHECK
(unit_price >= 0),
  total_amount NUMERIC
(12,2) NOT NULL CHECK
(total_amount >= 0)
);

-- Helpful indexes
CREATE INDEX
IF NOT EXISTS idx_fact_sales_date ON fact_sales
(date_id);
CREATE INDEX
IF NOT EXISTS idx_fact_sales_region ON fact_sales
(region_id);
CREATE INDEX
IF NOT EXISTS idx_fact_sales_product ON fact_sales
(product_id);
