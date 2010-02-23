# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#recebe o arquivo com as tarefas desejadas e separa as tarefas
#o arquivo de entrada com as tarefas é o mesmo utilizado no filter_urls, mas utiliza o ultimo parametro da linha

from optparse import OptionParser

def findUrlInLogLine(line):
    begin = line.index('"')
    end = line.rindex('"')
    return line[begin:end].split()[1]

def findActualTask(tasks, line):
    for i in range(len(tasks)):
        if line.find(tasks[i]['initial_url']) != -1:
            return i
    return None

def isInitialUrl(line, tasks):
    for task in tasks:
        if line.find(task['initial_url']) != -1:
            return True
    return False

def isFinalUrl(line, tasks):
    for task in tasks:
        if line.find(task['final_url']) != -1:
            return True
    return False

usage = 'usage: %prog -l tasks_log_file_path -t tasks_urls [options]'
parser = OptionParser(usage)
#optionparser sempre assume que a opcao sera do tipo string e que deve armazenar em dest
parser.add_option('-l', '--log', dest='logfile', help='read the LOGFILE as input with urls accesed by users, outputed by filter_urls', metavar='LOGFILE')
parser.add_option('-t', '--tasks', dest='tasksfile', help='urls from the taks to be separated URLFILE', metavar='URLFILE')
(options, args) = parser.parse_args()

if options.logfile == None:
    parser.error('please, inform a path for the log file')
if options.tasksfile == None:
    parser.error('please, inform a path for the tasks file')
if options.logfile == options.tasksfile:
    parser.error('the logfile (-l) and the urlsfile (-u) cannot be equal')

##le o arquivo de tarefas no formato [url_inicial url_final requisicoes_maximas_entre_urls nome_tarefa]
tasks_file = open(options.tasksfile, 'r')
tasks = []
for line in tasks_file:
    params = line.split()
    tasks.append({'id': params[3], 'initial_url': params[0], 'final_url': params[1], 'max_requisitions': params[2]})
tasks_file.close()

logfile = open(options.logfile, 'r')
num_searches = 0
task_index = 0
for line in logfile:
    if isInitialUrl(line, tasks):
        if task_index == -1:
            outputfile.close()
        task_index = findActualTask(tasks, line)
        outputfile = open(tasks[task_index]['id'], 'a')
        outputfile.write(line)
        num_searches = 1
    else:
        if num_searches <= int(tasks[task_index]['max_requisitions']):
            num_searches += 1
            if isFinalUrl(line, tasks):
                task_index = -1
                num_searches = 0
            outputfile.write(line)
outputfile.close()