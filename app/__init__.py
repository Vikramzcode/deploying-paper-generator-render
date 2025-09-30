import os
import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
db = SQLAlchemy()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# ... (lines 1-20 remain the same)

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # --- Database Configuration START ---
    db_user = os.getenv("DB_USER")
    db_pass_raw = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")  # No default value here!
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT", "3306") 

    if db_user and db_pass_raw and db_host and db_name:
        db_pass = urllib.parse.quote_plus(db_pass_raw)
        
        # *** NEW: Print the final URI for verification ***
        final_uri = f"mysql+pymysql://{db_user}:***@{db_host}:{db_port}/{db_name}"
        print(f"--- Using Remote Clever Cloud MySQL Configuration on HOST: {db_host} ---")
        print(f"--- Final SQLAlchemy URI (Excluding Password): {final_uri} ---")
        
        # Use the constructed URI for the app
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
        print("--- Using Local SQLite (or falling back) Configuration ---")
    # --- Database Configuration END ---

# ... (rest of the code remains the same)
"""def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # --- Database Configuration START ---
    # Remove the default '127.0.0.1' fallback from DB_HOST
    db_user = os.getenv("DB_USER")
    db_pass_raw = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")  # No default value here!
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT", "3306") # Keep 3306 as a safe default for the port

    if db_user and db_pass_raw and db_host and db_name:
        # URL-encode the password in case it contains special characters
        db_pass = urllib.parse.quote_plus(db_pass_raw)
        
        # Construct the URI using the host, port, user, pass, and name from env vars
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        print("--- Using Remote Clever Cloud MySQL Configuration ---")
    else:
        # Fallback to SQLite (only for local development/testing if variables are truly missing)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
        print("--- Using Local SQLite (or falling back) Configuration ---")
    # --- Database Configuration END ---"""

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401
        
        # This is where the connection attempt happens and fails if DB_HOST is wrong
        db.create_all()
        
        from .routes import main as main_bp
        app.register_blueprint(main_bp)

    return app
