# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# script que gera os parametros do kmeans a partir da saida do ghsom
class preKmeans:
    def __init__(self, ghsom_properties):
        self.ghsomProperties = ghsom_properties
        self.ghsomInputFile = None
        self.ghsomDescriptionFile = None
        self.ghsomSavePath = None
        self.ghsomResultsPrefix = None
        self.kmeansCentersAmount = 0
        self.kmeansInitialCenters = []
        self.inputVectors = []

    def buildVectors(self):
        properties = open(self.ghsomProperties)
        for line in properties:
            if line.find('inputFile') != -1:
                self.ghsomInputFile = line.split('=')[1].strip()
            elif line.find('descriptionFile') != -1:
                self.ghsomDescriptionFile = line.split('=')[1].strip()
            elif line.find('savePath') != -1:
                self.ghsomSavePath = line.split('=')[1].strip()
            elif line.find('HTML_PREFIX') != -1:
                self.ghsomResultsPrefix = line.split('=')[1].strip()
        print 'founded: '+self.ghsomProperties+' '+self.ghsomInputFile+' '+self.ghsomDescriptionFile+' '+self.ghsomSavePath

    def readInputVector(self):
        inputFile = open(self.ghsomInputFile)
        n_vectors = None
        read_vectors = 0
        can_read = False

        for line in inputFile:
            print line
            if line.find('$XDIM') != -1:
                n_vectors = line.split(' ')[1]
            elif line.find('$VEC_DIM') != -1:
                can_read = True
                continue

            if n_vectors != None and can_read == True and read_vectors <= n_vectors:
                self.inputVectors.append(line.split())
                read_vectors += 1

        print self.inputVectors

    def findCenters(self):
        import os, random
        dir_contents = os.listdir(self.ghsomSavePath)
        unit_files = []
        for content in dir_contents:
            if content.find(self.ghsomResultsPrefix) != -1 and content.find('.unit') != -1:
                 unit_files.append(content)

        pos_x = pos_y = None
        vec_mapped = False
        mapped_vecs = []

        for unit_file in unit_files:
            print 'Inspecionando mapa '+unit_file
            for line in open(self.ghsomSavePath + os.sep + unit_file):
                if line.find('$POS_X') != -1:
                    pos_x = line.split()[1]
                if line.find('$POS_Y') != -1:
                    pos_y = line.split()[1]
                if pos_x != None and pos_y != None:
                    print 'inspecionando posicao %s x %s'%(pos_x, pos_y)
                    pos_x = pos_y = None
                    vec_mapped = False
                if line.find('$NR_VEC_MAPPED') != -1 and int(line.split()[1]) > 0:
                    self.kmeansCentersAmount += 1
                    vec_mapped = True
                if line.find('$MAPPED_VECS') != -1 and vec_mapped:
                    mapped_vecs = line.split()[1:]
                    print mapped_vecs
                if line.find('$NR_SOMS_MAPPED') != -1 and int(line.split()[1]) > 0 and vec_mapped == True:
                    #eh preciso substrair pois existe pelo menos um mapa mais detalhado
                    self.kmeansCentersAmount -= 1
                elif line.find('$NR_SOMS_MAPPED') != -1 and vec_mapped == True:
                    if (len(mapped_vecs) > 1):
                        self.kmeansInitialCenters.append(mapped_vecs[random.randrange(0,len(mapped_vecs)-1)])
                    else:
                        self.kmeansInitialCenters.append(mapped_vecs[0])

                    print 'Novo centro inicial selecionado %s'%(self.kmeansInitialCenters[len(self.kmeansInitialCenters)-1])
        #aqui ele devera abrir os arquivos unit dentro da pasta de resultados
        #nesses aquivos devera ser adotada a seguinte estrategia:
        #a cada posição x,y lida verifica-se o NR_VEC_MAPED
        #caso ele seja maior que 0, um novo centro eh escolhido aleatoriamente
        #e incrementa a quantidade de centros
        #caso seja 0, verifica se NR_SOMS_MAPED é maior que 0
        #caso seja, repete-se toda rotina para as urls encontradas em URL_MAPPED_SOMS
        print 'Foram encontrados %d centros'%(self.kmeansCentersAmount)
        print 'Os %s foram selecionados como centros iniciais'%(self.kmeansInitialCenters)

    def generateKmeansInputFile(self):
        inputfile_name = self.ghsomResultsPrefix+'.in.kmeans'
        inputfile = open(inputfile_name, 'w')

        for access in self.inputVectors:
            inputfile.write(str(access[:len(access)-1]).replace(',', '').replace('[', '').replace(']', '').replace('\'', '')+'\n')

        inputfile.close()
        print 'Arquivo com os pontos de entrada para o Kmeans gerado'

    def generateKmeansPropertyFile(self):
        configfile = self.ghsomResultsPrefix+'.prop.kmeans'
        kmfile = open(configfile, 'w')
        kmfile.write('#Arquivo de entrada do algoritmo de clusterização kmeans para '+self.ghsomResultsPrefix+'\n')

        kmfile.write('stats summary\n')
        kmfile.write('show_assignments yes\n')
        kmfile.write('dim '+str(len(self.inputVectors[0])-1)+'\n')
        kmfile.write('data_size '+str(len(self.inputVectors))+'\n')
        kmfile.write('read_data_pts '+self.ghsomResultsPrefix+'.in.kmeans\n')
        kmfile.write('kcenters '+str(self.kmeansCentersAmount)+'\n')
        kmfile.write('colors '+str(self.kmeansCentersAmount)+'\n')
        kmfile.write('max_tot_stage 20 0 0 0\n')
        kmfile.write('max_run_stage 3\n')
        kmfile.write('min_accum_rdl 0.20\n')
        kmfile.write('seed 42\n')
        kmfile.write('run_kmeans lloyd\n')

        print 'Arquivo com as propriedades para execucao do Kmeans gerado'

pk = preKmeans('submit_exercice.prop')
pk.buildVectors()
pk.readInputVector()
pk.findCenters()
pk.generateKmeansInputFile()
pk.generateKmeansPropertyFile()