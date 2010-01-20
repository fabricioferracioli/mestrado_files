# -*- coding: utf-8 -*-
#!/usr/bin/pyhton

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

inputlogfile = open(options.inputfile, 'r')
for line in inputlogfile:
    print line