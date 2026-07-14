# ==============================================================================
# ASCENDRITE Pre-Phase 0 Infrastructure Connectivity and Privilege Preflight
# ==============================================================================
# Reusable, secure script to verify infrastructure status, versions, extension
# capabilities, and privilege boundaries before starting migration.
#
# Usage:
#   python scratch/preflight_checks.py
# ------------------------------------------------------------------------------

import os
import sys
import urllib.parse
from dotenv import load_dotenv

# 1. Bootstrapping environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_local_path = os.path.join(BASE_DIR, ".env.local")
if os.path.exists(env_local_path):
    load_dotenv(env_local_path)

# Inject server source directory into path
sys.path.append(os.path.join(BASE_DIR, "platform", "server"))

try:
    from core.config import settings
    import psycopg2
    import pymongo
    import redis
except ImportError as ie:
    print(f"Error: Required dependency missing: {ie}")
    sys.exit(1)

def run_postgres_checks():
    print("\n======================================================================")
    print("1. PostgreSQL and pgvector Preflight")
    print("======================================================================")
    
    host = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    database = settings.POSTGRES_DATABASE
    admin_user = settings.POSTGRES_ADMIN_USER
    admin_pass = settings.POSTGRES_ADMIN_PASSWORD
    app_user = settings.POSTGRES_APP_USER
    app_pass = settings.POSTGRES_APP_PASSWORD

    # Connection as Admin
    print(f"[ADMIN] Connecting to '{database}' database as '{admin_user}'...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_pass,
            database=database
        )
        print("[PASS] Connection successful.")
        
        with conn.cursor() as cur:
            # Check availability of pgvector extension
            cur.execute("SELECT default_version, installed_version FROM pg_available_extensions WHERE name = 'vector';")
            row = cur.fetchone()
            if row:
                default_ver, installed_ver = row
                print(f"[INFO] pgvector default version: {default_ver}, installed version: {installed_ver or 'None'}")
                if not installed_ver:
                    print("[INFO] pgvector extension not enabled. Enabling extension...")
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                    print("[PASS] CREATE EXTENSION vector succeeded.")
                else:
                    print("[PASS] pgvector extension is already enabled.")
                
                # Vector compatibility checks
                print("[INFO] Executing reversible vector capability test...")
                try:
                    cur.execute("CREATE TABLE preflight_vector_test (id serial PRIMARY KEY, embedding vector(3));")
                    cur.execute("INSERT INTO preflight_vector_test (embedding) VALUES ('[1.0, 2.0, 3.0]'), ('[4.0, 5.0, 6.0]'), ('[1.1, 2.1, 3.1]');")
                    cur.execute("SELECT id, embedding <-> '[1.0, 2.0, 3.0]' AS distance FROM preflight_vector_test ORDER BY distance;")
                    rows = cur.fetchall()
                    print("[PASS] Query executed successfully. Results:")
                    for r in rows:
                        print(f"       - ID: {r[0]}, Distance: {r[1]}")
                finally:
                    cur.execute("DROP TABLE IF EXISTS preflight_vector_test;")
                    print("[PASS] Temporary vector table dropped successfully.")
            else:
                print("[FAIL] pgvector extension is not available on this PostgreSQL server instance.")
        conn.close()
    except Exception as e:
        print(f"[FAIL] PostgreSQL Admin preflight failed: {e}")

    # Connection as Application (Runtime privilege separation)
    print(f"[APP] Connecting to '{database}' database as '{app_user}'...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=app_user,
            password=app_pass,
            database=database
        )
        print("[PASS] Connection successful.")
        
        with conn.cursor() as cur:
            # Check SELECT capability
            cur.execute("SELECT 1;")
            val = cur.fetchone()[0]
            if val == 1:
                print("[PASS] Basic SELECT capabilities verified.")
                
            # Verify DDL protection (PoLP)
            try:
                cur.execute("CREATE TABLE preflight_app_test (id int);")
                print("[WARN] App role was able to create tables. Review DDL permissions.")
                cur.execute("DROP TABLE preflight_app_test;")
            except psycopg2.DatabaseError as de:
                print(f"[PASS] App role is correctly restricted from schema creation (DDL).")
                print(f"       Observed message: {de.pgerror.strip()}")
                conn.rollback()
        conn.close()
    except Exception as e:
        print(f"[FAIL] PostgreSQL App preflight failed: {e}")

def run_mongodb_checks():
    print("\n======================================================================")
    print("2. MongoDB Preflight")
    print("======================================================================")
    
    host = settings.MONGODB_HOST
    port = settings.MONGODB_PORT
    database_name = settings.MONGODB_DATABASE
    auth_source = settings.MONGODB_AUTH_SOURCE
    
    admin_user = settings.MONGODB_ADMIN_USER
    admin_pass = settings.MONGODB_ADMIN_PASSWORD
    app_user = settings.MONGODB_APP_USER
    app_pass = settings.MONGODB_APP_PASSWORD

    # Connection as Admin
    print(f"[ADMIN] Connecting to '{database_name}' database as '{admin_user}' (AuthSource: {auth_source})...")
    try:
        encoded_user = urllib.parse.quote_plus(admin_user)
        encoded_pass = urllib.parse.quote_plus(admin_pass)
        uri = f"mongodb://{encoded_user}:{encoded_pass}@{host}:{port}/{database_name}?authSource={auth_source}"
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("[PASS] Connection successful.")
        
        db = client[database_name]
        print("[INFO] Performing write/delete capabilities test...")
        try:
            coll = db["preflight_admin_test"]
            coll.insert_one({"preflight": True})
            doc = coll.find_one({"preflight": True})
            if doc and doc.get("preflight"):
                print("[PASS] Admin write and read operations successful.")
        finally:
            db["preflight_admin_test"].drop()
            print("[PASS] Temporary preflight collection dropped.")
        client.close()
    except Exception as e:
        print(f"[FAIL] MongoDB Admin preflight failed: {e}")

    # Connection as Application (Runtime privilege separation)
    print(f"[APP] Connecting to '{database_name}' database as '{app_user}' (AuthSource: {auth_source})...")
    try:
        encoded_user = urllib.parse.quote_plus(app_user)
        encoded_pass = urllib.parse.quote_plus(app_pass)
        uri = f"mongodb://{encoded_user}:{encoded_pass}@{host}:{port}/{database_name}?authSource={auth_source}"
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("[PASS] Connection successful.")
        
        db = client[database_name]
        print("[INFO] Performing read/write capabilities test...")
        try:
            coll = db["preflight_app_test"]
            coll.insert_one({"preflight": True})
            doc = coll.find_one({"preflight": True})
            if doc and doc.get("preflight"):
                print("[PASS] App write and read operations successful.")
        finally:
            db["preflight_app_test"].drop()
            print("[PASS] Temporary preflight collection dropped.")
            
        # Verify restriction from administrative commands
        try:
            client.list_database_names()
            print("[WARN] App role was able to list server databases. Review cluster privileges.")
        except Exception as ae:
            print("[PASS] App role is correctly restricted from executing listDatabases command.")
            print(f"       Observed message: {ae}")
        client.close()
    except Exception as e:
        print(f"[FAIL] MongoDB App preflight failed: {e}")

def run_redis_checks():
    print("\n======================================================================")
    print("3. Memurai/Redis Preflight")
    print("======================================================================")
    
    host = settings.REDIS_HOST
    port = settings.REDIS_PORT
    db_idx = settings.REDIS_DATABASE
    admin_user = settings.REDIS_ADMIN_USER
    admin_pass = settings.REDIS_ADMIN_PASSWORD
    app_user = settings.REDIS_APP_USER
    app_pass = settings.REDIS_APP_PASSWORD

    # Connection as App
    print(f"[APP] Connecting to Redis on {host}:{port} db={db_idx} as '{app_user}'...")
    try:
        r = redis.Redis(host=host, port=port, username=app_user, password=app_pass, db=db_idx, socket_timeout=5)
        r.ping()
        print("[PASS] Connection successful.")
        
        # Test basic capabilities: SET, GET, EXPIRE, DELETE
        print("[INFO] Testing basic cache operations...")
        key = "ascendrite:preflight:test"
        r.set(key, "verified", ex=10)
        val = r.get(key)
        if val and val.decode("utf-8") == "verified":
            print("[PASS] Cache GET/SET capability verified.")
        ttl = r.ttl(key)
        if ttl > 0:
            print(f"[PASS] Expiration/TTL boundary capability verified (TTL: {ttl}s).")
        r.delete(key)
        print("[PASS] Temporary preflight keys removed.")
        
        # Try to flush db (should fail under standard role restriction)
        try:
            r.flushdb()
            print("[WARN] App cache role was able to flush the database. Review ACL rules.")
        except redis.exceptions.ResponseError as re:
            print("[PASS] App cache role is correctly restricted from administrative FLUSHDB command.")
            print(f"       Observed message: {re}")
    except Exception as e:
        print(f"[FAIL] Redis App preflight failed: {e}")

    # Connection as Admin
    print(f"[ADMIN] Connecting to Redis on {host}:{port} db={db_idx} as '{admin_user}'...")
    try:
        r = redis.Redis(host=host, port=port, username=admin_user, password=admin_pass, db=db_idx, socket_timeout=5)
        r.ping()
        print("[PASS] Connection successful.")
    except Exception as e:
        print(f"[FAIL] Redis Admin preflight failed: {e}")

if __name__ == "__main__":
    print("======================================================================")
    print("ASCENDRITE INFRASTRUCTURE CONNECTIVITY AND PRIVILEGE PREFLIGHT")
    print("======================================================================")
    run_postgres_checks()
    run_mongodb_checks()
    run_redis_checks()
    print("\n======================================================================")
    print("PREFLIGHT COMPLETED")
    print("======================================================================")
