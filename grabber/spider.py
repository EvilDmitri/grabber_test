import urllib
from grab.spider import Spider, Task, Data
from grab.tools.logs import default_logging
from grab import Grab
import re


from orm.models import Film
from worker import worker

BASE_PAGE = 'http://www.kinopoisk.ru/film/'
START = '598'


class KinoSpider(Spider):

    def task_generator(self):
        for x in range(int(START), int(START)+1):
            page = BASE_PAGE + str(x)
            print page
            yield Task('initial', url=page)

    def task_initial(self, grab, task):
        film = Film()
        film.rus_name = grab.xpath_text('//h1[@class="moviename-big"]')

        film.rus_name = grab.xpath_text('//h1[@class="moviename-big"]')
#
        film.eng_name = grab.xpath_text('//span[@itemprop="alternativeHeadline"]')
        film.director = grab.xpath_text('//td[@itemprop="director"]')
#
        film.actors = []
        for elem in grab.xpath_list('//span[@itemprop="actors"]'):
            film.actors.append(elem.text_content())
#
        ages = []
        for elem in grab.xpath_list('//tr[@class="ratePopup"]'):
            ages.append(elem.text_content())
#
        film.age_limit = " ".join(ages[0].split()[1:])
        film.rate_r = " ".join(ages[1].split()[2:])
#
        film.save()
#
#        image_link = grab.xpath('//div[@class="film-img-box"]').getchildren()[0].items()[1][1].split("'")[1]
#        image = urllib.urlopen(image_link).read()
#        with open(film.eng_name+'.jpg', "wb") as f:
#            f.write(image)

        #g.setup(url=page + 'stills')
        #yield Task('still', grab=g,)



    def task_still(self, g, task):

        a = g.xpath('//table[@class="fotos"]')
        b = a[1][1]
        link = b[0].values()[0]
        g.go(BASE_PAGE + link)


        img = g.xpath('//table[@id="main_table"]')




def main():
    threads = 1

    bot = KinoSpider(thread_number=threads,network_try_limit=10)

    try: bot.run()
    except KeyboardInterrupt: pass

    print bot.render_stats()

if __name__ == '__main__':
    main()