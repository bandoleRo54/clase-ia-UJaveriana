"""
Example: FastAPI Application with User Management
This module demonstrates a simple API for user management.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


app = FastAPI(title="User Management API")


# Models
class User(BaseModel):
    """User model for API requests and responses."""
    name: str
    email: str
    age: int


class UserResponse(User):
    """User response model with ID."""
    id: int
    created_at: datetime


# In-memory database
users_db: dict = {}
next_id = 1


# Routes
@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    """
    Create a new user in the system.
    
    Args:
        user: User data (name, email, age)
    
    Returns:
        Created user with ID and timestamp
    
    Raises:
        HTTPException: If user age < 18
    """
    global next_id
    
    if user.age < 18:
        raise HTTPException(
            status_code=400,
            detail="User must be at least 18 years old"
        )
    
    user_id = next_id
    next_id += 1
    
    users_db[user_id] = {
        **user.dict(),
        "id": user_id,
        "created_at": datetime.now()
    }
    
    return users_db[user_id]


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Get information about a specific user.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        User object with all information
    
    Raises:
        HTTPException: If user not found
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users_db[user_id]


@app.get("/users/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    """
    List all users with pagination.
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
    
    Returns:
        List of users
    """
    users = list(users_db.values())
    return users[skip : skip + limit]


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    """
    Update an existing user.
    
    Args:
        user_id: The ID of the user to update
        user: New user data
    
    Returns:
        Updated user object
    
    Raises:
        HTTPException: If user not found
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id].update(user.dict())
    return users_db[user_id]


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """
    Delete a user from the system.
    
    Args:
        user_id: The ID of the user to delete
    
    Returns:
        Confirmation message
    
    Raises:
        HTTPException: If user not found
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, connection_string: str):
        """
        Initialize the database manager.
        
        Args:
            connection_string: Database connection string
        """
        self.connection = connection_string
        self.is_connected = False
    
    def connect(self):
        """
        Establish connection to the database.
        
        Returns:
            True if connection successful
        
        Raises:
            ConnectionError: If connection fails
        """
        try:
            # Connection logic
            self.is_connected = True
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {e}")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        Execute a SQL query.
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
        
        Returns:
            Query results
        
        Raises:
            ConnectionError: If not connected
        """
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        
        # Query execution logic
        return []


def process_data(input_file: str, output_file: str) -> bool:
    """
    Process data from input file and write to output file.
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
    
    Returns:
        True if processing successful
    """
    try:
        # Processing logic
        return True
    except Exception as e:
        print(f"Error processing data: {e}")
        return False


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "User Management API",
        "version": "1.0.0"
    }
