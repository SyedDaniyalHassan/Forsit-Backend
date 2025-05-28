-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_name (name)
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    sku VARCHAR(50) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    category_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    INDEX idx_product_name (name),
    INDEX idx_product_sku (sku),
    INDEX idx_product_price (price),
    INDEX idx_product_category (category_id)
);

-- Create inventory table
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    quantity INT DEFAULT 0,
    low_stock_threshold INT DEFAULT 10,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_inventory_product (product_id),
    INDEX idx_inventory_quantity (quantity)
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount FLOAT NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'completed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sales_date (sale_date),
    INDEX idx_sales_amount (total_amount),
    INDEX idx_sales_status (status)
);

-- Create sales_details table
CREATE TABLE IF NOT EXISTS sales_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_sales_detail_sale (sale_id),
    INDEX idx_sales_detail_product (product_id)
);

-- Insert sample data

-- Insert categories
INSERT INTO categories (name, description, created_at, updated_at) VALUES
('Electronics', 'Electronic devices and accessories', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Clothing', 'Fashion and apparel items', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Books', 'Books and publications', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Home & Kitchen', 'Home appliances and kitchen items', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert products
INSERT INTO products (name, description, sku, price, category_id, created_at, updated_at) VALUES
('iPhone 13', 'Latest Apple smartphone with advanced features', 'IPH13-001', 999.99, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Samsung Galaxy S21', 'High-end Android smartphone', 'SAMS21-001', 899.99, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Men\'s T-Shirt', 'Cotton casual t-shirt', 'TS-M-001', 29.99, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Women\'s Jeans', 'Classic blue denim jeans', 'JN-W-001', 49.99, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Python Programming', 'Learn Python programming language', 'BK-PY-001', 39.99, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Data Science Basics', 'Introduction to data science', 'BK-DS-001', 45.99, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Coffee Maker', 'Automatic drip coffee maker', 'HM-CM-001', 79.99, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Blender', 'High-speed kitchen blender', 'HM-BL-001', 59.99, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert inventory
INSERT INTO inventory (product_id, quantity, low_stock_threshold, last_updated) VALUES
(1, 50, 10, CURRENT_TIMESTAMP),  -- iPhone 13
(2, 30, 5, CURRENT_TIMESTAMP),   -- Samsung Galaxy S21
(3, 100, 20, CURRENT_TIMESTAMP), -- Men's T-Shirt
(4, 75, 15, CURRENT_TIMESTAMP),  -- Women's Jeans
(5, 25, 5, CURRENT_TIMESTAMP),   -- Python Programming
(6, 20, 5, CURRENT_TIMESTAMP),   -- Data Science Basics
(7, 15, 3, CURRENT_TIMESTAMP),   -- Coffee Maker
(8, 8, 5, CURRENT_TIMESTAMP);    -- Blender (low stock)

-- Insert sample sales
INSERT INTO sales (sale_date, total_amount, status, created_at, updated_at) VALUES
('2025-05-01 10:00:00', 1029.98, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('2025-05-02 14:30:00', 79.98, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('2025-05-03 11:15:00', 85.98, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert sales details
INSERT INTO sales_details (sale_id, product_id, quantity, unit_price, total_price, created_at) VALUES
(1, 1, 1, 999.99, 999.99, CURRENT_TIMESTAMP),  -- iPhone 13
(1, 3, 1, 29.99, 29.99, CURRENT_TIMESTAMP),    -- Men's T-Shirt
(2, 3, 2, 29.99, 59.98, CURRENT_TIMESTAMP),    -- Two Men's T-Shirts
(2, 4, 1, 19.99, 19.99, CURRENT_TIMESTAMP),    -- Women's Jeans
(3, 5, 1, 39.99, 39.99, CURRENT_TIMESTAMP),    -- Python Programming
(3, 6, 1, 45.99, 45.99, CURRENT_TIMESTAMP);    -- Data Science Basics 