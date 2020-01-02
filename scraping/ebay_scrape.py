from lxml import html
import requests
from pprint import pprint
import unicodecsv as csv
from traceback import format_exc
import argparse

def parse(url):
    for i in range(5):
        try:
            brand = 'Test'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            print("Retrieving %s" % (url))
            response = requests.get(url, headers=headers, verify=False)
            print("Parsing page")
            parser = html.fromstring(response.text)
            product_listings = parser.xpath('//li[contains(@class,"lvresult")]')
            raw_result_count = parser.xpath("//span[@class='rcnt']//text()")
            result_count = ''.join(raw_result_count).strip()
            print("Found {0} results for {1}".format(result_count, brand))
            scraped_products = []

            for product in product_listings:
                raw_url = product.xpath('.//a[@class="vip"]/@href')
                raw_title = product.xpath('.//a[@class="vip"]/text()')
                raw_price = product.xpath(".//li[contains(@class,'lvprice prc')]//span[@class='bold binsold']//text()")
                price = ' '.join(' '.join(raw_price).split())
                title = ' '.join(' '.join(raw_title).split())
                data = {
                    'url': raw_url[0],
                    'title': title,
                    'price': price
                }
                scraped_products.append(data)
            return scraped_products
        except Exception as e:
            print(format_exc(e))


scraped_data = parse('https://www.ebay.com/sch/i.html?_from=R40&_nkw=michael+jordan+auto&_in_kw=1&_ex_kw=&_sacat=0&LH_Complete=1&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=10977&_sargn=-1%26saslc%3D1&_salic=1&_sop=13&_dmd=1&_ipg=50&_fosrp=1')
print("Writing scraped data to %s-ebay-scraped-data.csv" % ('MJ'))

with open('%s-ebay-scraped-data.csv' % ('Test'), 'wb') as csvfile:
    fieldnames = ["title", "price", "url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for data in scraped_data:
        writer.writerow(data)