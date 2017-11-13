
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
			return None
	return subs




def parse(sen):
	sen= sen.replace('(',' ( ')
	sen= sen.replace(')',' ) ')
	sen= sen.replace('|','')
	sen= sen.replace(',',' ')
	sen= sen.replace('~', ' ~ ')
	return sen





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
				for clause1 in kb.sentences[keys[pred][i]]:
					if clause1.pred==pred:
						outerClause= clause1	
				for j in range(i+1,arg_size):

					innerClause= None
					for clause2 in kb.sentences[keys[pred][j]]:
						if clause2.pred==pred and clause2.isComp(outerClause):
							innerClause=  clause2

					if outerClause and innerClause:
						temp_sen1= deepcopy(kb.sentences[keys[pred][i]])
						temp_sen2= deepcopy(kb.sentences[keys[pred][j]])
						#standardize(temp_sen1, temp_sen2)
						subs = unify(outerClause,innerClause)
						
						if subs==None:
							continue
						
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
						
						#print("Temporary clause list: ")
						#print(clause_list)
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
								


						if clause_list in kb.sentences or notUnified:
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
	with open("inp1.txt") as f:
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











	


