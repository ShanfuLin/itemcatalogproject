import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_dbsetup import User, Author, Work_titles, Discussion, Base
import datetime


engine = create_engine('sqlite:///authorsandworktitles.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#a = session.query(User).filter_by(email="mountainturtle87@gmail.com").one()
#a.superuser = "No"
#session.add(a)
#session.commit()

a = session.query(User).all()
#b = a.user

#print b.name

for item in a:
    print item.name, item.superuser, item.id

today = datetime.date.today()
print today
print today.strftime('%d/%m/%Y')
