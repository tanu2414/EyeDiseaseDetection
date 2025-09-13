#!/usr/bin/env python3
"""
Run script for the Eye Disease Prediction Flask application.
"""

import os
from app import app, db

def create_tables():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def main():
    """Main function to run the application."""
    # Create uploads directory if it doesn't exist
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created {uploads_dir} directory")
    
    # Create database tables
    create_tables()
    
    # Run the Flask application
    print("Starting Eye Disease Prediction Application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()