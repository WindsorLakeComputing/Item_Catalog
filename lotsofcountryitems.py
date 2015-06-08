from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Country, Base, CountryItem, User

engine = create_engine('sqlite:///country.db')
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


# Create dummy user
user1 = User(name="Ivan Konev", email="Ivan@ussr.com",
             picture='http://upload.wikimedia.org/wikipedia/commons/6/6e/IS_Konev_01.jpg')
session.add(user1)
session.commit()

country1 = Country(name="Bulgaria")

session.add(country1)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Vitosha", description="First Bulgarian made computer",
                     country=country1)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title=" IMKO-1", description="The first Bulgarian-made personal computer",
                     country=country1)

session.add(countryItem2)
session.commit()

print "added country items!"