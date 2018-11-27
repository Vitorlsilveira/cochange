from github import Github
import os
import subprocess
import git

class Git:
    def __init__(self, username, password):
        self.g = Github(username, password)

    def setRepo(self, name, repo, branch, rate):
	self.nameRepo = name
        self.repo = repo
        self.branch = branch
	self.rate = rate

    def run(self):
        self.getCommits()
	self.getNumberTotalCommits()
	self.getPosInitialCommits()
        self.getShaInitial()
	self.cloneLocal()
	self.getUniqueClasses()
        self.initializeMatrixClass()
        self.populateMatrixClass()
        #self.printMatrixClass()
	self.saveMatrixClass()

    def cloneLocal(self):
	os.popen('rm -rf ' + self.nameRepo )
	gitPythonRepo = git.Repo.clone_from('https://github.com/' + self.repo + '.git', self.nameRepo)
	gitPythonRepo.git.checkout(self.shaInitial)
	self.validClasses = subprocess.check_output('find ' + self.nameRepo + ' -iname *.java', shell=True)

    def getUniqueClasses(self):
        self.classes = []
        self.setClasses = set()
	for classe in self.validClasses.split('\n'):
		if classe not in self.setClasses and '.java' in classe:
	            self.setClasses.add(classe.replace( self.nameRepo + '/', ''))
	            self.classes.append(classe.replace( self.nameRepo + '/', ''))			

    def getCommits(self):
        self.repoObject = self.g.get_repo(self.repo)
        self.commits = self.repoObject.get_commits() if self.branch is None else self.repoObject.get_commits(self.branch)

    def getNumberTotalCommits(self):
        self.numberCommitsTotal = 0
	for commit in self.commits:
		self.numberCommitsTotal+= 1
	print "NumCommitsTotal" + str(self.numberCommitsTotal)

    def getPosInitialCommits(self):
        self.posInitialCommits = int ( self.numberCommitsTotal * self.rate / 100 )
	if self.posInitialCommits == 0:
		self.posInitialCommits = 1
	print "PosIniCommits" + str(self.posInitialCommits)
	self.posInitialCommits = self.numberCommitsTotal + 1 - self.posInitialCommits 
	print "PosIniCommits" + str(self.posInitialCommits)

    def getShaInitial ( self ):
	countCommit = 1
        for commit in self.commits:
		if countCommit == self.posInitialCommits:
		 	self.shaInitial = commit.sha
			return
		countCommit+=1

    def initializeMatrixClass( self ):
        self.matrixClass = []
        for i in range (len(self.classes)):
	    row = []
            for j in range (len(self.classes)):
                row.append(0)
	    self.matrixClass.append(row)

    def populateMatrixClass( self ):
	countCommit = 1
        for commit in self.commits:
		if countCommit <= self.posInitialCommits:
            		self.updateMatrixFiles(commit.files)
		countCommit+=1

    def updateMatrixFiles( self, files ):
        for file in files:
	    if file.filename in self.setClasses:
            	row = self.classes.index(file.filename)
            	for update in files:
			if update.filename in self.setClasses:
                		column = self.classes.index(update.filename)
                		self.matrixClass[row][column] += 1

    def printMatrixClass( self ):
        for i in range(len(self.classes)):
	    fileName = self.classes[i]
	    print "Arquivo: " + fileName + "\nModificado em: " + str(self.matrixClass[i][i]) + " commits\n"
	    for j in range(len(self.classes)):
	        if i != j and self.matrixClass[i][j]!=0:
		    fileColumnName = self.classes[j]
		    print fileColumnName + " -> " + str(self.matrixClass[i][j])
	    print "\n"	 

    def saveMatrixClass( self ):
	arq = open( str(self.nameRepo) + "-" + str(self.branch) + ".csv", "w")
	arq.write(str(self.nameRepo) + "-" + str(self.branch) + "\n\n")
        for i in range(len(self.classes)):
	    nameClasses = self.classes[i]
	    valueClasses = str(self.matrixClass[i][i])
	    for j in range(len(self.classes)):
	        if i != j and self.matrixClass[i][j]!=0:
		    nameClasses = nameClasses + ";" + self.classes[j]
		    valueClasses = valueClasses + ";" + str(self.matrixClass[i][j])
	    nameClasses = nameClasses + "\n"
	    valueClasses = valueClasses + "\n\n"
	    arq.write(nameClasses)
	    arq.write(valueClasses)	
		 	
github = Git("user", "password")
github.setRepo('Name', 'repo', 'branch', 'rate')
github.run()


