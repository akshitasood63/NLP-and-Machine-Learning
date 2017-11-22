# -*- coding: utf-8 -*-
#crawled 1 page as of now.need to crawl 2 more pages.--------------------
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import TextResponse,Request
from urllib.parse import urljoin

class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.in']
    #start_urls = ['https://www.tripadvisor.in/Restaurants-g304552-Shimla_Shimla_District_Himachal_Pradesh.html']
	#//*[@id="taplc_restaurants_coverpage_content_0"]/div[1]/div[2]/div/div[2]/div[3]/div/a/div/div/div/img
	#//*[@id="taplc_restaurants_coverpage_content_0"]/div[1]/div[1]/div/div[2]/div[3]/div/a/div/div/div/img
	#//img/@src----earlier
	#//*[@class="poi"]//a/@href
	
    def start_requests(self):
        url='https://www.tripadvisor.in/Restaurants-g304552-Shimla_Shimla_District_Himachal_Pradesh.html'
        yield scrapy.Request(url=url,callback=self.parse)
		
    def parse(self, response):
        l=response.xpath('//*[@class="title"]/a/@href').extract()
        print(l)
		
        #print("------------------------------------------")
        urls=[]
        for image in l:
	        print(image)
        	urls.append(image)
        #print("------------------------------------------")
		#to fetch all the links present(all data with 'href' tag)
 
        for i in urls:
            #print (response.urljoin(i))
            yield response.follow(response.urljoin(i),self.parse_about)

    def parse_about(self, response):
        def extract_with_css(query):
            return response.css(query).extract()
        
		#this function will fetch the content ,date and title of the headline
        res={
              'name':extract_with_css('.heading_title::text'),
              #'rating':response.xpath('//*[@id="taplc_location_detail_header_restaurants_0"]/div[1]/span[1]/div/div/span').extract_first()
              #'rating':extract_with_css('.ui_bubble_rating_45')
			  'review':''.join(extract_with_css('.partial_entry::text')),
			  #''.join(review)
              #'rating':response.xpath('//div//span [contains(@class,"ui_bubble_rating")]')
              #'Rating': response.xpath('//div[@class="claim false"]/span//text()').extract_first()
        }
        yield (res)