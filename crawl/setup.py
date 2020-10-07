#from scrapy.exporters import CsvItemExporter
#import scrapy
#from scrapy.crawler import CrawlerProcess
#from crawl.spiders import AmazonScraper

from os import system
import os.path

output_file_name = os.path.abspath('result.csv')
system('scrapy crawl amazonscraper -o'+output_file_name)




#process = CrawlerProcess()
#process.crawl(AmazonScraper)
#process.start()

#class CsvPipeline(object):
 #   def __init__(self):
  #      self.file = open("/home/sharon/Desktop/booksdata.csv", 'wb')
   #     self.exporter = CsvItemExporter(self.file)
    #    self.exporter.start_exporting()

    #d#ef close_spider(self, spider):
     #   self.exporter.finish_exporting()
      #  self.file.close()

    #def process_item(self, item, spider):
     #   self.exporter.export_item(item)
      #  return item
