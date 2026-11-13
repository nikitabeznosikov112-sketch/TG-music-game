from database import User, Session as dbSession
from sqlalchemy.orm import Session
class AdminRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self):
        return self.session.query(User).order_by(User.id).all()
    
    def get_user(self, tg_id: int):
        return self.session.query(User).filter_by(tg_id=tg_id).first()
    
    def reset_user(self, tg_id: int):
        user = self.get_user(tg_id)
        user.score = 0
        self.session.commit()

    def change_status(self, tg_id: int):
        user = self.get_user(tg_id)
        if user.subscription == False:
            user.subscription = True
            self.session.commit()
        else:
            user.subscription = False
            self.session.commit()
    def delete_user(self, tg_id: int):
        
        user = self.get_user(tg_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def change_score(self, tg_id: int, score: int):
        user = self.get_user(tg_id)
        user.score = score
        self.session.commit()

    def get_status(self, tg_id: int):
        user = self.get_user(tg_id)
        if user:
            return
