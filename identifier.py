# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#identificador de usuarios, paginas e reconhecimento de acessos (sessoes)
#recebe como parametro o arquivo com as urls a serem filtradas pois ele possui os nomes dos arquivos gerados com as urls ja filtradas

from optparse import OptionParser
import logutil, mining_database

usage = 'usage: %prog -i input_file_path [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-i', '--input', dest='inputfile', help='read the INPUTFILE as parameters defined by user to access the correct filtered logfiles', metavar='INPUTFILE')
(options, args) = parser.parse_args()


if options.inputfile == None:
    parser.error('please, inform a path for the input file')

logfiles = []
inputfile = open(options.inputfile, 'r')
for line in inputfile:
    logfiles.append(line.split()[3])
inputfile.close()

lu = logutil.LogUtil()
db = mining_database.MiningDatabase()
db.createTables()

for logfilepath in logfiles:
    logfile = open(logfilepath, 'r')
    for line in logfile:
        requester = lu.getRequester(line)
        if len(db.searchUser('ip', 'like', requester).fetchall()) == 0:
            db.insertUser(requester)

        document_requested = lu.getRequestedDocument(line)
        if len(db.searchPage('page', 'like', document_requested).fetchall()) == 0:
            db.insertPage(document_requested)

        request_date = lu.getRequestDate(line)
        server_response_status = lu.getServerResponseStatus(line)
        response_size = lu.getResponseSize(line)

        db.insertAccess(requester, document_requested, request_date, server_response_status, response_size)

inputfile = open(options.inputfile, 'r')
for line in inputfile:
    conf = line.split()
    print 'inserting config %s, %s, %s, %s'%(conf[0], conf[1], conf[2], conf[3])
    db.insertConfig(conf[0], conf[1], conf[2], conf[3])
inputfile.close()