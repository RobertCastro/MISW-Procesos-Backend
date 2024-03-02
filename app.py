from app_utils import create_flask_app

app = create_flask_app()

if __name__ == '__main__':
    # Only run the app if executed directly
    app.run()
