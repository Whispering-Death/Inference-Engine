from copy import deepcopy
from time import time
class KB:
	""" Knowledge Base representing a list of Clause

	KB consists of:
		- sentences (list of Clause): List of clauses
		- keyList (dict of 'str':list): Dictionary with the key representing a predicate and value representing the list of int

	"""

	def __init__(self):
		self.sentences=[]
		self.keyList={}
		
	def add(self,clauseList):

		""" A function to add a list of Clause to the sentence list
		Args:
			- clauseList (list of Clause): represents a list of Clause objects	

		"""
		self.sentences.append(clauseList)

		predicates = list(set(clause.pred for clause in clauseList))
		for pred in predicates:
			if pred not in self.keyList:
				self.keyList[pred]=[]
				self.keyList[pred].append(len(self.sentences)-1)
			else:
				self.keyList[pred].append(len(self.sentences)-1)

	def __repr__(self):
		s=""
		for sen in self.sentences:
			s+=print(sen)
		return s

	def printList(self):
		""" Function to print the dictionary - keyList """
		print(self.keyList)


	def printSentences(self):
		""" Function to print all sentences """
		for sentence in self.sentences:
			for clause in sentence:
				print(clause,end=" ")
			print()

	def __hash__(self):
		return hash(self.__repr__())


class Clause:
	""" Clause represents a clause
	A clause contains a predicate and a list of arguments
	It may also have a ~ preceding the predicate which is denoted by  neg = 1.
	Eg;- ~A(x,y) -  neg=1, pred=A, args=[x,y]

	Clause containes-
	- neg (int): A binary value representing whether ~ precedes the predicate or not. 
	- pred (str): A string representing the predicate
	- args (list of str): A list of strings representing the arguments of the predicate 
	"""
	def __init__(self,neg=0,pred="",args=[]):
		self.neg=neg
		self.pred=pred
		self.args=args

	def __repr__(self):
		rep = ""
		if self.neg==1:
			rep+= "~"
		rep+=str(self.pred)+ "( "+" , ".join(self.args)+" )"
		return rep

	def isComp(self, clause):
		""" A function which returns the complement of the predicate """
		if self.neg != clause.neg:
			return True
		else:
			return False

	def __eq__(self, other):
		if self.neg== other.neg and self.pred==other.pred and self.args==other.args:
			return isinstance(other,Clause)

	def __hash__(self):
		return hash(self.__repr__())




def isVariable(x):
	""" A function which checks whether an argument is a variable or not 
	Args:
		- x (str): A string which either represents a variable or a constant
	"""
	if x[0].isupper():
		return False
	else:
		return True


def unify(x,y):
	""" Code to perform unification of 2 Clause objects

	Args:
		- x (Clause instance): A Clause object
		- y (Clause instance): Another Clause object
	"""
	if x.pred!= y.pred:
		return None
	if len(x.args) != len(y.args):
		return None

	subs= {}
	for i in range(len(x.args)):
		#print(subs)
		if not isVariable(x.args[i]) and not isVariable(y.args[i]):
			if x.args[i]== y.args[i]:
				continue
			else:
				return None
		elif isVariable(x.args[i]) and not isVariable(y.args[i]):
			#print(x.args[i]," ",y.args[i])
			if x.args[i] in subs and subs[x.args[i]]!= y.args[i]:			
				return None
			elif x.args[i] not in subs:
				subs[x.args[i]]= y.args[i]

		elif isVariable(y.args[i]) and not isVariable(x.args[i]):
			#print(x.args[i]," ",y.args[i])
			if y.args[i] in subs and subs[y.args[i]]!= x.args[i]:		
				return None
			elif y.args[i] not in subs:
				subs[y.args[i]]= x.args[i]
			

		else:
			
			# Eg:- x and x1 : {x1: x}
			if x.args[i] not in subs and y.args[i] not in subs:
				if x.args[i]== y.args[i]:
					continue
				else:
					subs[y.args[i]]= x.args[i]

			# Eg:- {x:"John"} and x1 -  {x:"John", x1: "John"}

			elif x.args[i] in subs and y.args[i] not in subs:

				subs[y.args[i]] = subs[x.args[i]]

			# Eg:- x and {x1:"John"} - {x:"John", x1:"John"}   or  x and {x1: "x"} - do nothing
			elif x.args[i] not in subs and y.args[i] in subs:
				if isVariable(subs[y.args[i]]) and subs[y.args[i]]!= x.args[i]:
					return None
				else:
					subs[x.args[i]] = subs[y.args[i]]

			else:
				if subs[x.args[i]]!= subs[y.args[i]]:
					return None

	return subs

def parse(sen):
	""" Function to parse the sentence into an appropriate format 
	Args:
		- sen (str): A string which represents a line of the input
	"""
	sen= sen.replace('(',' ( ')
	sen= sen.replace(')',' ) ')
	sen= sen.replace('|','')
	sen= sen.replace(',',' ')
	sen= sen.replace('~', ' ~ ')
	return sen



def standardize_apart(sen2):
	""" Code to standardize variables in a given sentence """
	for clause in sen2:
		for arg_ind in range(len(clause.args)):
			if isVariable(clause.args[arg_ind]):
				clause.args[arg_ind]=clause.args[arg_ind]+"_1"
		


def factor(sen):

	""" Removing repeated predicates which can be unified
	Args:
		- sen (str): A sentence which is a list of Clause objects
	"""
	duplicates=set()
	vis=[0]*len(sen)
	for i in range(len(sen)):
		for j in range(i+1, len(sen)):
			if vis[i] or vis[j]:
				continue
			if sen[i]==sen[j]:
				duplicates.add(sen[j])
				vis[j]=1
				break

			clause1 = sen[i]
			clause2 = sen[j]
			if clause1.pred!= clause2.pred or clause1.isComp(clause2) or len(clause1.args)!= len(clause2.args):
				continue

			isUnifiable = True

			subs= unify(clause1, clause2)
			if subs!= None:
				vis[j]=1

				for clause in sen:
					for ind in range(len(clause.args)):
						if not isVariable(clause.args[ind]):
							continue
						else:
							if clause.args[ind] in subs:
								clause.args[ind] = subs[clause.args[ind]]

	sen=list(set(sen))
	return sen





def resolution(kb1, alpha):
	""" Main code to perform resolution of a query
	Args:
		- kb1 (list of list of Clause): kb1 represents a temporary knowledge base which consists of a list of sentences
		- alpha (list of Clause): Complement of the original query

	The complement of the query is added to the KB.
	The code returns True if an empty sentence([] ) is generated by the KB 
	Code returns False if no new sentences are added to the KB in one iteration
	
	"""

	kb= deepcopy(kb1)

	kb.add(alpha)
	prev_cnt=0
	start=time()
	while True:

		newsentences = []
		keys = kb.keyList
		for pred in keys:
			arg_size = len(keys[pred])

			# generating combinations which can unify and can be added to the KB.
			for i in range(arg_size-1):
				outerClause=None
				for clause1 in kb.sentences[keys[pred][i]]:
					if clause1.pred==pred:
						outerClause= clause1
					else:
						continue

					for j in range(i+1,arg_size):
						end = time()
						time_elapsed = end-start
						if time_elapsed> 45:
							return False
						if keys[pred][i]< prev_cnt and keys[pred][j]<prev_cnt:
							continue
						innerClause= None
						temp_sen2= deepcopy(kb.sentences[keys[pred][j]])


							
						for clause2 in temp_sen2:
							if clause2.pred==pred and clause2.isComp(outerClause):
								innerClause=  clause2

						if outerClause and innerClause:
							standardize_apart(temp_sen2)
							temp_sen1= deepcopy(kb.sentences[keys[pred][i]])
							subs = unify(outerClause,innerClause)
							
							if subs==None:
								continue
							

							temp_sen1.remove(outerClause)
							temp_sen2.remove(innerClause)
							clause_list = temp_sen1+temp_sen2
							
							notUnified = False

							for clause in clause_list:
								for ind in range(len(clause.args)):
									
									if not isVariable(clause.args[ind]):
										continue
									
									if clause.args[ind] in subs:
										clause.args[ind]= subs[clause.args[ind]]
									
							
							for clause in clause_list:
								for ind in range(len(clause.args)):
									if clause.args[ind].find("_1")!= -1:
										clause.args[ind]=clause.args[ind].replace("_1","")
							clause_list=factor(clause_list)
														
							if clause_list in kb.sentences:
								continue

							
							
							
							if clause_list==[]:
								
								return True
							else:
								newsentences.append(clause_list)

		if newsentences==[]:
			return False

		else:
			
			kb_cnt=0
			prev_cnt= len(kb.sentences)
			end = time()

			time_elapsed = end-start
			if time_elapsed > 45:
				return False
			cnt=0
			for sentence in newsentences:
				isNew = True
				if time()-start > 45:

					return False
				for sen in kb.sentences:
					if set(sentence)== set(sen):
						cnt+=1
						isNew= False
				if isNew:
					kb.add(sentence)
					kb_cnt+=1
			
			
			if kb_cnt==0:
				return False
			
			
if __name__=='__main__':
	queries = []

	sentences=[]
	start=time()
	f1 = open("output.txt", "w")
	with open("input.txt") as f:
		content = f.readlines()
		n= content[0].strip()
		for i in range(int(n)):
			q = content[i+1].strip()
			queries.append(q)

		ind = int(n)+1
		n_sentences = content[ind].strip()

		for i in range(int(n_sentences)):
			sen= content[ind+i+1].strip()
			sentences.append(sen)
	kb = KB()
	for i in sentences:
		comp_string = parse(i)
		comp_string = comp_string.split()
		clause_list=[]

		pred=""
		args=[]
		neg= 0
		for j in comp_string:
			if j=='~':
				neg=1
			elif j=='(':
				pass

			elif j==')':
				cl = Clause(neg, pred,args)
				clause_list.append(cl)
				pred=""
				args=[]
				neg=0

			else:
				if pred=="":
					pred=j
				else:
					args.append(j)
		kb.add(clause_list)
		
	for query in queries:
		comp_query = parse(query)
		comp_query = comp_query.split()

		pred=""
		args=[]
		neg=1
		query_clause= []
		for c in comp_query:
			if c=='~':
				neg=0
			elif c=='(':
				pass

			elif c==')':
				query_clause.append(Clause(neg, pred,args))
				pred=""
				args=[]
				neg=0

			else:
				if pred=="":
					pred=c
				else:
					args.append(c)
		ans = resolution(kb,query_clause)
		if ans:
			f1.write("TRUE\n")
		else:
			f1.write("FALSE\n")	
	end = time()
	f1.close()
    











	

