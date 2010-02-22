# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#receives two input files, one is a filtered web server log file and another the urls that will be filtered defined by user

from optparse import OptionParser
import re
usage = 'usage: %prog -l input_log_file_path -u input_urls -b base_url [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-l', '--log', dest='logfile', help='read the LOGFILE as input log file', metavar='LOGFILE')
parser.add_option('-u', '--urls', dest='urlsfile', help='urls to be filtered URLFILE', metavar='URLFILE')
parser.add_option('-b', '--baseurl', dest='base_url', help='base url BASEURL used as prefix to all urls to be filtered', metavar='BASEURL')
(options, args) = parser.parse_args()

if options.logfile == None:
    parser.error('please, inform a path for the logfile')
if options.urlsfile == None:
    parser.error('please, inform a path for the input log file')
if options.logfile == options.urlsfile:
    parser.error('the logfile (-l) and the urlsfile (-u) cannot be equal')
if options.base_url == None:
    parser.error('please, inform the base url')

#initial urls from the tasks to be filtered
initial_urls = []
#final urls from the tasks to be filtered
final_urls = []
#max requisition between urls, avoiding umcompleted tasks
max_req_between_urls = []

urlsfile = open(options.urlsfile, 'r')
for line in urlsfile:
    splitted_line = line.split()
    initial_urls.append(splitted_line[0])
    final_urls.append(splitted_line[1])
    max_req_between_urls.append(int(splitted_line[2]))
urlsfile.close()

logfile = open(options.logfile, 'r')
outputfile = open('urls_output.log', 'w')

index_tested = 0
num_searches = 0
include_line = False
for line in logfile:
    if include_line == False:
        num_searches = 0
        for index in range(len(initial_urls)):
            pattern = re.compile('.*\s/'+options.base_url+'.*/'+initial_urls[index]+'.*')
            if pattern.match(line):
                index_tested = index
                num_searches += 1
                include_line = True
                outputfile.write(line)
                break
    else:
        print 'gravando para %s'%initial_urls[index_tested]
        print 'buscando %s vezes'%final_urls[index_tested]
        print 'buscas realizadas %d'%num_searches
        print 'maximo a buscar %s'%max_req_between_urls[index_tested]
        pattern = re.compile('.*\s/'+options.base_url+'.*/'+final_urls[index_tested]+'.*')
        if num_searches <= max_req_between_urls[index_tested]:
            outputfile.write(line)
            num_searches += 1
            if pattern.match(line):
                include_line = False
        else:
            include_line = False
logfile.close()
outputfile.close()