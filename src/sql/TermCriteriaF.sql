SELECT *
FROM 'Journal'
JOIN 'Order' ON 'Journal'.'order_id' = 'Order'.'order_id'
JOIN 'Product' ON 'Journal'.'product_id' = 'Product'.'product_id'
JOIN 'Category'ON 'Product'.'category_id' = 'Category'.'category_id'
JOIN 'Fabricator' ON 'Product'.'fabricator_id' = 'Fabricator'.'fabricator_id';
WHERE 'Orders'.'orders_id' LIKE '%{}%' AND 'Product'.'product_name' LIKE '%{}%' 
AND 'journal'.'quantity' LIKE '%{}%' AND 'Fabricator'.'fabricator_name' LIKE '%{}%'
AND 'Category'.'category_name' LIKE '%{}%'