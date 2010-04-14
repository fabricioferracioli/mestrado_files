# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#quinto a roda com rotinas para leitura do banco de dados e contrucao das sessoes dos usuarios pela aplicacao, separadas por tarefa recebe o arquivo com as urls de inicio das tarefas

import mining_database, datetime

def timeBetweenRequests(firstAccess, secondAccess):
    fd = firstAccess.split()[0].split('-')
    ft = firstAccess.split()[1].split(':')

    fdt = datetime.datetime(int(fd[2]), int(fd[1]), int(fd[0]), int(ft[0]), int(ft[1]), int(ft[2]))

    sd = secondAccess.split()[0].split('-')
    st = secondAccess.split()[1].split(':')

    stf = datetime.datetime(int(sd[2]), int(sd[1]), int(sd[0]), int(st[0]), int(st[1]), int(st[2]))
    return stf - fdt

def reachMaxIdleTime(firstAccessTime, secondAccessTime):
    #20 minutos
    return timeBetweenRequests(firstAccessTime, secondAccessTime) > datetime.timedelta(0,0,0,0,20)

def userCompletedTheTask(urlSequence, initialAccess, taskConfigs):
#AQUI ESTA O PROBLEMA - TUDO CHEGA MUITO BEM ATE AQUI, MAS A SESSAO NAO ESTA SENDO MUITO BEM IDENTIFICADA
#VERIFICAR SE ESTA REALMENTE FILTRANDO POR TAREFAS DIFERENTES, SE A LINHA ESTA SENDO INICIADA NO MOMENTO CORRETO
#SE O CALCULO DE TEMPO ENTRE DUAS REQUISICOES ESTA CORRETO
    for config in taskConfigs:
        line = str(initialAccess[1]) + ' '
        for i in range(len(urlSequence)):
            ##verifico se ele abortou e comecou qualquer outra tarefa
            if (urlSequence[i][1] == config[1]):
                print 'outra tarefa foi iniciada'
                return false
            #agora devo verificar o tempo de acesso entre duas urls (atual - anterior)

            startNewSession = False
            if (i == 0):
                startNewSession = reachMaxIdleTime(initialAccess[3], urlSequence[i][3])
            else:
                startNewSession = reachMaxIdleTime(urlSequence[i-1][3], urlSequence[i][3])

            if (startNewSession == False):
                line = line + str(urlSequence[i][1]) + ' '
            else:
                print line
                line = ''
        print line


db = mining_database.MiningDatabase();
configs = db.searchConfig('1', '!=', '2').fetchall()

#com as ids das requisicoes iniciais realizo a separacao das sessoes por tarefa
for config in configs:
    begin_of_tasks = db.customQuery('select * from access where page_id = '+str(config[1])).fetchall()
    #com o inicio das tarefas posso realizar a captura da sequencia de urls acessadas
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
            userCompletedTheTask(requests, begin_of_tasks[i], configs)
