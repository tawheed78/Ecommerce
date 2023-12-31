E-Commerce Application 
This is a Backend system for Ecommerce Website, built using FastAPI, MongoDB, Redis, AWS SQS

I have developed a robust backend system for an Ecommerce application using FastAPI. Leveraging MongoDB, I've ensured efficient storage and retrieval of data. To enhance performance, I've seamlessly integrated Redis for data caching. Furthermore, I've integrated AWS SQS in the the order placement process, enabling real-time message reception on AWS servers whenever a customer places an order.

Installation
Clone this repository to your local machine using git clone https://github.com/tawheed78/Ecommerce.git
Navigate to the cloned directory.
Install the required packages by running pip install -r requirements.txt.
Create a .env file in the root directory and add your environment variables or remove the os command and put your own secret key and save while working on it locally.
Start the development server using uvicorn main:app --reload

Endpoints
POST /add-user/ - Add a new user
GET /user/{id}/ - Get user details
PUT /update-user/{id}/ - Update user details
POST /add-to-cart/ - Add product to user cart
GET /user-cart-details/{id}/ - Get cart items of user
DELETE /delete-user-cart/ - Delete products from cart
POST /create-product/ - Create a new product
GET /products/ - Get all products
GET /product-detail/{id}/ - Get product details
PUT /update-product/{id}/ - Update product details
DELETE /delete-product/{id}/ - Delete a product
POST /place-order/ - Place order
GET /orders/{id}/ - Get previous orders of user

Environment Variables
To run this project, you will need to set the following environment variables:

HOST - Redis Host
PORT - Redis Port
PASSWORD - Redis Password
MONGO_URI = MongoDB connection string
ACCESS_KEY - AWS SQS Access Key
SECRET_ACCESS_KEY - AWS SQS Secret Access Key
AWS_REGION = AWS Region
QUEUE_URL - AWS SQS Queue URL
 
 
