DROP DATABASE IF EXISTS Day4;
CREATE SCHEMA Day4;

USE Day4;

CREATE TABLE customers (
	customer_id INT PRIMARY KEY auto_increment,
    customer_name VARCHAR(50)
    );
    
CREATE TABLE products(
	product_id INT PRIMARY KEY auto_increment,
    product_name VARCHAR(50),
    product_price DECIMAL(5,2),
    product_stock INT
    );

ALTER TABLE products
	auto_increment = 100;

CREATE TABLE orders(
	order_id INT PRIMARY KEY auto_increment,
    customer_id INT,
    product_id INT,
    ordered_quantity INT,
    total_amount DECIMAL(10,2),
    
    CONSTRAINT fk_customer_id
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_product_id
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    
-- initial dummy dataset
INSERT INTO customers(customer_name) VALUES ('Emily'), ('Linda'), ('Thomas'), ('Laura'), ('Matthew'), ('Ava'), ('Mia'), ('David'), ('Olivia');
SELECT * FROM customers;

INSERT INTO products (product_name, product_price, product_stock) VALUES
('Laptop', 999.99, 25),
('Smartphone', 699.50, 50),
('Headphones', 49.99, 200),
('Smartwatch', 199.95, 75),
('Tablet', 299.00, 40),
('Bluetooth Speaker', 89.99, 120),
('Monitor', 179.99, 60),
('Keyboard', 29.99, 150),
('Mouse', 19.99, 175),
('External Hard Drive', 79.99, 90),
('Gaming Console', 399.95, 30),
('Camera', 549.99, 15),
('Printer', 129.99, 50);
SELECT * FROM products;

SELECT * FROM orders;

DELIMITER $$
CREATE TRIGGER update_total_amount
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
	DECLARE product_price DECIMAL (10,2);

	SELECT p.product_price INTO product_price
	FROM products p WHERE p.product_id = NEW.product_id;

	SET NEW.total_amount = product_price*NEW.ordered_quantity;
END $$
DELIMITER ;

SELECT * FROM products;

INSERT INTO orders(customer_id, product_id, ordered_quantity) VALUES(10, 100, 3);

SELECT * FROM orders;

DELIMITER $$
CREATE TRIGGER adjust_product_stock
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    DECLARE quantity_difference INT;

    -- Calculate the difference in ordered quantity
    SET quantity_difference = NEW.ordered_quantity - OLD.ordered_quantity;

    -- Update the product_stock in the products table based on the quantity change
    UPDATE products
    SET product_stock = product_stock - quantity_difference
    WHERE product_id = NEW.product_id;
END $$
DELIMITER ;


UPDATE orders
SET ordered_quantity = 20
WHERE order_id = 1;

SELECT * FROM orders;

SELECT * FROM products;

SELECT *
FROM customers
WHERE customer_name = 'John';

INSERT INTO customers (customer_name)
VALUES ('John');

SELECT * FROM customers;

INSERT INTO orders (customer_id, ordered_quantity, total_amount)
VALUES ((SELECT customer_id FROM customers WHERE customer_name = 'John'), 1, 1.34);

SELECT order_id, customer_id, ordered_quantity, total_amount
FROM orders;


DELIMITER $$
CREATE PROCEDURE get_customers()
BEGIN
	SELECT * FROM customers;
END $$
DELIMITER ;

CALL get_customers();


DELIMITER $$
CREATE PROCEDURE InsertOrder( IN P_customer_name VARCHAR(50), IN P_price DECIMAL(5, 2))
BEGIN
DECLARE _customer_id INT; -- Declare variable to hold customer ID
-- Step 1: Check if the customer exists
SELECT customer_id INTO v_customer_id
FRoM customers
WHERE customer_name = P_customer_name;
-- Step 2: If the customer doesn't exist, insert a new record into the customers table
IF v_customer_id IS NULL THEN
INSERT INTO customers (customer_name) VALUES (P_customer_name);
-- Retrieve the new customer ID after insertion
SELECT LAST_INSERT_ID() INTO v_customer_id;
END IF;
-- Step 3: Insert the new order into the orders table
INSERT INTO orders (customer_id, price)
VALUES (V_customer_id, P_price);
END $$
DELIMITER ;