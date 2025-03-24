## See demo
![Demo of AI Tutor](aitutor.gif)

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nguyenduchuyiu/aitutor.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd aitutor
   ```
3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
4. **Install required Python packages and openssl:**
   ```bash
    pip install -r requirements.txt
    sudo apt-get install openssl
   ```
5. **Setup GEMINI_API_KEY**
    ```bash
        export GEMINI_API_KEY="your_gemini_api_key"
    ```
6. **Setup PostgreSQL:**
   - Install PostgreSQL if it's not installed.
   - Create a database for your project.
   - Modify the `DATABASES` configuration in `settings.py` to match your database settings:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '',
         }
     }
     ```
7. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
8. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
9. **Start the development server:**
    - Generate a new private key with a passphrase
   ```bash
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=www.example.com"

    python manage.py runsslserver --certificate cert.pem --key key.pem
   ```
10. **Open your web browser and navigate to `https://localhost:8000/`**
    - Login with super user account
11. **Insert sample data in database**
    - Open https://localhost:8000/admin to add lesson info