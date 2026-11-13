from repositories.user_repositories import UserRepository
from database import Session

session = Session()
session.close()
session = Session()
repo = UserRepository(session)
print(repo.get_status(5915029791))