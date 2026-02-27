from sqlmodel import create_engine, Session, SQLModel
import time


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False es necesario solo para SQLite
# Solo añade esto si usas SQLite. 
# Si luego cambias a PostgreSQL o MySQL, debes quitarlo.
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

