
# Social Network Prototype

## Overview

This is a small prototype of a social network developed using Django and PostgreSQL. The application allows users to manage profiles, create and like posts, and receive notifications when a post gets liked. The prototype is designed to showcase key social media features like posting, liking, and notifications in a simple format.

### Key Features:
- **User Profiles**: Users can edit their profile, including updating their avatar and username.
- **Posts**: Users can create posts (with video or image URLs), like posts, and view their own posts and liked posts.
- **Notifications**: Users receive notifications when their posts are liked by others.

## Setup

### Prerequisites

Ensure that the following tools are installed on your machine:
- **Docker** (for containerizing the application)
- **Docker Compose** (to orchestrate the containers)
- **PostgreSQL** (used for data storage)

### How to Run the Application

Follow these steps to set up and run the project using Docker Compose:

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   touch .env
   ```

2. **Build and run the project**:
   copy all from .env_example to .env
   ```bash
   docker compose up --build
   ```

3. **Enter the running web container**:

   ```bash
   docker exec -it web bash
   ```

4. **Run the database migrations**:

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Create a superuser for accessing the admin panel**:

   ```bash
   python3 manage.py createsuperuser
   ```

6. The API documentation is available at: [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)

---

## API Endpoints

Below are the API endpoints available in the system, along with example `curl` commands to interact with them.

### **User Profile Endpoints**

1. **Get User Profile (`GET /api/users/`)**

   Fetch the authenticated user’s profile:

   ```bash
   curl -X GET http://127.0.0.1:8000/api/users/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

2. **Update User Profile (`PATCH /api/users/`)**

   Update the authenticated user’s profile (e.g., username or avatar):

   ```bash
   curl -X PATCH http://127.0.0.1:8000/api/users/    -H "Authorization: Bearer <token>"    -H "Content-Type: application/json"    -d '{
     "username": "john_doe",
     "avatar": "http://example.com/new_avatar.jpg"
   }'
   ```

---

### **Post Endpoints**

1. **Create a New Post (`POST /api/posts/`)**

   Create a new post by providing a URL for the content (image or video):

   ```bash
   curl -X POST http://127.0.0.1:8000/api/posts/    -H "Authorization: Bearer <token>"    -H "Content-Type: application/json"    -d '{
     "content_url": "http://example.com/photo.jpg"
   }'
   ```

2. **Get User’s Posts (`GET /api/posts/mine/`)**

   Fetch all posts created by the authenticated user:

   ```bash
   curl -X GET http://127.0.0.1:8000/api/posts/mine/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

3. **Get Liked Posts (`GET /api/posts/liked/`)**

   Fetch all posts liked by the authenticated user:

   ```bash
   curl -X GET http://127.0.0.1:8000/api/posts/liked/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

4. **Like a Post (`POST /api/posts/<post_id>/like/`)**

   Like a specific post by providing the post ID:

   ```bash
   curl -X POST http://127.0.0.1:8000/api/posts/1/like/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

5. **Update a Post (`PATCH /api/posts/<post_id>/`)**

   Update an existing post by providing the post ID and new content:

   ```bash
   curl -X PATCH http://127.0.0.1:8000/api/posts/1/    -H "Authorization: Bearer <token>"    -H "Content-Type: application/json"    -d '{
     "content_url": "http://example.com/updated_photo.jpg"
   }'
   ```

6. **Delete a Post (`DELETE /api/posts/<post_id>/delete/`)**

   Delete a specific post by providing the post ID:

   ```bash
   curl -X DELETE http://127.0.0.1:8000/api/posts/1/delete/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

---

### **Notification Endpoints**

1. **Get Notifications (`GET /api/notifications/`)**

   Fetch notifications related to the authenticated user’s posts (e.g., when someone likes a post):

   ```bash
   curl -X GET http://127.0.0.1:8000/api/notifications/    -H "Authorization: Bearer <token>"    -H "accept: application/json"
   ```

---

### Swagger UI for API Documentation

You can explore and test the API via the interactive Swagger UI, which is available at:

[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)

---

## Additional Notes

- **Authentication**: Replace `<token>` in the `curl` commands with your actual JWT token if you are using token-based authentication. If you are using session-based authentication, you will need to modify the commands accordingly (e.g., use session cookies).
- **Superuser**: You can access the Django admin panel using the superuser account you created by visiting `http://127.0.0.1:8000/admin/`.
- **Database**: The system uses PostgreSQL for data storage. Ensure that the PostgreSQL service is running before starting the application.
