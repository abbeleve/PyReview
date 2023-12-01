import requests
from bs4 import BeautifulSoup
from DataBase import DataAccessObject

#from telegram_bot import Bot
import random


class Menu:
    def __init__(self):
        self.__url = 'https://cubemarket.ru/catalog/kubiki-rubika'
        self.__response = requests.get(self.__url)
        self.__data = BeautifulSoup(self.__response.text, 'html.parser')
        self.__dao = DataAccessObject()

    def parsing_rubiks_cubes(self):
        items = self.__data.find_all('div', class_='item')
        for card in items:
            name = card.find("p", class_='item_name').text
            price = card.find('p', class_='item_price').text.replace(' ', '')
            if '%' in price:
                sale = price[:price.find('%')]
            else:
                sale = 0
            price = price[price.find('%') + 1:]
            photo_url = card.find('img').get("src")
            url = card.find('a').get("href")
            url = 'https://cubemarket.ru' + url
            if card.find('span').text == 'Новинка':
                new = card.find('span').text
            else:
                new = ' '
            print(card.find('span').text, new)
            DataAccessObject().insert(name, price, photo_url, url, sale, new)

    #def output(self, new_result):
        #for stroke in new_result:
            #print(f"Наименование: {stroke[0]}. Стоимость товара: {stroke[1]}, URL Фото: {stroke[2]}, URL: {stroke[3]}, Скидка: {stroke[4]}")

    def make_output(self, arr):
        return f"Наименование: {arr[0][0]}. Стоимость товара: {arr[0][1]}, URL Фото: {arr[0][2]}, URL: {arr[0][3]}, Скидка: {arr[0][4]}"

    def get_concrete_cube(self, criteria):
        temp = self.__dao.fetchall()
        save = []
        for item in temp:
            if criteria in item[0]:
                save.append(item)
        return save

    def get_max_cube(self):
        sales = self.__dao.get_max_cube()
        return f'''Наименование: {sales[0][0]}, Цена: {sales[0][1]}, Скидка: {-1*(sales[0][4])} %, Ссылка: {sales[0][3]}\n'''

    def get_concrete_cube_by_price(self, price_min, price_max):
        return self.__dao.find_concrete_cube_by_price(price_min, price_max)
    
    def get_sales(self):
        sales = self.__dao.find_sale_cube()
        stroke = ''
        for i in range(0, len(sales)):
            stroke += f'''Наименование: {sales[i][0]}, Цена: {sales[i][1]}, Скидка: {-1*(sales[i][4])} %, Ссылка: {sales[i][3]}\n'''
        return stroke
    
    def get_new(self):
        new = self.__dao.find_new_cube()
        stroke = ''
        for i in range(0, 2):
            stroke += f'''Новинка: Наименование: {new[i][0]}, Цена: {new[i][1]}, Скидка: {-1*(new[i][4])} %, Ссылка: {new[i][3]}\n'''
        return stroke

    def set_url(self, url):
        self.__url = url

    def refresh_data(self):
        self.__data = BeautifulSoup(self.__response.text, 'html.parser')

    def refresh_response(self):
        self.__response = requests.get(self.__url)

    def go_to_new_page(self, url):
        self.set_url(url)
        self.refresh_response()
        self.refresh_data()

    def get_url(self):
        return self.__url

    def get_response(self):
        return self.__response

    def get_html_text(self):
        return BeautifulSoup(self.get_response().text, 'html.parser')
    
    def refresh_information_about_cubes(self):
        self.go_to_new_page("https://cubemarket.ru/catalog/kubiki-rubika")
        self.parsing_rubiks_cubes()
        self.go_to_new_page("https://cubemarket.ru/catalog/kubiki-rubika?page=2")
        self.parsing_rubiks_cubes()
        self.go_to_new_page("https://cubemarket.ru/catalog/kubiki-rubika?page=3")
        self.parsing_rubiks_cubes()

    def refresh_information_about_sales(self):
        self.go_to_new_page("https://cubemarket.ru/catalog/novinki")
        self.parsing_rubiks_cubes()

menu = Menu()
print('-')