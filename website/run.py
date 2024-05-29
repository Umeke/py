import os

from app import create_app

app = create_app()
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
if __name__ == '__main__':
    app.run(debug=True)
