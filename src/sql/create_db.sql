CREATE TABLE `Category` (
  `category_id` INTEGER PRIMARY KEY,
  `category_name` VARCHAR(256)
);

CREATE TABLE `Fabricator` (
  `fabricator_id` INTEGER PRIMARY KEY,
  `fabricator_name` VARCHAR(256)
);

CREATE TABLE `Order` (
  `order_id` INTEGER PRIMARY KEY,
  `order_address` VARCHAR(256),
  `order_date` DATE
);

CREATE TABLE `Product` (
  `product_id` INTEGER PRIMARY KEY,
  `category_id` INTEGER,
  `fabricator_id` INTEGER,
  `product_name` VARCHAR(256),
  FOREIGN KEY (`category_id`) REFERENCES `Category` (`category_id`),
  FOREIGN KEY (`fabricator_id`) REFERENCES `Fabricator` (`fabricator_id`)
);

CREATE TABLE `Journal` (
  `journal_id` INTEGER PRIMARY KEY,
  `order_id` INTEGER,
  `product_id` INTEGER,
  `quantity` INTEGER,
  FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`),
  FOREIGN KEY (`order_id`) REFERENCES `Order` (`order_id`)
);
