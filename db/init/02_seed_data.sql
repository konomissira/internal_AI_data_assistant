-- 02_seed_data.sql
-- Seed dimensions

INSERT INTO dim_region
    (region_id, region_name)
VALUES
    (1, 'London'),
    (2, 'Manchester'),
    (3, 'Birmingham')
ON CONFLICT DO NOTHING;

INSERT INTO dim_product
    (product_id, product_name, product_category)
VALUES
    (1, 'Espresso', 'Coffee'),
    (2, 'Latte', 'Coffee'),
    (3, 'Croissant', 'Bakery'),
    (4, 'Muffin', 'Bakery')
ON CONFLICT DO NOTHING;

-- Seed dates (10 days)
INSERT INTO dim_date
    (date_id, date_value, year, month, day, week)
VALUES
    (20250101, '2025-01-01', 2025, 1, 1, 1),
    (20250102, '2025-01-02', 2025, 1, 2, 1),
    (20250103, '2025-01-03', 2025, 1, 3, 1),
    (20250104, '2025-01-04', 2025, 1, 4, 1),
    (20250105, '2025-01-05', 2025, 1, 5, 1),
    (20250106, '2025-01-06', 2025, 1, 6, 2),
    (20250107, '2025-01-07', 2025, 1, 7, 2),
    (20250108, '2025-01-08', 2025, 1, 8, 2),
    (20250109, '2025-01-09', 2025, 1, 9, 2),
    (20250110, '2025-01-10', 2025, 1, 10, 2)
ON CONFLICT DO NOTHING;

-- Seed facts (simple but varied)
INSERT INTO fact_sales
    (date_id, region_id, product_id, order_id, quantity, unit_price, total_amount)
VALUES
    (20250101, 1, 1, 'ORD-001', 2, 2.50, 5.00),
    (20250101, 1, 3, 'ORD-001', 1, 3.20, 3.20),
    (20250102, 1, 2, 'ORD-002', 1, 3.50, 3.50),
    (20250102, 2, 1, 'ORD-003', 3, 2.50, 7.50),
    (20250103, 2, 4, 'ORD-004', 2, 2.80, 5.60),
    (20250104, 3, 2, 'ORD-005', 2, 3.50, 7.00),
    (20250105, 3, 1, 'ORD-006', 1, 2.50, 2.50),
    (20250106, 1, 4, 'ORD-007', 4, 2.80, 11.20),
    (20250107, 2, 3, 'ORD-008', 2, 3.20, 6.40),
    (20250108, 1, 2, 'ORD-009', 3, 3.50, 10.50),
    (20250109, 3, 3, 'ORD-010', 1, 3.20, 3.20),
    (20250110, 2, 1, 'ORD-011', 2, 2.50, 5.00)
ON CONFLICT DO NOTHING;
