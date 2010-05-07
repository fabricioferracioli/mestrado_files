# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# script geral do filtro

import logutil, mining_database

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
                outputfile = open(tasks[task_index]['id'], 'a')
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