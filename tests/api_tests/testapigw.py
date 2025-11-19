import sys
import subprocess
import pytest
from fastapi.testclient import TestClient
import os
import time  # To allow the server to start before running tests

# Add the path to the api_gateway folder for importing server_1.py
sys.path.append(r"E:\OptiFlow_VS_project\api_gateway")  # Add the absolute path

# Verify the current working directory (helpful for debugging)
print(f"Current working directory: {os.getcwd()}")

# Start the server process
def start_server():
    """Starts server_1.py and captures log messages."""
    process = subprocess.Popen(
        ['python', r'E:\OptiFlow_VS_project\api_gateway\api_gateway_entry.py'],  # Full path to server_1.py
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    print("Server started successfully. Printing log messages:")

    # Print log messages asynchronously
    def print_logs():
        for line in process.stdout:
            print(line, end="")  # Print server logs line by line

    # Start printing logs in the background
    import threading
    threading.Thread(target=print_logs, daemon=True).start()

    # Return the process to manage or stop it later if needed
    return process

# Import the FastAPI application
from api_gateway_entry import app  # Ensure api_gateway_entry exists and has the FastAPI app instance

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

# Define test functions
def test_root():
    """Test the root endpoint of the FastAPI application."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to OptiFlow API Gateway!", "ip": "127.0.0.1"}

def test_health_check():
    """Test the health check endpoint of the FastAPI application."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Run tests and manage server lifecycle
if __name__ == "__main__":
    # Start the server
    server_process = start_server()
    
    # Allow the server to initialize
    time.sleep(2)
    
    try:
        # Run pytest to execute test functions
        pytest.main(["-q", "--disable-warnings"])
    finally:
        # Terminate the server process after tests complete
        server_process.terminate()
        print("Server stopped.")