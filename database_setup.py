from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):    
    __tablename__ = 'user'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(500), nullable=False)
    picture = Column(String(500))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'email'        : self.email,
           'picture'      : self.picture
       }

class Country(Base):
    __tablename__ = 'country'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'      : self.user_id,
           'user'         : self.user
       }


class CountryItem(Base):
    __tablename__ = 'country_item'

    title =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    country_id = Column(Integer,ForeignKey('country.id'))
    country = relationship(Country)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'title'         : self.name,
           'description'   : self.description,
           'id'            : self.id,
           'description'   : self.description,
           'country_id'    : self.country_id,
           'country'       : self.country,
           'user_id'       : self.user_id,
           'user'          : self.user
       }



engine = create_engine('sqlite:///country.db')
 

Base.metadata.create_all(engine)
