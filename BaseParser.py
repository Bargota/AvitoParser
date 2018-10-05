import requests



class Parser():
	def __init__(base_url):
		self.base_url=base_url

	def GetHTMLText(self):
		try:
			r=requests.get(self.base_url)
		except:
			return ''
		return r.text

	def GetTotalPages(self,html):
		soup = BeautifulSoup(html)
		tmp_pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		#total_pages = tmp_pages.split('=')[1]
		total_pages = tmp_pages.split('=')[1].split('&')[0]
		return int(total_pages)

	def TakeData(self, ads):
		list=[]
		for ad in ads:
			title=FindTitle()
			address=FindAddress()
			price=FindPrice()
			area=FindArea()
			price_m2=round(price/area)

			dict_ad = {'title':title,
                        'price':price,
                        'price_m2':price_m2,
                        'address':address,
                        'urlad':url_ad,
                        'area':area,
                        'floors':floors,
                        'date_ad':date_ad,
                        #'type_house':type_house}
                        }
			list.append(dict_ad)
		return list
		

	def FindTitle(self):
		return title
		

	def FindAddress(self):
		return address
		

	def FindPrice(self):
		return price
		pass

	def FindArea(self):
		return area
		pass