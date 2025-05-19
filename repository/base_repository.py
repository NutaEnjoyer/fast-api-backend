from database import new_session

class BaseRepository:
    def __init__(self, session=new_session):
        self.session = session
