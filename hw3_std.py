
from copy import deepcopy
from time import time
class KB:

	def __init__(self):
		self.sentences=[]
		self.keyList={}
		self.doneset= set()
	def add(self,clauseList):
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
		print(self.keyList)


	def printSentences(self):
		for sentence in self.sentences:
			for clause in sentence:
				print(clause,end=" ")
			print()

	def __hash__(self):
		return hash(self.__repr__())


class Clause:
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
	if x[0].isupper():
		return False
	else:
		return True


def unify(x,y):

	if x.pred!= y.pred:
		#print("Predicates don't match")
		return None
	if len(x.args) != len(y.args):
		#print("Argument lists are of different length")
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

				'''
				if subs[y.args[i]] != subs[x.args[i]]:
					return None
				'''

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
	sen= sen.replace('(',' ( ')
	sen= sen.replace(')',' ) ')
	sen= sen.replace('|','')
	sen= sen.replace(',',' ')
	sen= sen.replace('~', ' ~ ')
	return sen



def standardize_apart(sen2):
	for clause in sen2:
		for arg_ind in range(len(clause.args)):
			if isVariable(clause.args[arg_ind]):
				clause.args[arg_ind]=clause.args[arg_ind]+"_1"
		


def factor(sen):
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
				#factor(temp_sen1)
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
							#print(temp_sen1)
							#print(temp_sen2)
							#print(subs)
							

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
									

									#Added sentences
							
							#print("Clauses: ")
							for clause in clause_list:
								#print("Arguments: ")
								for ind in range(len(clause.args)):
									if clause.args[ind].find("_1")!= -1:
										clause.args[ind]=clause.args[ind].replace("_1","")
										
							#print(clause_list)
							#clause_list=factor(clause_list)
							#print(clause_list)
							#print("********")
														
							if clause_list in kb.sentences:
								continue

							
							
							
							if clause_list==[]:
								#print(temp_sen1)
								#print(temp_sen2)
								#print(innerClause)
								#print(outerClause)
								#print("Final answer")
								#kb.printSentences()
								#input()
								#print(len(kb.sentences))
								
								return True
							else:
								newsentences.append(clause_list)

		if newsentences==[]:
			#print("FALSE")
			#kb.printSentences()
			#input()
			#print("*****")
			#rint("******")
			return False

		else:
			#print("New sentences: ")
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
			
			#print(cnt)
			if kb_cnt==0:
				return False
			#kb.printSentences()
			#print(len(kb.sentences))
			#input()
			
if __name__=='__main__':

	queries = []

	sentences=[]
	start=time()
	f1 = open("output.txt", "w")
	with open("wapp_14.txt") as f:
		content = f.readlines()
		#print(content)

		n= content[0].strip()
		#print(n)

		for i in range(int(n)):
			q = content[i+1].strip()
			queries.append(q)

		ind = int(n)+1
		n_sentences = content[ind].strip()

		for i in range(int(n_sentences)):
			sen= content[ind+i+1].strip()
			sentences.append(sen)
	#print(queries)
	#print(sentences)
	#start = time.time();
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
		#clause_list= factor(clause_list)
		#print(clause_list)
		#input()
		kb.add(clause_list)
		#print(clause_list)
	#kb.printSentences()
	#kb.printList()

	for query in queries:
		comp_query = parse(query)
		#print(comp_query)

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
		#print(query_clause)
		#kb.add(query_clause)
		ans = resolution(kb,query_clause)
		#print(ans)
		if ans:
			f1.write("TRUE\n")
		else:
			f1.write("FALSE\n")

		#f1.write(str(ans)+"\n")

		#print(kb.sentences)
		#input()
	#print(resolution(kb,None))
	#kb.printSentences()
	#print(kb.keyList)
	end = time()
	#print(end-start)
	f1.close()
    











	


