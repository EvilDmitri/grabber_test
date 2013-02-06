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

    def save(self):
        with open("data.txt", "w") as data:
            data.write(self.__repr__())

mapper(Film, films_table)
