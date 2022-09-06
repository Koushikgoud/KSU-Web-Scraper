import sys
sys.path.append('/Users/koushik/Documents/python/IRa1/')
from IRa1.items import Ira1Item
import requests
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider

#Three pre-defined urls that are scraped first
urls = [
        'https://www.kennesaw.edu/',
        'https://ccse.kennesaw.edu/',
        'https://studentaffairs.kennesaw.edu/',
    ]


for url in urls:
    #Spider code
    class KSUwebsiteSpider(scrapy.Spider):
        name = "webpages"
        allowed_domains = ['kennesaw.edu']
        start_urls = [
            'https://www.kennesaw.edu/',
            'https://ccse.kennesaw.edu/',
            'https://studentaffairs.kennesaw.edu/',
        ]
        rules = (
            Rule(LinkExtractor(allow=('kennesaw\.edu', ))),
        )
        pageid = 0
        

        def parse(self, response):
            #Crawling webpages to find title, pageid, url, mails and body data.
            entry = Ira1Item()
            title = response.css("title::text").get()
            body = ' '.join(BeautifulSoup(response.text, "lxml").get_text('').split())
            self.pageid += 1
            if self.pageid > 1001:
                raise CloseSpider(f"Scraped {self.pageid-1} pages. Eject!")
            else:
                url = response.url
                base_url = url
                email_regex= "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
                email_url = requests.get(url)
                html_text = email_url.text
                mails = re.findall(email_regex, html_text)
                page_urls = response.css("a::attr(href)").getall()
                entry['pageid'] = self.pageid
                entry['title'] = title
                entry['body'] = body
                entry['url'] = url
                entry['mails'] = mails    
                keys = ['pageid','url', 'title', 'body', 'mails']     
                yield entry
            
                #crawling through all the sublinks present in each webpage.
                for page_url in page_urls:
                    if str(page_url).startswith('/'):
                        page_url = urljoin(base_url, page_url)
                        yield response.follow(page_url, callback = self.parse)
                    elif str(page_url).startswith('http'):
                        yield response.follow(page_url, callback = self.parse)
                    else:
                        break
                
                    
            