from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

class Film(object):

    def __init__(self, rus_name=None, eng_name=None, director=None, actors=None, film_img=None,
                age_limit=None, rate_r=None, still=None):
        self.rus_name = rus_name
        self.eng_name = eng_name
        self.director = director
        self.actors = actors
        self.film_img = film_img
        self.age_limit = age_limit
        self.rate_r = rate_r
        self.still = still

    def __repr__(self):
        return "Film - %s (%s)" % (self.rus_name, self.eng_name)



engine = create_engine('sqlite:///../films.db', echo=False)
metadata = MetaData()



films_table = Table('films', metadata,
    Column('id', Integer, primary_key=True),
    Column('rus_name', String(50)),
    Column('eng_name', String(50)),
    Column('director', String(50)),
    Column('actors', String(250)),
    Column('film_img', String(150)),
    Column('age_limit', String(150)),
    Column('rate_r', String(50)),
    Column('still', String(50))
)



metadata.create_all(engine)

mapper(Film, films_table)

Session = sessionmaker(bind=engine)

session = Session()

def store(film):
    session.add(film)
    session.commit()








