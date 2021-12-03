import re

class Table:
  __index=None
  __DICT=None
  __INVERT_DICT=None

  def __init__(self):
    self.__index=1
    self.__DICT={}
    self.__INVERT_DICT={}    

  def addToTable(self,b):
    if type(b)==set:
      self.__DICT[self.__index]=b
      self.__index+=1

  def invert_index(self):
    self.__INVERT_DICT={}
    t=[]
    for i in self.__DICT.keys():
      t+=self.__DICT[i]
    for i in range(1,len(self.__DICT.values())+1):
      check=self.__DICT[i]
      for item in set(t):
        if item in check:
          if item not in self.__INVERT_DICT:
            self.__INVERT_DICT[item]=set()
          if item in self.__INVERT_DICT:
            self.__INVERT_DICT[item].add(i)

  def contains(self,find):
    newdict={}
    for i in find:
      if i in self.__INVERT_DICT.keys():
        newdict[i]=self.__INVERT_DICT.get(i)

    temp=set()
    for i in newdict.values():
      if len(temp)==0:
        temp=i.copy()
      temp.intersection_update(i)

    res=[]
    for i in temp:
      if find ==self.__DICT.get(i):
        res.append(self.__DICT.get(i))

    if len(res)!=0:
      print('True')
    else:
      print('False')  


  def scontains(self,find):
    a=set()
    for i in find:
      if i in self.__INVERT_DICT.keys():
        if len(a)==0:
          a=self.__INVERT_DICT.get(i).copy()
        a.intersection_update(self.__INVERT_DICT.get(i))  

    if len(a)==0:
      print('{}')
    for i in a:
      print(self.__DICT.get(i))

  def intersects(self,find):
    a=set()
    for i in find:
      if i in self.__INVERT_DICT.keys():
        if len(a)==0:
          a=self.__INVERT_DICT.get(i).copy()
        a.update((self.__INVERT_DICT.get(i)))

    for i in a:
      print(self.__DICT.get(i))

  def contained_by(self,find): 
    newdict={}
    for i in find:
      if i in self.__INVERT_DICT.keys():
        newdict[i]=self.__INVERT_DICT.get(i)
    unique=set()

    for i in newdict.values():
      if len(unique)==0: 
        unique=i.copy()
      else:
        unique=unique.union(i)

    uniquelist=list(unique)
    count=[0]*len(uniquelist)
    k=0
    for i in uniquelist:
      for j in newdict.values():
        if i in j:
          count[k]+=1
      k+=1

    k1=0
    answer=[]

    for i in uniquelist:
      if count[k1]==len(self.__DICT.get(i)):
        answer.append(self.__DICT.get(i))
        k1+=1

    for i in answer:
      print(i)

  def showTable(self):
    for i in self.__DICT.keys():
      print(f'{i}: {self.__DICT[i]}')

  def showInvertIndex(self):
    for i in self.__INVERT_DICT.keys():
      print(f'{i}: {self.__INVERT_DICT[i]}')

  def get(self):
    return self.__INVERT_DICT
  def getS(self):
    return self.__DICT

class SQL:
  __tablename=None
  __invert_dict=None
  __OBJ=None
  
  def __init__(self):
    self.__tablenames=[]
    self.__invert_dict={}
    self.d=Table()
    self.__OBJ={}

  def create(self,text):
    template=re.findall(r'(CREATE)\s+(\w+)\s*;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      self.__tablenames.append(name)
      self.__OBJ[name]=Table()
    else:
      print('error')
  
  def insert(self,text):
    template=re.findall(r'(INSERT)\s+(\w+)\s+\{([^}]+)\}\s*\;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        self.__OBJ[name].addToTable(self.__getNumber(list(template[0])[-1]))
        self.__OBJ[name].invert_index()
      else:
        return print('wrong name')
    else:
      return print('error')

  def print_index(self,text):
    template=re.findall(r'(PRINT_INDEX)\s+(\w+)\s*\;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].showInvertIndex() 
      else:
        return print('wrong name')
    else:
      return print('error')

  def search(self,text):
    template=re.findall(r'(SEARCH)\s+(\w+)\s*\;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].showTable() 
      else:
        return print('wrong name')
    else:
      return print('error')
  

  def contains(self,text):
    template=re.findall(r'(CONTAINS)\s+(\w+)\s+\{([^}]+)\}\s*\;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].contains(self.__getNumber(list(template[0])[-1])) 
      else:
        return print('wrong name')
    else:
      return print('error')   

  def searchIntrsects(self,text):
    template=re.findall(r'(SEARCH)\s+(\w+)\s+(WHERE)\s+(INTERSECTS)\s+\{([^}]+)\}\s*;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].intersects(self.__getNumber(list(template[0])[-1])) 
      else:
        return print('wrong name')
    else:
      return print('error')  

  def searchContained_by(self,text):
    template=re.findall(r'(SEARCH)\s+(\w+)\s+(WHERE)\s+(CONTAINED_BY)\s+\{([^}]+)\}\s*;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].contained_by(self.__getNumber(list(template[0])[-1])) 
      else:
        return print('wrong name')
    else:
      return print('error')  

  def searchContains(self,text):
    template=re.findall(r'(SEARCH)\s+(\w+)\s+(WHERE)\s+(CONTAINS)\s+\{([^}]+)\}\s*;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].scontains(self.__getNumber(list(template[0])[-1])) 
      else:
        return print('wrong name')
    else:
      return print('error')  

  def __getNumber(self,text):
    try:
      result = [int(item) for item in text.split(',')]
    except:
      return print('error')
    return set(result)
  
  def input_text(self):
    text=input('>>>')
    t=re.split(r'(?:\\n)',text)
    e=[]
    for i in t:
      if i != '':
        e.append(i)
    return e


  def parser(self,text):
    temp=re.findall(r'\w+',text)
    if temp[0].upper()=='CREATE':
      self.create(text) 
    if temp[0].upper()=='INSERT':
      self.insert(text)
    if temp[0].upper()=='PRINT_INDEX':
      self.print_index(text)
    if temp[0].upper() not in ['CREATE','INSERT','PRINT_INDEX','SEARCH','CONTAINS']:
      return print('ERROR')
    if temp[0].upper()=='SEARCH':
      self.search(text)
    if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='INTERSECTS':
      self.searchIntrsects(text)
    if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='CONTAINED_BY':
      self.searchIntrsects(text)
    if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='CONTAINS':
      self.searchContains(text)
    if temp[0].upper()=='CONTAINS':
      self.contains(text)
           

  def process(self):
    FLAG=True
    while FLAG:
      LISTTEXT=self.input_text()
      for i in LISTTEXT:
        if i=='q' or i=='Q':
          FLAG=False
        else:
          self.parser(i)



s=SQL()
s.process()