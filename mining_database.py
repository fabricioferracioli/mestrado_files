# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#funcoes para manipulação do banco de dados que sera utilizado para clusterizacao
import sqlite3

class MiningDatabase:

    def __init__(self):
        self.connection = sqlite3.connect('mining.db')

    def createTables(self):
        tables = {
            'users': 'create table users (id integer primary key, ip text)',
            'pages': 'create table pages (id integer primary key, page text)',
            'access': 'create table access (id integer primary key, page_id integer, user_id integer, request_date text, response_status integer, response_size integer, foreign key(page_id) references pages(id), foreign key (user_id) references users(id))',
            'configs': 'create table configs (id integer primary key, initial_page_id integer, final_page_id integer, max_urls integer, task_name text, foreign key (initial_page_id) references pages(id), foreign key (final_page_id) references pages(id))'
        }
        for table in tables:
            self.connection.execute(tables[table])
            print 'table '+ table +' sucessfully created'

    def insertUser(self, ip):
        self.connection.execute('insert into users(ip) values (?)', [ip])

    def searchUser(self, findBy, operator, findValue):
        return self.connection.execute('select * from users where '+findBy+' '+operator+' ? ', [findValue])

    def insertPage(self, page):
        self.connection.execute('insert into pages(page) values (?)', page)

    def findPage(self, findBy, operator, findValue):
        return self.connection.execute('select * from pages where '+findBy+' '+operator+' '+findValue)

    def __del__(self):
        self.connection.close()