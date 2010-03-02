# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#identificador de usuarios, paginas e reconhecimento de acessos (sessoes)
#recebe como parametro o arquivo com as urls a serem filtradas pois ele possui os nomes dos arquivos gerados com as urls ja filtradas

from optparse import OptionParser
import logutil, sqlite3

usage = 'usage: %prog -i input_file_path [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-i', '--input', dest='inputfile', help='read the INPUTFILE as parameters defined by user to access the correct filtered logfiles', metavar='INPUTFILE')
(options, args) = parser.parse_args()


if options.inputfile == None:
    parser.error('please, inform a path for the input file')


users = []
pages = []
access = []
logfiles = []

def isInUsers(userIP):
    for u in users:
        if u['ip'] == userIP:
            return True
    return False

def findUserBy(key, value):
    for u in users:
        if u[key] == value:
            return u
    return None

def isInPages(page):
    for p in pages:
        if p['page'] == page:
            return True
    return False

def findPageBy(key, value):
    for p in pages:
        if p[key] == value:
            return p
    return None

inputfile = open(options.inputfile, 'r')
for line in inputfile:
    logfiles.append(line.split()[3])

lu = logutil.LogUtil()

for logfilepath in logfiles:
    logfile = open(logfilepath, 'r')
    for line in logfile:
        requester = lu.getRequester(line)
        if isInUsers(requester) == False:
            users.append({'id': len(users)+1, 'ip': requester})

        document_requested = lu.getRequestedDocument(line)
        if isInPages(document_requested) == False:
            pages.append({'id': len(pages)+1, 'page': document_requested})

        request_date = lu.getRequestDate(line)
        server_response_status = lu.getServerResponseStatus(line)
        response_size = lu.getResponseSize(line)

        access.append({'id': len(access)+1, 'page_id': findPageBy('page', document_requested)['id'], 'user_id': findUserBy('ip', requester)['id'], 'request_date': request_date, 'response_status': server_response_status, 'response_size': response_size}),

for line in inputfile:
    conf = line.split()
    config['initial_url'] = findPageBy('page', conf[0])
    config['final_url'] = findPageBy('page', conf[1])
    config['max_urls'] = conf[2]
    config['task_name'] = conf[3]
inputfile.close()

con = sqlite3.connect('database.sql')
con.execute('create database users (id integer primary key, ip text)')
con.execute('create database pages (id integer primary key, page text)')
con.execute('create database access (id integer primary key, page_id integer foreign key(page_id) references pages(id), user_id integer foreign key (user_id) references users(id), time datetime)')
con.execute('create database configs (id interger primary key, initial_page_id integer foreign key(initial_page_id) references pages(id), final_page_id integer foreign key (final_page_id) references pages(id), max_urls integer, task_name text)')