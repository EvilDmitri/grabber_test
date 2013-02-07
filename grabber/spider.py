import urllib
from grab.spider import Spider, Task, Data

import os

import locale
enc = locale.getpreferredencoding()

from orm.models import Film

BASE_PAGE = 'http://www.kinopoisk.ru/'
START = '298'
directory = 'images'


class KinoSpider(Spider):

    def task_generator(self):
        for x in range(int(START), int(START)+1):
            page = BASE_PAGE + 'film/' + str(x)
            yield Task('initial', url=page)

    def task_initial(self, grab, task):
        film = Film()

        film.rus_name = grab.xpath_text('//h1[@class="moviename-big"]').encode("utf-8")

        film.eng_name = grab.xpath_text('//span[@itemprop="alternativeHeadline"]').encode("utf-8")
        film.director = grab.xpath_text('//td[@itemprop="director"]')

        film.actors = []
        for elem in grab.xpath_list('//span[@itemprop="actors"]'):
            film.actors.append(elem.text_content())

        ages = []
        for elem in grab.xpath_list('//tr[@class="ratePopup"]'):
            ages.append(elem.text_content())

        film.age_limit = " ".join(ages[0].split()[1:])
        film.rate_r = " ".join(ages[1].split()[2:])

        film.save()

        image_link = grab.xpath('//div[@class="film-img-box"]').getchildren()[0].items()[1][1].split("'")[1]
        filename = directory + os.path.sep + film.eng_name+'.jpg'
        image = urllib.urlopen(image_link).read()
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(image)

        page = task.url + '/stills/'
        yield Task('still', url=page, film_name=film.eng_name)



    def task_still(self, grab, task):
        a = grab.xpath('//table[@class="fotos"]')

        b = a[0][0]
        images_link = BASE_PAGE + b[0].values()[0]
        yield Task('get_still', url=images_link, film_name = task.film_name)


    def task_get_still(self, grab, task):
        a = grab.xpath('//img[@id="image"]')
        link = a.get("src")

        filename = directory + os.path.sep + task.film_name + '(foto)' + '.jpg'

        print '1'
        image = urllib.urlopen(link).read()
        print '2'
        with open(filename, "wb") as f:
            f.write(image)








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


