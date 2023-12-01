import sqlite3

class DataAccessObject:
    connection = sqlite3.Connection("./db.sqlite3", check_same_thread=False)
    cursor = connection.cursor()
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataAccessObject, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # Создаем таблицу Users
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ScrapingDataBase (
        name TEXT PRIMARY KEY NOT NULL,
        price INTEGER NOT NULL,
        photo_url TEXT NOT NULL,
        url TEXT NOT NULL,
        sale INTEGER NOT NULL,
        new TEXT
        )
        ''')
        self.connection.commit()

    def insert(self, name, price, photo_url, url, sale, new):
        if new != ' ':
            self.cursor.execute('INSERT or REPLACE INTO ScrapingDataBase (name, price, photo_url, url, sale, new) VALUES (?, ?, ?, ?, ?, ?)', (name, int(price), photo_url, url, int(sale), new))
        else:
            self.cursor.execute('INSERT or REPLACE INTO ScrapingDataBase (name, price, photo_url, url, sale, new) VALUES (?, ?, ?, ?, ?, NULL)', (name, int(price), photo_url, url, int(sale)))
        self.connection.commit()

    def find_concrete_cube(self, criteria):
        self.cursor.execute(f'SELECT * FROM ScrapingDataBase WHERE ? IN name', (criteria, ))

    def find_concrete_cube_by_price(self, price_min, price_max):
        self.cursor.execute(f'SELECT * FROM (SELECT * FROM ScrapingDataBase WHERE price BETWEEN {int(price_min)} AND {int(price_max)}) GROUP BY price')
        #self.cursor.execute('SELECT name, price,  FROM ScrapingDataBase ORDER BY price')
        return self.cursor.fetchall()

    def get_max_cube(self):
        self.cursor.execute('SELECT name, max(price), photo_url, url, sale FROM ScrapingDataBase')
        return self.cursor.fetchall()
    
    def find_sale_cube(self):
        self.cursor.execute(f'SELECT * FROM ScrapingDataBase WHERE sale != {0}')
        return self.cursor.fetchall()
    
    def find_new_cube(self):
        self.cursor.execute(f'SELECT * FROM ScrapingDataBase WHERE new IS NOT NULL ')
        return self.cursor.fetchall()

    def fetchall(self):
        self.cursor.execute('SELECT * FROM ScrapingDataBase')
        return self.cursor.fetchall()