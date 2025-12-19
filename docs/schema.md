# Database schema summary

This document summarizes the main models and relationships used in the project.

## Accounts

- `User` (extends `AbstractUser`)
  - `is_vendor`: Boolean
  - `is_customer`: Boolean

- `VendorProfile`
  - `user`: OneToOne -> `User`
  - `shop_name`, `phone`

- `CustomerProfile`
  - `user`: OneToOne -> `User`
  - `address`, `phone`

## Products

- `Category`
  - `name`, `description`, `image`
  - has many `Product`

- `Product`
  - `vendor`: FK -> `VendorProfile`
  - `category`: FK -> `Category` (SET_NULL)
  - `name`, `description`, `price`, `stock`, `image`, `is_active`
  - has many `ProductImage`
  - has many `Review`

- `ProductImage`
  - `product`: FK -> `Product`
  - `image`

- `Review`
  - `product`: FK -> `Product`
  - `user`: FK -> `User`
  - `rating`, `comment` (unique per `product`+`user`)

## Orders & Cart

- `Cart`
  - `user`: OneToOne -> `User`
  - has many `CartItem`

- `CartItem`
  - `cart`: FK -> `Cart`
  - `product`: FK -> `Product`
  - `quantity`

- `Order`
  - `user`: FK -> `User`
  - `order_number`, `status`, `total_amount`, `shipping_address`
  - has many `OrderItem`

- `OrderItem`
  - `order`: FK -> `Order`
  - `product`: FK -> `Product` (SET_NULL)
  - `vendor`: FK -> `VendorProfile` (SET_NULL)
  - `quantity`, `price`

## Notes

- Migrations for each app are present under each app's `migrations/` folder — include them when you push the repo. For a visual ER diagram, add `django-extensions` and Graphviz and run `python manage.py graph_models -a -o docs/ER_diagram.png`.
