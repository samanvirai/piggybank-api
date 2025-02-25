# Flask GraphQL Server

This is a Flask-based backend application with a PostgreSQL database, utilizing GraphQL for API interactions. The application includes services for user authentication and gift management.

## Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv (optional but recommended)

## Setup Instructions

### 1. Clone the Repository

bash
git clone <repository-url>
cd <repository-directory>


### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

bash
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies

bash
pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file in the root directory and set the following environment variables:

```plaintext
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
JWT_SECRET=your-secret-key-here
```

Replace `<username>`, `<password>`, and `<database_name>` with your PostgreSQL credentials and database name.

### 5. Initialize the Database

Run the following script to create the necessary database tables:

bash
python -c "from models import init_db; init_db()"

### 6. Start the Flask Server

Run the Flask application:

bash
flask run

The server will start on `http://localhost:5000` by default.

## Accessing the GraphQL Endpoint

Once the server is running, you can access the GraphQL interface at:

```
http://localhost:5000/graphql
```

### Example GraphQL Queries and Mutations

- **Sign Up a User**

```graphql
mutation {
  signUp(firstName: "John", lastName: "Doe", phoneNumber: "1234567890", email: "john.doe@example.com", password: "password123") {
    user {
      id
      email
    }
  }
}
```

- **Login a User**

```graphql
mutation {
  login(email: "john.doe@example.com", password: "password123") {
    token
  }
}
```

- **Send a Gift**

```graphql
mutation {
  sendGift(senderId: 1, receiverId: 2, giftDetails: "{amount: 100}") {
    success
  }
}
```

- **List Gifts for a User**

```graphql
query {
  listGiftsForUser(token: "your_jwt_token_here") {
    id
    amount
  }
}
```

## Notes

- Ensure your PostgreSQL server is running and accessible with the credentials provided in your `.env` file.
- The JWT secret key should be kept secure and not exposed publicly.
- The application is set up to run in development mode. For production, consider using a production-ready server like Gunicorn and configuring environment variables appropriately.
