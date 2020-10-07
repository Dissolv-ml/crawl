# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import scrapy
from ..items import Mobile







print(
    "*******************************************DISSOLV-ML****************************************************************************")

print("**FOR TEST/DEBUG ONLY**")
id = input("**ENTER THE ITEM YOU WANT TO DATAMINE:")
ab = '/s?k=' + id
wsite = "https://www.amazon.in/" + id + ab


# class enginespider(scrapy.Spider):
#      name = "engine"
#     start_urls = [url]

#    def parse(self, response, **kwargs):

#    title = response.css('title::text').extract()
#   yield {"title:": title}
#  print(title)






class AmazonScraper(scrapy.Spider):
    name = "amazonscraper"

    # How many pages you want to scrape
    no_of_pages = 1

    # ho Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

    def start_requests(self):
        # starting urls for scraping
        urls = [wsite]

        for url in urls: yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):

        self.no_of_pages -= 2

        # print(response.text)

        mobiles = response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()

        # print(len(mobiles))

        for mobile in mobiles:
            final_url = response.urljoin(mobile)
            yield scrapy.Request(url=final_url, callback=self.parse_mobile, headers=self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)

        if (self.no_of_pages > 0):
            next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=final_url, callback=self.parse, headers=self.headers)

    def parse_mobile(self, response):
        title = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath(
            "//h1[@id='title']//text()").get()
        brand = response.xpath("//a[@id='bylineInfo']//text()").get() or "not specified"
        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath(
            "//span[@class='a-icon-alt']//text()").get()

        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath(
            "//span[@id='priceblock_dealprice']//text()")
        print(price)
        if len(price) > 1:
            price = price[1].get()
        elif len(price) == 1:
            price = price[0].get()
        else:
            price = price.get()

        colour = response.xpath("//div[@id='variation_color_name']/div/span[@class='selection']//text()").get() or "not defined"
        instock = response.xpath("//div[@id='availability']").xpath(
            "//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        instock = instock.strip() == "In stock."
        reviews = response.xpath(
            "//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath(
            "//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()

        img_url = response.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get()

        description = []
        for description_temp in description_raw:
            description.append(description_temp.strip())

        print(title, brand, rating, price, instock)
        # print(final_review)
        # print(reviews)
        # print(description)

        #yield Mobile(title=title.strip(), brand=brand.strip(), rating=rating.strip(), price=price.strip(), instock=instock, reviews=reviews,
                    # description=description)

        yield Mobile(title=title, brand=brand, rating=rating, price=price,
                     colour=colour, instock=instock, reviews=reviews, description=description)

        #open('/home/data.csv')

    # FEED_URI = '/home/Desktop/data.csv' -s FEED_FORMAT=csv



#class CsvPipeline(object):
 #   def __init__(self):
  #      self.file = open("home/sharon/Desktop/booksdata.csv", 'wb')
   #     self.exporter = CsvItemExporter(self.file)
    #    self.exporter.start_exporting()

    #def close_spider(self, spider):
     #   self.exporter.finish_exporting()
      #  self.file.close()

    #def process_item(self, item, spider):
     #   self.exporter.export_item(item)
      #  return item











