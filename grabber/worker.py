from grab import Grab
import urllib

def worker(g, film):
    film.rus_name = g.xpath_text('//h1[@class="moviename-big"]')
    film.eng_name = g.xpath_text('//span[@itemprop="alternativeHeadline"]')
    film.director = g.xpath_text('//td[@itemprop="director"]')

    film.actors = []
    for elem in g.xpath_list('//span[@itemprop="actors"]'):
        film.actors.append(elem.text_content())

    ages = []
    for elem in g.xpath_list('//tr[@class="ratePopup"]'):
        ages.append(elem.text_content())

    film.age_limit = " ".join(ages[0].split()[1:])
    film.rate_r = " ".join(ages[1].split()[2:])

    image_link = g.xpath('//div[@class="film-img-box"]').getchildren()[0].items()[1][1].split("'")[1]

    image = urllib.urlopen(image_link).read()

    with open(film.eng_name+'.jpg', "wb") as f:
        f.write(image)



#    g.go(page + 'stills')
#    a = g.xpath('//table[@class="fotos"]')
#    b = a[1][1]
#    link = b[0].values()[0]
#    g.go(BASE_PAGE + link)
#
#
#    img = g.xpath('//table[@id="main_table"]')






