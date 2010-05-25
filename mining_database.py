# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#funcoes para manipulação do banco de dados que sera utilizado para clusterizacao
import sqlite3

class MiningDatabase:

    def __init__(self, forceCreation = False):
        self.connection = sqlite3.connect('mining.db')
        if forceCreation == True:
            self.connection.execute('drop table if exists access')
            self.connection.execute('drop table if exists configs')
            self.connection.execute('drop table if exists users')
            self.connection.execute('drop table if exists pages')

    def createTables(self):
        tables = {
            'users': 'create table if not exists users (id integer primary key autoincrement, ip text unique)',
            'pages': 'create table if not exists pages (id integer primary key autoincrement, page text unique)',
            'access': 'create table if not exists access (id integer primary key autoincrement, page_id integer, user_id integer, request_date text, response_status integer, response_size integer, foreign key(page_id) references pages(id), foreign key (user_id) references users(id))',
            'configs': 'create table if not exists configs (id integer primary key autoincrement, initial_page_id integer, final_page_id integer, max_urls integer, task_name text, foreign key (initial_page_id) references pages(id), foreign key (final_page_id) references pages(id))'
        }
        for table in tables:
            self.connection.execute(tables[table])
            print 'table '+ table +' sucessfully created'

    def insertUser(self, ip):
        self.connection.execute('insert into users(ip) values (?)', [ip])
        self.connection.commit()

    def searchUser(self, findBy, operator, findValue):
        return self.connection.execute('select * from users where '+findBy+' '+operator+' (?) ', [findValue])

    def insertPage(self, page):
        try:
            self.connection.execute('insert into pages(page) values (?)', [page])
            self.connection.commit()
        except sqlite3.IntegrityError:
            print 'Pagina ja inserida'

    def searchPage(self, findBy, operator, findValue):
        return self.connection.execute('select * from pages where '+findBy+' '+operator+' (?) ', [findValue])

    def insertAccess(self, userIp, page_path, request_date, response_status, response_size):
        user = self.searchUser('ip', 'LIKE', userIp)
        page = self.searchPage('page', 'LIKE', page_path)

        user_id = user.fetchall()[0][0]
        page_id = page.fetchall()[0][0]

        request_date = self.normalizeDate(request_date)
        self.connection.execute('insert into access(page_id, user_id, request_date, response_status, response_size) values (?, ?, ?, ?, ?)', [page_id, user_id, request_date, response_status, response_size])
        self.connection.commit()

    def insertConfig(self, initialPage, finalPage, maxUrls, taskName):
        initial_page = self.searchPage('page', 'like', initialPage)
        final_page = self.searchPage('page', 'like', finalPage)
        self.connection.execute('insert into configs (initial_page_id, final_page_id, max_urls, task_name) values (?, ?, ?, ?)', [initial_page.fetchall()[0][0], final_page.fetchall()[0][0], maxUrls, taskName])
        self.connection.commit()

    def searchConfig(self, findBy, operator, findValue):
        return self.connection.execute('select * from configs where '+findBy+' '+operator+' (?) ', [findValue])

    def normalizeDate(self, date):
        month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        date = date.replace('/', '-')
        date = date.replace(date.split('-')[1], month[date.split('-')[1]])
        date = date[0:date.find(' ')]
        date = date.replace(':', ' ', 1)
        return date

    def customQuery(self, query):
        return self.connection.execute(query)

    def teste():
        first_access = self.connection.execute('select min(id) from access')
        access = self.connection.execute('select * from access where id = (?)', [first_access.fetchone()[0]])

    def __del__(self):
        self.connection.close()