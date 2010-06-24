# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# script geral do filtro

import logutil, mining_database, datetime

class LogFilter:

    def __init__(self, configFile):
        self.extensionsToExclude = ['.gif', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.css', '.js']
        self.configFile = configFile

    def isInGroup(self, searchFor, inGroup):
        for index in range(len(inGroup)):
            if searchFor.find(inGroup[index]) >= 0:
                return True
        return False

    def findUrlInLogLine(self, line):
        begin = line.index('"')
        end = line.rindex('"')
        return line[begin:end].split()[1]

    def findActualTask(self, tasks, line):
        for i in range(len(tasks)):
            if line.find(tasks[i]['initial_url']) != -1:
                return i
        return None

    def isInitialUrl(self, line, tasks):
        for task in tasks:
            if line.find(task['initial_url']) != -1:
                return True
        return False

    def isFinalUrl(self, line, tasks):
        for task in tasks:
            if line.find(task['final_url']) != -1:
                return True
        return False

    def timeBetweenRequests(self, firstAccess, secondAccess):
        fd = firstAccess.split()[0].split('-')
        ft = firstAccess.split()[1].split(':')

        fdt = datetime.datetime(int(fd[2]), int(fd[1]), int(fd[0]), int(ft[0]), int(ft[1]), int(ft[2]))

        sd = secondAccess.split()[0].split('-')
        st = secondAccess.split()[1].split(':')

        stf = datetime.datetime(int(sd[2]), int(sd[1]), int(sd[0]), int(st[0]), int(st[1]), int(st[2]))
        return stf - fdt

    def reachMaxIdleTime(self, firstAccessTime, secondAccessTime):
        #20 minutos
        return self.timeBetweenRequests(firstAccessTime, secondAccessTime) > datetime.timedelta(0,0,0,0,20)

    def userCompletedTheTask(self, urlSequence, initialAccess, taskConfigs):
        line = str(initialAccess[1])
        for i in range(len(urlSequence)):
            #verifico se ele abortou e comecou qualquer outra tarefa
            for config in taskConfigs:
                if (urlSequence[i][1] == config[1]):
                    print 'outra tarefa foi iniciada'
                    return False
            #agora devo verificar o tempo de acesso entre duas urls (atual - anterior)

            startNewSession = False
            if (i == 0):
                startNewSession = self.reachMaxIdleTime(initialAccess[3], urlSequence[i][3])
            else:
                startNewSession = self.reachMaxIdleTime(urlSequence[i-1][3], urlSequence[i][3])

            if (startNewSession == False):
                line = line + ' ' + str(urlSequence[i][1])
            else:
                #as urls depois de expirada a sessao sao ignoradas
                print 'sessao expirada'
                return line
        return line

    def normalizeLine(self, line, maxUrls, withTime = False):
        if withTime == True:
            if len(line.split()) < maxUrls * 2:
                line = line + (maxUrls*2 - len(line.split())) * ' 0 :00'
        else:
            if len(line.split()) < maxUrls:
                #precisa ser -1 pois o somtoolbox reconhece esse valor como null
                line = line + (maxUrls - len(line.split())) * ' -1'
        return line

    def initialFilter(self, logFile, filteredLog = 'output.log'):
        if (logFile == None):
            raise Exception('WrongParameter', 'The logFile must be specified.')
        if (logFile == filteredLog):
            raise Excetion('WrongParameter', 'The values of arguments are equal. Please, set different values.')

        lines_included = 0
        lines_excluded = 0

        inputlogfile = open(logFile, 'r')
        outputlogfile = open(filteredLog, 'w')

        for line in inputlogfile:
            include_line = True
            for extension in self.extensionsToExclude:
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
        return {'excluded': lines_excluded, 'included': lines_included}

    def filterUrls(self, logFile = 'output.log'):
        if (logFile == None):
            raise Exception('WrongParameter', 'logFile parameter must be a valid path to a filtered log file')
        if (self.configFile == logFile):
            raise ('WrongParameter', 'The two arguments must be different.')

        #initial and final urls from the tasks to be filtered, max requisition between urls, avoiding umcompleted tasks
        initial_urls = []
        final_urls = []
        max_req_between_urls = []

        urlsfile = open(self.configFile, 'r')
        for line in urlsfile:
            splitted_line = line.split()
            initial_urls.append(splitted_line[0])
            final_urls.append(splitted_line[1])
            max_req_between_urls.append(int(splitted_line[2]))
        urlsfile.close()

        logfile = open(logFile, 'r')
        outputfile = open('urls_output.log', 'w')

        index_tested = 0
        num_searches = 0
        include_line = False
        for line in logfile:
            if include_line == False:
                num_searches = 0
                for index in range(len(initial_urls)):
                    if line.find(initial_urls[index]) >= 0:
                        index_tested = index
                        num_searches += 1
                        include_line = True
                        outputfile.write(line)
                        break
            else:
                if num_searches <= max_req_between_urls[index_tested]:
                    if self.isInGroup(line, initial_urls) == True:
                        num_searches = 1
                    outputfile.write(line)
                    num_searches += 1
                    if line.find(final_urls[index_tested]) >= 0:
                        include_line = False
                else:
                    if self.isInGroup(line, initial_urls) == True:
                        outputfile.write(line)
                    include_line = False
        logfile.close()
        outputfile.close()
        return True

    def filterTasks(self, filteredUrlsFile = 'urls_output.log'):
        if (filteredUrlsFile == None):
            raise Exception('WrongParameter', 'You must specify a log file with the filtered urls')
        if (self.configFile == filteredUrlsFile):
            raise Exception('WrongParameter', 'The config and filtered urls file must be different')

        tasks_file = open(self.configFile, 'r')
        tasks = []
        for line in tasks_file:
            params = line.split()
            tasks.append({'id': params[3], 'initial_url': params[0], 'final_url': params[1], 'max_requisitions': params[2]})
        tasks_file.close()

        logfile = open(filteredUrlsFile, 'r')
        num_searches = 0
        task_index = 0
        for line in logfile:
            if self.isInitialUrl(line, tasks):
                if task_index == -1:
                    outputfile.close()
                task_index = self.findActualTask(tasks, line)
                outputfile = open(tasks[task_index]['id'], 'w')
                outputfile.write(line)
                num_searches = 1
            else:
                if num_searches <= int(tasks[task_index]['max_requisitions']):
                    num_searches += 1
                    if self.isFinalUrl(line, tasks):
                        task_index = -1
                        num_searches = 0
                    outputfile.write(line)
        outputfile.close()
        return True

    def itentifyTasks(self, forceDbCreation):

        db = mining_database.MiningDatabase(forceDbCreation)
        db.createTables()

        logfiles = []
        inputfile = open(self.configFile, 'r')
        for line in inputfile:
            conf = line.split()
            logfiles.append(conf[3])
            db.insertPage(conf[0])
            db.insertPage(conf[1])
            db.insertConfig(conf[0], conf[1], conf[2], conf[3])
        inputfile.close()

        lu = logutil.LogUtil()

        for logfilepath in logfiles:
            try:
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
            except IOError:
                print 'Arquivo '+ logfilepath +' nao encontrado'
        return True

    def sessions(self):
        db = mining_database.MiningDatabase();
        configs = db.searchConfig('1', '!=', '2').fetchall()

        #com as ids das requisicoes iniciais realizo a separacao das sessoes por tarefa
        for config in configs:
            file_lines = []
            begin_of_tasks = db.customQuery('select * from access where page_id = '+str(config[1])).fetchall()
            #com o inicio das tarefas posso realizar a captura da sequencia de urls acessadas
            counter = 1
            for i in range(len(begin_of_tasks)):
                if i < len(begin_of_tasks) - 1:
                    subsequent_requests = db.customQuery('select * from access where id > '+str(begin_of_tasks[i][0])+' AND user_id = '+str(+begin_of_tasks[i][2])+' AND id < '+ str(begin_of_tasks[i+1][0]) +' limit '+str(config[3]))
                else:
                    subsequent_requests = db.customQuery('select * from access where id > '+str(begin_of_tasks[i][0])+' AND user_id = '+str(+begin_of_tasks[i][2])+' limit '+str(config[3]))

                #nesse ponto tenho os acessos subsequentes ao inicio da tarefa atual para um usuario com a quantidade maxima de urls possiveis para aquela tarefa
                #devo verificar se o usuario chega a url final
                #devo verificar se ele atinge o tempo limite de sessao
                #devo cuidar para nao ter outro inicio de tarefa entre as requisicoes
                requests = subsequent_requests.fetchall()
                if len(requests) > 0:
                    line = self.userCompletedTheTask(requests, begin_of_tasks[i], configs)
                else:
                    line = str(begin_of_tasks[i][1])

                if line != False:
                    file_lines.append(self.normalizeLine(line, config[3])+' access_'+str(counter))
                    counter += 1
            #construo o arquivo de entrada para a tarefa atual
            #documentacao do somtoolbox http://www.ifs.tuwien.ac.at/dm/somtoolbox/index.html
            #mas como eu vou usar o ghsom1.6, preciso verificar essa documentacao
            #http://www.ifs.tuwien.ac.at/~andi/ghsom/index.html
            filename = config[4]+'.in.som'
            header = '$TYPE '+config[4]+'\n$XDIM '+str(len(file_lines))+'\n$YDIM 1 \n$VEC_DIM '+str(config[3]+1)+'\n'
            som_file = open(filename, 'w');
            som_file.write(header);
            for access in file_lines:
                som_file.write(access+'\n')
            som_file.close()
            print ' -file '+filename+' generated'

            template = config[4]+'.t.som'
            header = '$TYPE '+config[4]+'_template\n$XDIM 7\n$YDIM '+str(len(file_lines))+'\n$VEC_DIM '+str(config[3]+1)+'\n'
            template_file = open(template, 'w')
            template_file.write(header)
            for i in range(config[3]+1):
                template_file.write(str(i)+' url_'+str(i)+' 1 1 1 1 1.0\n')
            template_file.close()
            print ' -file '+template+' generated'

            prop = config[4]+'.prop'
            prop_file = open(prop, 'w')

            #os valores default devem ser alterados
            prop_file.write('EXPAND_CYCLES=4\n')
            prop_file.write('MAX_CYCLES=0\n')
            prop_file.write('TAU_1=0.2\n')
            prop_file.write('TAU_2=0.1\n')
            prop_file.write('INITIAL_LEARNRATE=0.8\n')
            prop_file.write('NR=0.0006\n')
            prop_file.write('HTML_PREFIX='+config[4]+'\n')
            prop_file.write('DATAFILE_EXTENSION=\n')
            prop_file.write('randomSeed=17\n')
            prop_file.write('inputFile=./'+filename+'\n')
            prop_file.write('descriptionFile=./'+template+'\n')
            prop_file.write('savePath=./output\n')
            prop_file.write('printMQE=false\n')
            prop_file.write('normInputVectors=NONE\n')
            prop_file.write('saveAsHTML=true\n')
            prop_file.write('saveAsSOMLib=true\n')
            prop_file.write('INITIAL_X_SIZE=2\n')
            prop_file.write('INITIAL_Y_SIZE=2\n')
            prop_file.write('LABELS_NUM=1\n')
            prop_file.write('LABELS_ONLY=true\n')
            prop_file.write('LABELS_THRESHOLD=0.35\n')
            prop_file.write('ORIENTATION=true\n')

            prop_file.close()
            print ' -file '+prop+' generated'
