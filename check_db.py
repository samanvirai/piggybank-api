from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

def check_database_state():
    try:
        # Load environment variables
        env = os.getenv('FLASK_ENV', 'development')
        load_dotenv('.env.local')
        database_url = os.getenv('DATABASE_URL')
        
        print(f"Environment: {env}")
        print(f"Database URL: {database_url}\n")

        # Check Alembic state
        print("Checking Alembic state:")
        alembic_cfg = Config("alembic.ini")
        command.current(alembic_cfg)
        
        # Check database tables
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Get list of all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """))
            tables = [row[0] for row in result]
            
            print("\nExisting tables in database:")
            for table in tables:
                print(f"  - {table}")
            
            # Check if alembic_version table exists and its content
            if 'alembic_version' in tables:
                version = conn.execute(text("SELECT version_num FROM alembic_version;")).scalar()
                print(f"\nCurrent Alembic version: {version}")
            else:
                print("\nNo alembic_version table found - migrations may not be initialized")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_database_state()