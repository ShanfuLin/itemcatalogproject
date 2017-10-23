from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    picture_url = Column(String(250))
    superuser = Column(String(3))
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'           : self.id,
            'name'         : self.name,
            'email'        : self.email,
            'picture_url'  : self.picture_url,
        }


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    dob = Column(String(250))
    country = Column(String(250))
    category = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'           : self.id,
            'name'         : self.name,
            'dob'          : self.dob,
            'country'      : self.country,
        }


class Work_titles(Base):
    __tablename__ = 'work_titles'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    work_title = Column(String(250), nullable=False)
    category = Column(String(250))
    summary = Column(String(1000))
    author = relationship(Author)
    owner = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'           : self.id,
            'work_title'   : self.work_title,
            'category'     : self.category,
            'summary'      : self.summary,
        }


class Discussion(Base):
    __tablename__ = 'discussion'

    id = Column(Integer, primary_key=True)
    message = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    work_id = Column(Integer, ForeignKey('work_titles.id'))
    date_created = Column(String(250))
    user = relationship(User)
    work_title = relationship(Work_titles)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'           : self. id,
            'message'      : self. message,
            'user'        : self. user_id,
            'date'        : self.date_created,
        }


engine = create_engine('sqlite:///authorsandworktitles.db')
Base.metadata.create_all(engine)
