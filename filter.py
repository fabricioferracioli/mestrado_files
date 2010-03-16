# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# primeiro script a rodar, recebe o arquivo de log bruto como entrada

from optparse import OptionParser
usage = 'usage: %prog -i inputfilepath [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-i', '--input', dest='inputfile', help='read the FILE as input', metavar='FILE')
parser.add_option('-o', '--output', dest='outputfile', help='write filtered log in the FILE. if not specified, the default is %default', metavar='FILE', default='output.log')
(options, args) = parser.parse_args()

if options.inputfile == options.outputfile:
    parser.error('the options for input (-i) and output (-o) files cannot be equal')
if options.inputfile == None:
    parser.error('please, inform a path for the input log file')

extensions_to_exclude = ['.gif', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.css', '.js']
lines_included = 0
lines_excluded = 0

inputlogfile = open(options.inputfile, 'r')
outputlogfile = open(options.outputfile, 'w')

for line in inputlogfile:
    include_line = True
    for extension in extensions_to_exclude:
        if line.find(extension) != -1:
            lines_excluded += 1
            include_line = False
            break
    else:
        if (include_line):
            outputlogfile.write(line)
            lines_included += 1
inputlogfile.close()
outputlogfile.close()
print 'lines excluded: %d' %lines_excluded
print 'lines included: %d' %lines_included
print 'total lines: %d' %(lines_excluded + lines_included)