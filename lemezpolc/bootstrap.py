from peewee_models import db, Release


def create_tables():
    db.connect()
    db.drop_tables([Release])
    db.create_tables([Release])
    
create_tables()
