# Import the Flask app factory function
from server import create_app

# Create an instance of the Flask app
app = create_app()

# Run the app only if this file is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
