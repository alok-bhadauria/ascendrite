import os
import sys
import urllib.parse
from sqlalchemy import create_engine, text

# Add platform/server directory to PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(os.path.dirname(script_dir), "platform", "server")
if server_dir not in sys.path:
    sys.path.append(server_dir)

from app.core.config import settings
from app.core.security import get_password_hash
from pymongo import MongoClient

def init_postgres():
    print("Connecting to PostgreSQL to verify database and initialize schema...")
    
    # Assemble Admin connection URL for default database to check/create the application database
    encoded_admin_user = urllib.parse.quote(settings.POSTGRES_ADMIN_USER, safe="")
    encoded_admin_pass = urllib.parse.quote(settings.POSTGRES_ADMIN_PASSWORD, safe="")
    
    admin_url = f"postgresql://{encoded_admin_user}:{encoded_admin_pass}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres"
    
    try:
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            # Check if database exists
            res = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{settings.POSTGRES_DATABASE}'"))
            if not res.fetchone():
                print(f"Database '{settings.POSTGRES_DATABASE}' not found. Creating database...")
                conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DATABASE}"))
            else:
                print(f"Database '{settings.POSTGRES_DATABASE}' already exists.")
        admin_engine.dispose()
    except Exception as e:
        print(f"Failed to check/create PostgreSQL database: {e}")
        return False

    # Connect to target application database to run init SQL schema script with admin privileges
    admin_app_url = f"postgresql://{encoded_admin_user}:{encoded_admin_pass}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
    app_engine = create_engine(admin_app_url)
    sql_file_path = os.path.join(script_dir, "init_postgres.sql")
    
    if not os.path.exists(sql_file_path):
        print(f"PostgreSQL init schema file not found at: '{sql_file_path}'")
        return False
        
    try:
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_commands = f.read()
            
        print("Executing PostgreSQL schema script DDL commands...")
        with app_engine.connect() as conn:
            # Split commands by semicolon to run individually
            for command in sql_commands.split(";"):
                clean_command = command.strip()
                if clean_command:
                    conn.execute(text(clean_command))
            conn.commit()
            
        print("PostgreSQL database tables and indexes initialized successfully.")
        return True
    except Exception as e:
        print(f"Failed to execute PostgreSQL schema script: {e}")
        return False
    finally:
        app_engine.dispose()

def init_mongodb():
    print("Connecting to MongoDB to configure collections and unique indexes...")
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB_NAME]
        
        # Enforce unique indexes
        print("Enforcing MongoDB collection indexes...")
        db["users"].create_index("email", unique=True)
        db["user_identities"].create_index([("provider", 1), ("provider_user_id", 1)], unique=True)
        db["sessions"].create_index("expires_at")
        db["subjects"].create_index("subject_id", unique=True)
        db["topics"].create_index([("subject_id", 1), ("topic_id", 1)], unique=True)
        
        print("MongoDB collections and indices initialized successfully.")
        return db
    except Exception as e:
        print(f"Failed to initialize MongoDB indices: {e}")
        return None

def seed_users(mongo_db):
    print("Seeding initial administrator and developer credential records...")
    
    # 3 Seed user specifications
    seed_data = [
        {
            "id": "usr_admin001",
            "email": "admin@ascendrite.com",
            "first_name": "Alok",
            "last_name": "Bhadauria",
            "role": "Admin",
            "password": "Admin@123",
            "capabilities": ["knowledge:read", "knowledge:write", "knowledge:publish", "admin:manage", "admin:write", "creator:write"]
        },
        {
            "id": "usr_creator002",
            "email": "creator@ascendrite.com",
            "first_name": "Author",
            "last_name": "Account",
            "role": "Contributor",
            "password": "Creator@123",
            "capabilities": ["knowledge:read", "knowledge:write", "creator:write"]
        },
        {
            "id": "usr_learner003",
            "email": "learner@ascendrite.com",
            "first_name": "Learner",
            "last_name": "Account",
            "role": "Student",
            "password": "Learner@123",
            "capabilities": ["knowledge:read"]
        }
    ]
    
    # Seed PostgreSQL
    encoded_admin_user = urllib.parse.quote(settings.POSTGRES_ADMIN_USER, safe="")
    encoded_admin_pass = urllib.parse.quote(settings.POSTGRES_ADMIN_PASSWORD, safe="")
    admin_app_url = f"postgresql://{encoded_admin_user}:{encoded_admin_pass}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
    pg_engine = create_engine(admin_app_url)
    try:
        with pg_engine.connect() as pg_conn:
            # Clean existing seed IDs to allow updating user capabilities
            seed_ids = [user["id"] for user in seed_data]
            pg_conn.execute(text("DELETE FROM users WHERE id = ANY(:ids)"), {"ids": seed_ids})
            
            for user in seed_data:
                # Insert into users table
                pg_conn.execute(
                    text("""
                        INSERT INTO users (id, email, first_name, last_name, role)
                        VALUES (:id, :email, :first_name, :last_name, :role)
                    """),
                    {
                        "id": user["id"],
                        "email": user["email"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "role": user["role"]
                    }
                )
                
                # Insert into user_identities
                hashed_pw = get_password_hash(user["password"])
                pg_conn.execute(
                    text("""
                        INSERT INTO user_identities (user_id, provider, provider_user_id, password_hash)
                        VALUES (:user_id, 'local', :email, :password_hash)
                    """),
                    {
                        "user_id": user["id"],
                        "email": user["email"],
                        "password_hash": hashed_pw
                    }
                )
                
                # Insert workspace settings
                pg_conn.execute(
                    text("""
                        INSERT INTO workspace_settings (user_id, theme)
                        VALUES (:user_id, 'dark')
                    """),
                    {"user_id": user["id"]}
                )
            pg_conn.commit()
        print("PostgreSQL seed user entries written successfully.")
    except Exception as e:
        print(f"Failed to seed users in PostgreSQL: {e}")
    finally:
        pg_engine.dispose()

    # Seed MongoDB
    if mongo_db is not None:
        try:
            # Clean existing seed IDs
            seed_ids = [user["id"] for user in seed_data]
            mongo_db["users"].delete_many({"_id": {"$in": seed_ids}})
            mongo_db["user_identities"].delete_many({"user_id": {"$in": seed_ids}})
            
            for user in seed_data:
                # Insert users doc
                mongo_db["users"].insert_one({
                    "_id": user["id"],
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "role": user["role"],
                    "is_active": True,
                    "preferences": {
                        "theme": "dark",
                        "notifications_enabled": True,
                        "interest": "ai" if user["role"] == "Admin" else "web-development"
                    },
                    "is_deleted": False
                })
                
                # Insert user_identities doc
                hashed_pw = get_password_hash(user["password"])
                mongo_db["user_identities"].insert_one({
                    "user_id": user["id"],
                    "provider": "local",
                    "provider_user_id": user["email"],
                    "password_hash": hashed_pw,
                    "mfa_enabled": False
                })
            print("MongoDB seed user entries written successfully.")
        except Exception as e:
            print(f"Failed to seed users in MongoDB: {e}")

def main():
    print("======================================================================")
    print("               ASCENDRITE DATABASE INITIALIZATION WORKFLOW            ")
    print("======================================================================")
    
    postgres_ok = init_postgres()
    mongo_db = init_mongodb()
    
    if postgres_ok or mongo_db is not None:
        seed_users(mongo_db)
        print("Database initialization and user credentials mapping complete.")
    else:
        print("Database initialization failed.")

if __name__ == "__main__":
    main()
