# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
# script que gera os parametros do kmeans a partir da saida do ghsom
class preKmeans:
    def __init__(self, ghsom_properties):
        self.ghsomProperties = ghsom_properties
        self.ghsomInputFile = None
        self.ghsomDescriptionFile = None
        self.ghsomSavePath = None
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
                print ('aqui1')
            elif line.find('$VEC_DIM') != -1:
                can_read = True
                print ('aqui2')
                continue

            if n_vectors != None and can_read == True and read_vectors <= n_vectors:
                self.inputVectors.append(line.split())
                read_vectors += 1

        print self.inputVectors

    def findCenters(self):
        #aqui ele devera abrir os arquivos unit dentro da pasta de resultados
        #nesses aquivos devera ser adotada a seguinte estrategia:
        #a cada posição x,y lida verifica-se o NR_VEC_MAPED
        #caso ele seja maior que 0, um novo centro eh escolhido aleatoriamente
        #e incrementa a quantidade de centros
        #caso seja 0, verifica se NR_SOMS_MAPED é maior que 0
        #caso seja, repete-se toda rotina para as urls encontradas em URL_MAPPED_SOMS


pk = preKmeans('submit_exercice.prop')
pk.buildVectors()
pk.readInputVector()