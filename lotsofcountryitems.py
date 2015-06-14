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

country1 = Country(user_id=1, name="Bulgaria")

session.add(country1)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Vitosha", description="First Bulgarian made computer",
                     country=country1)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="IMKO-1", description="The first Bulgarian-made personal computer",
                     country=country1)

session.add(countryItem2)
session.commit()


country2 = Country(user_id=1, name="Czechoslovakia")

session.add(country2)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Bata Shoe Organisation", description="A family-owned global footwear and fashion accessory manufacturer and retailer with acting headquarters",
                     country=country2)

session.add(countryItem2)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Wyborowa", description="Czech Vodka",
                     country=country2)

session.add(countryItem2)
session.commit()

country3 = Country(user_id=1, name="East Germany")

session.add(country3)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Praktica", description="A brand of camera manufactured by Pentacon in Dresden",
                     country=country3)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Trabant", description="A car that produced by East German auto maker VEB Sachsenring Automobilwerke Zwickau",
                     country=country3)

session.add(countryItem2)
session.commit()

country4 = Country(user_id=1, name="Hungary")

session.add(country4)
session.commit()

countryItem1 = CountryItem(user_id=1, title="MAVAG", description="A Hungarian rail vehicle producer",
                     country=country4)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Magomobil", description="The most important Hungarian vehicle manufacturer before World War II, based in Budapest.",
                     country=country4)

session.add(countryItem2)
session.commit()

country5 = Country(user_id=1, name="Poland")

session.add(country5)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Powszechna Kasa Oszczednosci Bank Polski Spolka Akcyjna", description="Poland's largest bank",
                     country=country5)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Polski Koncern Naftowy Orlen", description="A major Polish oil refiner and petrol retailer",
                     country=country5)

session.add(countryItem2)
session.commit()

country6 = Country(user_id=1, name="Romania")

session.add(country6)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Extreme Light Infrastructure", description="A laser facility that aims to host the most intense Beamline system world-wide, develop new interdisciplinary research opportunities with light from these lasers and secondary radiation derived from them, and make them available to an international scientific user community",
                     country=country6)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Goliat", description="The first artificial satellite developed in Romania",
                     country=country6)

session.add(countryItem2)
session.commit()

country7 = Country(user_id=1, name="Soviet Union")

session.add(country7)
session.commit()

countryItem1 = CountryItem(user_id=1, title="Gorkovsky Avtomobilny Zavod", description="The leading manufacturer of commercial vehicles in the Soviet Union",
                     country=country7)

session.add(countryItem1)
session.commit()


countryItem2 = CountryItem(user_id=1, title="Bolshevichka", description="A clothes factory in Moscow",
                     country=country7)

session.add(countryItem2)
session.commit()

print "added country items!"