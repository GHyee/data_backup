-- Create the customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255)
);

-- Insert 100 mock data records
INSERT INTO customers (customer_name)
SELECT 'Customer ' || g || '-' || s
FROM generate_series(1, 10) AS g,
     generate_series(1, 10) AS s;
