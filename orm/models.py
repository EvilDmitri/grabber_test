from sqlalchemy import create_engine
engine = create_engine('sqlite:///films.db', echo=False)
from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
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

class Film(object):
    def __init__(self, rus_name, eng_name, director, actors, film_img, age_limit, rate_r, still):
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

mapper(Film, films_table)
