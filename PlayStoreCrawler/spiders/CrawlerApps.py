'''
	Product : Google Play Store Search result Crawler
	Author  : Lutfi Budi Ilmawan
	Mail    : luthfy13@live.com
	How to use it:
		scrapy crawl AppName -a KataKunci=[insert your keyword here] -o output.json
	Example :
		scrapy crawl AppName -a KataKunci="mobile legends" -o output.json
'''
import scrapy
import os
		
class crawlerapps(scrapy.Spider):
	name = "AppName"
	hasil = "degaga"
	def __init__(self, KataKunci="", *args, **kwargs):
		super(crawlerapps, self).__init__(*args, **kwargs)
		self.start_urls = [
			'https://play.google.com/store/search?q=' + KataKunci + '&c=apps&hl=en'
		]
	
	def parse(self, response):
		x = 0;
		y = 0;
		while (x<97): #97
			hasil = yield {
				'Nama App' : "".join(response.css('.details>.title::text')[x].extract()).replace("  ", "")[:-1],
				'Nama Package' : "".join(response.css('.details>.title::attr(href)')[y].extract()).replace("/store/apps/details?id=", ""),	
				'Developer': "".join(response.css('.details>.subtitle-container>.subtitle::text')[y].extract()),
				'Rating': "".join(response.css('.reason-set-star-rating>.star-rating-non-editable-container::attr(aria-label)')[y].extract()[7:10]),
				'Icon Path': "".join(response.css('.cover-inner-align>.cover-image::attr(data-cover-small)')[y].extract().replace("//", ""))
			}
			x = x + 2
			y = y + 1
			print hasil