'''
	Product : Google Play Store Text Review Crawler
	Author  : Lutfi Budi Ilmawan
	Mail    : luthfy13@live.com
	How to use it:
		scrapy crawl TextReviewEn -a NamaPackage=[insert the package name here] -a JmlIterasi=[how many times do you want to repeat the request [1 .. infinite] -o output.json
	Example :
		scrapy crawl TextReviewEn -a NamaPackage=com.whatsapp -a JmlIterasi=200 -o review.json
	PS: This web crawler get 40 record on one request.
'''
import scrapy
import os
from bs4 import BeautifulSoup as BS
from langdetect import detect

class crawlerreviews(scrapy.Spider):
	JML = 0
	indeks = 0
	#self.__class__.JML
	if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")
	
	name = 'TextReviewEn'
	def __init__(self, JmlIterasi=0, *args, **kwargs):
		super(crawlerreviews, self).__init__(*args, **kwargs)
		self.__class__.JML = JmlIterasi
		self.start_urls = ['https://play.google.com']
	
	def parse(self, response):
		headers_data = {
			'accept' : '*/*',
			'accept-encoding' : 'gzip, deflate, br',
			'accept-language' : 'en-US,en;q=0.5',
			'connection' : 'keep-alive',
			'content-type' :  'application/x-www-form-urlencoded;charset=utf-8',
			'origin' : 'https://play.google.com',
			'DNT' : '1',
			'Host' : 'play.google.com',
			'referer' : 'https://play.google.com/store/apps/details?id=' + self.NamaPackage,
			'user-agent'	: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
			'X-Same-Domain' : '1'
		}
		form_data = {
			'reviewType' : '0',
			'pageNum' : '0',
			'id' : self.NamaPackage,
			'reviewSortOrder' : '2',
			'xhr' : '1'
		}
		yield scrapy.http.FormRequest(
			url='https://play.google.com/store/getreviews?authuser=0',
			method = 'POST',
			headers=headers_data,
			formdata=form_data,
			callback=self.parseReview
		)
		
	def parseReview(self, response):
		hasil = response.body
		hasil = hasil.replace('\\u003d\\', '=')
		hasil = hasil.replace('\\u003c', '<')
		hasil = hasil.replace('\\u003e', '>')
		hasil = hasil.replace('\\"', '"')
		hasil = hasil.replace('[["ecr",1," ', '')
		hasil = hasil.replace(' ",1]', '')
		hasil = hasil.replace(")]}'", "<html><body>")
		hasil = hasil.replace("]", "</body></html>")
		hasil = hasil.decode('unicode_escape').encode('ascii','ignore')
		hasil = hasil.replace('\\', '')
		hasil = hasil.replace('\n', '')
		xxx = response.replace(body=hasil)
		x = 1
		y = 0
		while(x <= 118):
			#untuk training
			try:
				rating = int(xxx.css('.review-info-star-rating>.tiny-star::attr(aria-label)')[y].extract()[7:][:1])
			except:
				rating = 0;
			komentar = xxx.css('.review-body::text')[x].extract()[:-1][1:]
			if len(komentar) >= 70 and rating==5:
				bahasa = detect(komentar)
				if bahasa ==  'en':				
					#---------------------------------------------------------------------------------------------------------------------------end
					yield {
						'Text Review' : xxx.css('.review-body::text')[x].extract()[:-1][1:],
						'Tanggal' : xxx.css('.review-date::text')[y].extract(),
						'Nama User' : xxx.css('.review-info>.author-name::text')[y].extract()[:-1][1:],
						'Rating' : xxx.css('.review-info-star-rating>.tiny-star::attr(aria-label)')[y].extract()[7:][:1]
					}
			x = x + 3
			y = y + 1
		self.__class__.JML = int(self.__class__.JML) - 1
		print "JML = %s" % self.__class__.JML
		if (int(self.__class__.JML) != 0):
			self.__class__.indeks = int(self.__class__.indeks) + 1
			headers_data = {
				'accept' : '*/*',
				'accept-encoding' : 'gzip, deflate, br',
				'accept-language' : 'en-US,en;q=0.5',
				'connection' : 'keep-alive',
				'content-type' :  'application/x-www-form-urlencoded;charset=utf-8',
				'origin' : 'https://play.google.com',
				'DNT' : '1',
				'Host' : 'play.google.com',
				'referer' : 'https://play.google.com/store/apps/details?id=' + self.NamaPackage,
				'user-agent'	: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
				'X-Same-Domain' : '1'
			}
			form_data = {
				'reviewType' : '0',
				'pageNum' : str(self.__class__.indeks),
				'id' : self.NamaPackage,
				'reviewSortOrder' : '2',
				'xhr' : '1'
			}
			yield scrapy.http.FormRequest(
				url='https://play.google.com/store/getreviews?authuser=0',
				method = 'POST',
				headers=headers_data,
				formdata=form_data,
				callback=self.parseReview
			)
			
			
#str.decode('unicode_escape').encode('ascii','ignore')    <== matikan unicode
#sorting: 0: terbaru, 2: paling berguna/bermanfaat