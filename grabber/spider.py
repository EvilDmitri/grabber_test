from grab.spider import Spider, Task, Data
from grab.tools.logs import default_logging
from grab import Grab
import re


from orm.models import Film
from worker import worker

BASE_PAGE = 'http://www.kinopoisk.ru/film/'
START = '298/'


class KinoSpider(Spider):

    def task_generator(self):
        for x in range(START, START+5):
            yield (BASE_PAGE + x)

    def task_initial(self, grab, task):
        film = Film()
        worker(g=grab, film=film)



def main():
    threads = 1
    #default_logging(grab_log="log/log.txt")
    fl = open("out.txt","w")

    bot = KinoSpider(thread_number=threads,network_try_limit=2)

    bot.out = fl

    try: bot.run()
    except KeyboardInterrupt: pass
    fl.close()

    print bot.render_stats()

if __name__ == '__main__':
    main()