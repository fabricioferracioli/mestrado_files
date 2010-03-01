# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#funcoes uteis na manipulacao dos arquivos de log

import datetime

class LogUtil:

    def getRequester(self, logline):
        return logline.split()[0]

    def getRequestDate(self, logline):
        return logline[logline.index('[')+1:logline.index(']')]

    def getRequestedDocument(self, logline):
        return logline[logline.index('"'):logline.rindex('"')].split()[1]

    def getServerResponseStatus(self, logline):
        return logline[logline.rindex('"'):].split()[1]

    def getResponseSize(self, logline):
        return logline[logline.rindex('"'):].split()[2]

    def calculateDiferenceBetweenTimes(self, beginTime, endTime)
        return datetime.datetime(beginTime['year'], beginTime['month'], beginTime['day'], beginTime['hour'], beginTime['minute'], beginTime['second']) - datetime.datetime(endTime['year'], endTime['month'], endTime['day'], endTime['hour'], endTime['minute'], endTime['second'])

    def createNNInputFile(self, access, filename, maxurls, maxIdleSessionTime = 20):
        nnfile = open(filename, 'w')
        session_time = []
        actual_user = ''
        line = ''
        for ac in access:
            if actual_user == ac['user_id']:
                #primeiro preciso finalizar a linha atual entao termina isso aqui depois
                #quando for o mesmo usuario da ultima url, posso estar dentro de uma sessao
                time_between_requests = calculateDiferenceBetweenTimes(session_time.pop(), ac['request_date'])
                if  time_between_requests <= maxIdleSessionTime:
                    #estou na mesma sessao
                    line += time_between_requests +' 'ac['page_id']+' '
                    session_time.append(ac['request_date'])
                else:
                    #nao estou na mesma sessao, entao finalizo a linha com o tempo maximo permitido e gravo no arquivo
                    line += maxIdleSessionTime
                    nnfile.write(line)
                    #entao inicio uma nova linha com a nova sessao do mesmo usuario
                    line = ac['page_id']
                    session_time.pop()
                    session_time.append(ac['request_date'])
            else
                #se for um novo usuario apenas inicio uma nova linha com a id da pagina acessada
                line += ac['page_id']+' '
                session_time.append(ac['request_date'])