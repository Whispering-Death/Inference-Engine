
from copy import deepcopy
class KB:

	def __init__(self):
		self.sentences=[]
		self.keyList={}
		self.doneset= set()
	def add(self,clauseList):
		self.sentences.append(clauseList)

		predicates = list(set(clause.pred for clause in clauseList))
		#print(predicates)
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
		print("Predicates don't match")
		return None
	if len(x.args) != len(y.args):
		print("Argument lists are of different length")
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
			#print(subs)

		else:
			'''
			if x.args[i]!= y.args[i]:
				return None
			'''
			
			# Eg:- x and x1 : {x1: x}
			if x.args[i] not in subs and y.args[i] not in subs:
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


def Unify(x, y, subst = {}):
    if subst is None:
        return None

    elif x == y:
        return subst

    elif isVariable(x):
        return Unify_Var(x, y, subst)

    elif isVariable(y):
        return Unify_Var(y, x, subst)

    else:
        return None


def Unify_Var(var, x, subst):
    if var in subst:
        return Unify(subst[var], x, subst)

    newSubst = subst.copy()
    newSubst[var] = x
    return newSubst




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
		


def factor(clause_list):
	
	posPred= dict()
	for ind in range(len(clause_list)):
		print("A")
		clause = clause_list[ind]
		if clause.neg==0:
			continue
		if clause.pred in posPred:
			posPred[clause.pred].append(ind)
		else:
			posPred[clause.pred]=[ind]
	print("Clause list: ")
	print(clause_list)
	print("Dictionary: ")
	print(posPred)
	input()
	for j in posPred:
		if len(posPred[j])==1:
			continue
		else:
			print(posPred[j][0], posPred[j][1])
			subs = unify(clause_list[posPred[j][0]], clause_list[posPred[j][1]])
			if subs==None:
				return False


	return True



def resolution(kb1, alpha):
	kb= deepcopy(kb1)

	kb.add(alpha)
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

						innerClause= None
						temp_sen2= deepcopy(kb.sentences[keys[pred][j]])


							
						for clause2 in temp_sen2:
							if clause2.pred==pred and clause2.isComp(outerClause):
								innerClause=  clause2

						if outerClause and innerClause:
							standardize_apart(temp_sen2)
							temp_sen1= deepcopy(kb.sentences[keys[pred][i]])
							#factor(temp_sen1)
							#print("Temporary sentence: ")
							#print(temp_sen2)
							#print("Inner clause: ")
							#print(innerClause)
							#print("Outer Clause: ")
							#print(outerClause)
							#standardize(temp_sen1, temp_sen2)
							subs = unify(outerClause,innerClause)
							
							if subs==None:
								continue
							print(temp_sen1)
							print(temp_sen2)
							print(subs)
							
							'''
							for clause in temp_sen1:
								if clause.pred==pred:
									temp_sen1.remove(clause)
									break

			
							
							for clause in temp_sen2:
								if clause.pred==pred:
									temp_sen2.remove(clause)
									break
							'''

							temp_sen1.remove(outerClause)
							temp_sen2.remove(innerClause)
							clause_list = temp_sen1+temp_sen2
							
							notUnified = False

							for clause in clause_list:
								for ind in range(len(clause.args)):
									#Adde
									if not isVariable(clause.args[ind]):
										continue
									#EAdde
									if clause.args[ind] in subs:
										clause.args[ind]= subs[clause.args[ind]]
									'''
									else:
										notUnified=True
										break
									'''

									#Added sentences
							
							#print("Clauses: ")
							for clause in clause_list:
								#print("Arguments: ")
								for ind in range(len(clause.args)):
									if clause.args[ind].find("_1")!= -1:
										clause.args[ind]=clause.args[ind].replace("_1","")
										#print("New arg: ",arg)
							#print("Temporary clause list: ")
							print(clause_list)
							#print(factor(clause_list))
							print("********")
							#factor(clause_list)
							

							
							if clause_list in kb.sentences:
								continue

							
							
							
							if clause_list==[]:
								#print(innerClause)
								#print(outerClause)
								print("Final answer")
								kb.printSentences()
								#input()
								print(len(kb.sentences))
								#print(innerClause)
								#print(outerClause)
								#print()
								return True
							else:
								
								#print(kb.sentences[keys[pred][i]])
								#print(kb.sentences[keys[pred][j]])
								#print("Inner Clause", innerClause)
								#print("Outer Clause", outerClause)
								#print(subs)
								#print(clause_list)
								#print("****")
								#input()
								
								#print("****")
								newsentences.append(clause_list)

		if newsentences==[]:
			#print("FALSE")
			kb.printSentences()
			#print("*****")
			#rint("******")
			return False

		else:
			#print("New sentences: ")
			kb_cnt=0
			for sentence in newsentences:
				isNew = True
				for sen in kb.sentences:
					if set(sentence)== set(sen):
						isNew= False
				if isNew:
					kb.add(sentence)
					kb_cnt+=1
				
			if kb_cnt==0:
				return False
			kb.printSentences()
			print(len(kb.sentences))
			#print(len(set(kb.sentences)))
			input()
			#input()






if __name__=='__main__':

	queries = []

	sentences=[]

	f1 = open("output.txt", "w")
	with open("inp5.txt") as f:
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
	f1.close()











	


