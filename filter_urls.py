# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# segundo script a rodar, recebe a saida do primeiro e um arquivo com as urls que deve procurar. receives two input files, one is a filtered web server log file and another the urls that will be filtered defined by user

def isInGroup(searchFor, inGroup):
    for index in range(len(inGroup)):
        if searchFor.find(inGroup[index]) >= 0:
            return True
    return False

from optparse import OptionParser
import re
usage = 'usage: %prog -l input_log_file_path -u input_urls -b base_url [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-l', '--log', dest='logfile', help='read the LOGFILE as input log file', metavar='LOGFILE')
parser.add_option('-u', '--urls', dest='urlsfile', help='urls to be filtered URLFILE', metavar='URLFILE')
#parser.add_option('-b', '--baseurl', dest='base_url', help='base url BASEURL used as prefix to all urls to be filtered', metavar='BASEURL')
(options, args) = parser.parse_args()

if options.logfile == None:
    parser.error('please, inform a path for the logfile')
if options.urlsfile == None:
    parser.error('please, inform a path for the input log file')
if options.logfile == options.urlsfile:
    parser.error('the logfile (-l) and the urlsfile (-u) cannot be equal')
#if options.base_url == None:
    #parser.error('please, inform the base url')

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
            #pattern = re.compile('.*'+initial_urls[index]+'.*')
            if line.find(initial_urls[index]) >= 0:
                index_tested = index
                num_searches += 1
                include_line = True
                outputfile.write(line)
                break
    else:
        #end_pattern = re.compile('.'+final_urls[index_tested]+'.*')
        if num_searches <= max_req_between_urls[index_tested]:
            if isInGroup(line, initial_urls) == True:
                num_searches = 1
            outputfile.write(line)
            num_searches += 1
            if line.find(final_urls[index_tested]) >= 0:
                include_line = False
        else:
            if isInGroup(line, initial_urls) == True:
                outputfile.write(line)
            include_line = False
logfile.close()
outputfile.close()