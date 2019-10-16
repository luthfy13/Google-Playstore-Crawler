import os,re,json
from flask import Flask, jsonify, request


if __name__ == '__main__':
	query = "scrapy crawl AppName -a KataKunci=tokopedia -o hasil.json"
	os.system(query)
	with open('hasil.json') as data_file:
		data = json.load(data_file)
	os.system("cls")
	print data[0]['Nama App']