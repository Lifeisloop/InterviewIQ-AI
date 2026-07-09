from database.connection import engine
from database.base import Base

from database.models.user import User
from database.models.resume import Resume
from database.models.interview import Interview

Base.metadata.create_all(bind=engine)
print("All tables are created successfully!")