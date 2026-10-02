from database.connection import engine
from database.models import Base


def initialize_database():
    print("Creating database tables...")

    Base.metadata.create_all(engine)

    print("Database created successfully.")


if __name__ == "__main__":
    initialize_database()