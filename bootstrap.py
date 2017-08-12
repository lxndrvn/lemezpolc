from models import db, Release


def create_tables():
    db.connect()
    db.create_tables([Release])
    
create_tables()