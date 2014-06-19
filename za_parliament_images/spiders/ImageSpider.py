from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

import urllib
import re

class ImageSpider(CrawlSpider):
    name = "image"
    allowed_domains = ["www.parliament.gov.za"]
    start_urls = [
        "http://www.parliament.gov.za/live/content.php?Category_ID=97",
    ]

    rules = (

        Rule(SgmlLinkExtractor(allow=('content\.php\?Item_ID=184&MemberID=[0-9]+', )), callback='parse_person'),

    )

    def parse_person(self, response):

        sel = Selector(response)

        images = sel.xpath('//img/@src').extract()

        for image in images:

            if re.match('http://www\.parliament\.gov\.za/content/.*\.jpg', image):
                name = image.rpartition('/')[2]
                urllib.urlretrieve(image, 'images/' + name)
