# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#rotinas para leitura do banco de dados e contrucao das sessoes dos usuarios pela aplicacao, separadas por tarefa
#recebe o arquivo com as urls de inicio das tarefas

import mining_database
db = mining_database.MiningDatabase();
configs = db.searchConfig('1', '!=', '2').fetchall()
#com as ids das requisicoes iniciais realizo a separacao das sessoes por tarefa
for config in configs:
    begin_of_tasks = db.customQuery('select * from access where page_id = '+str(config[1])).fetchall()
    #com o inicio das tarefas posso realizar a captura da sequencia de urls acessadas
    for bt in begin_of_tasks:
        subsequent_requests = db.customQuery('select * from access where page_id > '+str(bt[0])+' AND user_id = '+str(+bt[2])+' limit '+str(config[3]))
        print subsequent_requests.fetchall()


