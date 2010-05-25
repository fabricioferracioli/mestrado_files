# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# primeiro script a rodar, recebe o arquivo de log bruto como entrada e configurações

import logfilter
from optparse import OptionParser
usage = 'usage: %prog -i inputfilepath [options]'
parser = OptionParser(usage)

parser.add_option('-i', '--input', dest='inputfile', help='read the FILE as input', metavar='FILE')
parser.add_option('-c', '--config', dest='configfile', help='FILE with the configurations for the filter', metavar='FILE')
parser.add_option('-f', '--force', dest='forcedbcreation', action='store_true', help='Reset previous databases created', default=False)

(options, args) = parser.parse_args()

if options.inputfile == options.configfile:
    parser.error('the options for input (-i) and config (-c) files cannot be equal')
if options.inputfile == None:
    parser.error('please, inform a path for the input log file')
if options.configfile == None:
    parser.error('please, inform a path for the config file')

lf = logfilter.LogFilter(options.configfile)
initial_filter_results = lf.initialFilter(options.inputfile)

print '-- Initial Filter --'
print '- Lines excluded: %d' %initial_filter_results['excluded']
print '- Lines included: %d' %initial_filter_results['included']

lf.filterUrls()

print '-- Urls Filter finished --'

lf.filterTasks()

print '-- Tasks Filter finished --'

lf.itentifyTasks(options.forcedbcreation)

print '-- Tasks Identified --'

lf.sessions()

print '-- Sessions identified --'