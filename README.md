# Library Management System

## Overview
The **Library Management System** is a web-based application that allows users to browse books and administrators to manage the book collection efficiently. The system includes authentication for users and administrators, with specific privileges for each.

## Features
### 1. User Authentication
- Secure login and registration.
- Role-based access control (User/Admin).

### 2. Browse Books
- Available to both users and admins.
- Books can be filtered by:
  - Pagination (limit per page input by user).
  - Genre.
  - Rating.
- Search for a specific book using its unique **Book ID**.

### 3. Manage Books (Admin Only)
- Admins can **add new books** to the collection.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python (for backend development using Flask)
- Database (sqlite3)
- Frontend framework (HTML/CSS/JavaScript)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt  # For Python backend
   npm install  # If using Node.js
   ```
3. Configure database settings in `.env` file or settings file.
4. Run the application:
   ```sh
   python app.py  # For Flask
   npm start  # If using Node.js
   ```
5. Open `http://localhost:8000` (or your configured port) in a browser.

## API Endpoints
### Authentication
- `POST /register` - Register a new user.
- `POST /login` - Login to the system.

### Browse Books
- `GET /books` - Get a list of books with optional filters:
  - `?limit={num}` - Set the number of books per page.
  - `?genre={genre}` - Filter by genre.
  - `?rating={rating}` - Filter by rating.
- `GET /books/{id}` - Get details of a specific book by ID.

### Admin Management
- `POST /books` - Add a new book (Admin only).

## Technologies Used
- **Backend**: Flask
- **Database**: sqlite3
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: JWT or OAuth

