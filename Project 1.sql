-----------------------#1_Project_Title = "Order Data Analysis"--------------------------------

---setting up PRIMARY_KEY----------------------------------------------------------------------

--ALTER TABLE product
--DD CONSTRAINT pk_product_order_id 
--PRIMARY KEY (order_id);

---setting up FORIGN_KEY-----------------------------------------------------------------------

--ALTER TABLE shipment
--ADD CONSTRAINT fk_shipment_order_id
--FOREIGN KEY (order_id)
--REFERENCES product (order_id);

---1.Find top 10 highest revenue generating products---

SELECT 
	product_id,sale_price 
FROM 
	product
ORDER BY 
	sale_price DESC
LIMIT 10;

---2.Find the top 5 cities with the highest profit margins---

SELECT 
	s.city,
	sum(p.profit) as total_profit
FROM 
    product p
JOIN 
    shipment s 
ON 
    p.order_id = s.order_id
GROUP BY 
    s.city
ORDER BY 
    total_profit DESC
LIMIT 5;

---3.Calculate the total discount given for each category---

SELECT 
	category,
	SUM(discount) as total_discount
FROM 
	PRODUCT
GROUP BY 
	category
ORDER BY
	total_discount DESC;
	
---4.Find the average sale price per product category---

SELECT 
	category,
	AVG(sale_price) as average_sale_price
FROM 
	PRODUCT
GROUP BY 
	category
ORDER BY
	average_sale_price;
	
---5.Find the region with the highest average sale price---

SELECT 
	s.region
FROM 
    product p
JOIN 
    shipment s 
ON 
    p.order_id = s.order_id
GROUP BY 
    s.region
ORDER BY 
    AVG(p.sale_price) DESC
LIMIT 1;

---6.Find the total profit per category---

SELECT 
	category,
	SUM(profit) as total_profit
from 
	product p
JOIN 
	shipment s 
ON 
	p.order_id = s.order_id
GROUP BY 
	p.category
ORDER BY 
	total_profit DESC;
	
---7.Identify the top 3 segments with the highest quantity of orders---

SELECT 
	segment,
	sum(quantity) as no_of_quantity
FROM 
	shipment s
JOIN 
	PRODUCT p
ON 
	p.order_id = s.order_id
GROUP BY
	segment
ORDER BY
	no_of_quantity desc
LIMIT 3;

---8.Determine the average discount percentage given per region---

SELECT
	region,
	AVG(discount_percent) as avg_discount
FROM 
	product p
JOIN 
	shipment s
ON 
	p.order_id = s.order_id
GROUP BY 
	region
ORDER BY 
	avg_discount DESC;
	
---9.Find the product category with the highest total profit---

SELECT 
	category,
	sum(profit) as total_profit
FROM 
	product p 
JOIN 
	shipment s
ON
	p.order_id = s.order_id
GROUP BY 
	category
ORDER BY 
	total_profit DESC
limit 1;

---10.Calculate the total revenue generated per year---

SELECT 
    EXTRACT(YEAR FROM order_date::DATE) AS year,
    SUM(sale_price) AS total_revenue
FROM 
    product p
JOIN 
    shipment s
ON 
    p.order_id = s.order_id
GROUP BY 
    year
ORDER BY 
    total_revenue DESC;
-----------------------------------------------------------------------------------------
---10 MORE ADDITIONAL REQUIREMENTS:---
-----------------------------------------------------------------------------------------
---11.Top-Selling Products---

SELECT 
	product_id,
	category,
	sum(sale_price) as total_revenue
FROM
	product p
JOIN
	shipment s
ON
	p.order_id = s.order_id
GROUP BY
	product_id,category
ORDER BY
	total_revenue DESC
LIMIT 5;

---12. Year-Over-Year Monthly Sales Comparison---

SELECT
	EXTRACT(YEAR FROM order_date::DATE) AS year_,
	EXTRACT(MONTH FROM order_date::DATE) AS month_,
	SUM(sale_price) as total_sales
from
	product p
join
	shipment s
on
	p.order_id = s.order_id
group by 
	year_,
	month_
order by 
	year_ ASC,
	month_ ASC,
	total_sales asc;
	
---13.	Best Performing Products by Revenue---

SELECT 
	ROW_NUMBER() OVER (ORDER BY SUM(sale_price) DESC) as p_rank,
	product_id,
	sum(sale_price) as total_revenue
FROM
	product p
JOIN
	shipment s
ON
	p.order_id = s.order_id
GROUP BY
	product_id
ORDER BY
	p_rank,
	total_revenue DESC;
	
---14.	Region-Wise Performance
--Determine which region generates the highest total sales revenue and profit.
SELECT
	region,
	sum(sale_price) as total_sales,
	sum(profit) as total_profit
FROM
	product p
JOIN
	shipment s
ON
	p.order_id = s.order_id
GROUP BY
	region
ORDER BY
	total_sales DESC,
	total_profit DESC
LIMIT 1;
---15. Analyze the Impact of Order Quantity on Total Sales and Profit(TOP 10 qty)---

SELECT 
    p.product_id,
    SUM(quantity) AS total_quantity,
    SUM(sale_price) AS total_sales,
    SUM(profit) AS total_profit
FROM
    product p
JOIN
    shipment s
ON
    p.order_id = s.order_id
GROUP BY
    product_id
ORDER BY
    total_quantity DESC
LIMIT 10;

---16.Category Performance, evaluate the profit margin for each category.
SELECT 
	category,
	sum(sale_price) as total_sales,
	sum(profit) as total_profit,
	(sum(profit)  / sum(sale_price)) * 100 as profit_margin
FROM
	product p
JOIN
	shipment s
ON
	p.order_id = s.order_id
GROUP BY
	category
HAVING
	(sum(profit)  / sum(sale_price)) * 100 >1
ORDER BY
	total_profit DESC;
	
---17.Monthly Regional Sales Analysis--
SELECT 
	EXTRACT(MONTH FROM order_date::DATE) 
	AS month,
	s.region,
	SUM(p.sale_price) AS total_sales
FROM 
	product p
JOIN 
	shipment s 
ON 
	p.order_id = s.order_id
GROUP BY
	month, s.region
ORDER BY 
	month, total_sales DESC;
	
---18.Monthly Sales by Region---
SELECT CASE 
			WHEN discount_percent > 0 
			THEN 'discounted' ELSE 'Non-Discounted'
            END AS sale_type, 
            SUM(sale_price) AS total_revenue
FROM product
GROUP BY sale_type;
	
---19.Show Products with Sales more than 50,000 Revenue Along with Regions---
SELECT 
    p.product_id,
    s.region,
    SUM(p.sale_price) AS total_sales
FROM 
    product p
RIGHT JOIN 
    shipment s
ON 
    p.order_id = s.order_id
GROUP BY 
    p.product_id,region
HAVING
	SUM(p.sale_price) >50000
ORDER BY 
    total_sales DESC;

--(Tried Complex query) 20. Identify the Best-Selling Products in Each Region---

WITH RegionSales AS (
    SELECT 
        s.region,
        p.product_id,
        SUM(p.sale_price) AS total_sales
    FROM 
        shipment s
    JOIN 
        product p
    ON 
        p.order_id = s.order_id
    GROUP BY 
        s.region, p.product_id
)
SELECT region, product_id, total_sales,
    CASE 
        WHEN total_sales >= 100000 THEN 'Top Performer'
        WHEN total_sales >= 50000 THEN 'Mid Performer'
        ELSE 'Low Performer'
    END AS performance_category
FROM (
    SELECT region, product_id, total_sales,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY total_sales DESC) AS rank
    FROM RegionSales
) AS ranked_sales
WHERE rank <= 3
ORDER BY region, rank;


-------------------------------------------------THE_END---------------------------------------------------
--Please eveluate me with below parameters out of 10
--1.project goals ----------------   /10
--2.Query Organization -----------   /10
--3.Way of defined variables -----   /10
--4.Overall ----------------------   /10
