### ⚠️ -- still in development -- ⚠️
# 🌱PSYNO - Social Media API for Mental Health Support

Welcome to **PSYNO**, a RESTful API designed to power a social media platform focused on mental health and emotional well-being. This project aims to create a safe space where users can share their thoughts, connect with others, and support each other through their mental health journeys. Built with Python, FastAPI, SQLModel, and JWT authentication, PSYNO provides a secure and scalable backend for managing user posts.

## 🛠️Features

- **User Authentication**: Secure login and registration using JWT (JSON Web Tokens) with password hashing (bcrypt) for user privacy.
- **Post Management**: Create, read, update, and delete posts with user-specific access control.
  - Any authenticated user can view all posts.
  - Only the post owner can create, edit, or delete their own posts.
- **Mental Health Focus**: Designed as a foundation for a social media platform where users can express and share their mental health experiences.
- **RESTful API**: Easy-to-use endpoints with FastAPI for efficient communication.
- **Database Integration**: SQLite database with SQLModel for storing users and posts.

## 💻Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (via SQLModel)
- **Authentication**: JWT with `python-jose` and `passlib[bcrypt]`
- **Dependencies**: `uvicorn`, `sqlmodel`, `pydantic`

## ⚙️Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/3hsan1njast/psyno.git
   cd psyno
   ```

2. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn sqlmodel pydantic python-jose[cryptography] passlib[bcrypt]
   ```

3. **Run the Application**
   - Ensure the `database.db` file is either absent (it will be created automatically) or deleted to start fresh.
   - Start the server:
     ```bash
     python main.py
     ```
   - The API will be available at `http://localhost:8000`.

4. **Secure the Secret Key**
   - Open `auth.py` and replace the default `SECRET_KEY` ("your-secret-key-1234567890abcdef") with a secure key:
     ```bash
     openssl rand -hex 32
     ```
   - Paste the generated key into `SECRET_KEY`.

## 🕸️API Endpoints

### Authentication
- **Register**: `POST /register`
  - Body: `{"username": "string", "hashed_password": "string"}`
  - Response: `{"message": "User created successfully"}`
- **Login**: `POST /login`
  - Body: `{"username": "string", "password": "string"}`
  - Response: `{"access_token": "string", "token_type": "bearer"}`

### Posts
- **Get All Posts**: `GET /posts`
  - Response: List of all posts.
- **Get Post by ID**: `GET /posts/{post_id}`
  - Response: Single post.
- **Create Post**: `POST /posts`
  - Headers: `Authorization: Bearer <token>`
  - Body: `{"body": "string"}`
  - Response: Created post object.
- **Update Post**: `PUT /posts/{post_id}`
  - Headers: `Authorization: Bearer <token>`
  - Body: `{"body": "string"}` (only owner can update).
  - Response: Updated post object.
- **Delete Post**: `DELETE /posts/{post_id}`
  - Headers: `Authorization: Bearer <token>`
  - Response: Deleted post object (only owner can delete).

## 👤Usage
1. Register a new user via `/register`.
2. Login with `/login` to get a token.
3. Use the token in the `Authorization` header (e.g., `Bearer <token>`) for protected endpoints like `/posts`.
4. Test the API with tools like Postman or cURL.

## 🫂Contributing
Feel free to fork this repository, submit issues, or send pull requests. Suggestions for mental health features (e.g., mood tracking, support groups) are welcome!

## 💁Acknowledgements
- Built with ❤️ by Ehsan, inspired by the need for mental health support communities.
- Thanks to the FastAPI and SQLModel communities for amazing tools!
