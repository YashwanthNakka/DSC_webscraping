from bs4 import BeautifulSoup #this code takes input value from user regarding how many categories to e scraped
import requests,re,csv,os
os.mkdir('DSC_webscraping_task')
os.chdir('DSC_webscraping_task')
os.mkdir('book_images')

def f1(url):                #function to write csv file and download images
	source_for_url=requests.get(url).text
	soup_3=BeautifulSoup(source_for_url,'lxml')
	Category=soup_3.h1.getText()
	f=open(Category+'.csv','a',encoding='utf-8')
	f_writer=csv.writer(f)
	if os.stat(Category+'.csv').st_size==0 :
		f_writer.writerow(['Name_of_the_book','Rating','Price','Availabilty'])	
	all_books=open('file_containing_details_of_all_books.csv','a',encoding='utf-8')
	all_books_writer=csv.writer(all_books)
	if os.stat('File_containing_details_of_all_books.csv').st_size==0 :
		all_books_writer.writerow(['Category','Name_of_the_book','Rating','Price','Availabilty'])
	os.chdir('book_images')
	if not os.path.exists(Category):    #checks if the url received to this functon is of previous category or not
		#if it is of previous category, it just appends
		os.mkdir(Category)
		os.chdir(Category)
	else:		
		os.chdir(Category)
	for details_of_books in soup_3.section.findAll('article'):
		Name_of_the_book=details_of_books.a.img.get('alt')[:20]+details_of_books.a.img.get('alt')[-10:]
		Name_of_the_book = re.sub('[\\W]','_',Name_of_the_book)
		Rating=details_of_books.p.get('class')[1]+' stars'
		Price=details_of_books.find('div',class_='product_price').p.getText()[1:]		
		Availability=details_of_books.find('p',class_='instock availability').getText().strip()		
		url_of_the_image=home_page[:26]+details_of_books.img.get('src')[11:]	
		all_books_writer.writerow([Category,Name_of_the_book,Rating,Price,Availability])
		f_writer.writerow([Name_of_the_book,Rating,Price,Availability])
		with open(Name_of_the_book+'.jpg','wb') as file:
			source_for_url_of_image=requests.get(url_of_the_image)
			file.write(source_for_url_of_image.content)			
	os.chdir("..")		
	os.chdir("..")   
 
home_page='https://books.toscrape.com/index.html'
source = requests.get(home_page).text
soup=BeautifulSoup(source,'lxml')
num_of_categories_to_be_scraped=int(input("num_of_categories_to_be_scraped: "))    ##### maximum =50 categories possible
Categories_of_books=soup.find('div',class_='side_categories')
for a_tag in Categories_of_books.li.ul.find_all('a',limit=num_of_categories_to_be_scraped):
	complete_url_of_category=home_page[:27]+a_tag.get('href')
	f1(complete_url_of_category)
	complete_url_of_category=complete_url_of_category.replace('index','page-2')
	source_for_next_page_of_category=requests.get(complete_url_of_category).text
	soup_2=BeautifulSoup(source_for_next_page_of_category,'lxml')
	check_404_in_pages=soup_2.h1.getText()
	if not check_404_in_pages=='404 Not Found':
		f1(complete_url_of_category)               
	# from page 2 onwards checks if the page is empty or not and then only it calls f1 for writing csv files and downloading images
	for x in range(3,8):
		complete_url_of_category=complete_url_of_category[:-11]+f'page-{x}'+'.html'
		source_for_next_page_of_category=requests.get(complete_url_of_category).text
		soup_2=BeautifulSoup(source_for_next_page_of_category,'lxml')
		check_404_in_pages=soup_2.h1.getText()
		if not check_404_in_pages=='404 Not Found':
			f1(complete_url_of_category)
		else:
			break	
		

		