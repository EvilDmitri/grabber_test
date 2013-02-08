import urllib
from grab.spider import Spider, Task, Data
from grab.tools.files import hashed_path_details

import os

import locale
enc = locale.getpreferredencoding()

import orm.models as model

BASE_PAGE = 'http://www.kinopoisk.ru/'
START = '298'
directory = '../images/'

import logging
logging.basicConfig(level=logging.DEBUG)

class KinoSpider(Spider):

    def task_generator(self):
        for x in range(int(START), int(START)+1):
            page = BASE_PAGE + 'film/' + str(x)
            yield Task('initial', url=page)

    def task_initial(self, grab, task):
        film = model.Film()

        film.rus_name = grab.xpath_text('//h1[@class="moviename-big"]')

        film.eng_name = grab.xpath_text('//span[@itemprop="alternativeHeadline"]')
        film.director = grab.xpath_text('//td[@itemprop="director"]')

        actors =  grab.xpath('//td[@class="actor_list"]')[1].text_content().strip().splitlines()
        film.actors = ", ".join(actors[:-1:2])

        ages = []
        for elem in grab.xpath_list('//tr[@class="ratePopup"]'):
            ages.append(elem.text_content())
        film.age_limit = " ".join(ages[0].split()[1:])
        film.rate_r = " ".join(ages[1].split()[2:])

        image_link = grab.xpath('//div[@class="film-img-box"]').getchildren()[0].items()[1][1].split("'")[1]
        film.film_img = self.save_img(image_link, film.eng_name)['full_path']



        page = task.url + '/stills/'
        yield Task('still', url=page, film=film)



    def task_still(self, grab, task):
        a = grab.xpath('//table[@class="fotos"]')[0][0]
        images_link = BASE_PAGE + a[0].values()[0]
        yield Task('get_still', url=images_link, film = task.film)


    def task_get_still(self, grab, task):
        a = grab.xpath('//img[@id="image"]')
        link = a.get("src")
        task.film.still =  self.save_img(link, task.film.eng_name +'(foto)')['full_path']

        model.store(task.film)



    def save_img(self, image, name):
        filename = hashed_path_details(name)
        if not os.path.exists(directory + filename['directory']):
            os.makedirs(directory + filename['directory'])

        if not os.path.exists(directory + filename['full_path']):
            image = urllib.urlopen(image).read()
            with open(directory + filename['full_path'], "wb") as f:
                print (directory + filename['full_path'])
                f.write(image)
        return filename









def main():

    # Create directory for images
    if not os.path.exists(directory):
        os.makedirs(directory)

    threads = 1

    bot = KinoSpider(thread_number=threads,network_try_limit=10)

    try: bot.run()
    except KeyboardInterrupt: pass

    print bot.render_stats()

if __name__ == '__main__':
    main()


