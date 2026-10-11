from backend.app.core.database import engine


try:
    with engine.connect() as connection:
        print("================================")
        print("Database connection successful!")
        print("================================")

except Exception as e:
    print("================================")
    print("Database connection failed!")
    print("================================")
    print(e)