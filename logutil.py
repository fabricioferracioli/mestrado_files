# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#funcoes uteis na manipulacao dos arquivos de log

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