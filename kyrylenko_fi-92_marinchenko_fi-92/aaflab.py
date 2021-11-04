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
    if type(b)==list:
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
            self.__INVERT_DICT[item]=[]
          if item in self.__INVERT_DICT:
            self.__INVERT_DICT[item].append(i)
    

  def showTable(self):
    for i in self.__DICT.keys():
      print(f'{i}: {self.__DICT[i]}')
  
  def showInvertIndex(self):
    for i in self.__INVERT_DICT.keys():
      print(f'{i}: {self.__INVERT_DICT[i]}')

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
      else:
        return print('wrong name')
    else:
      return print('error')

  def print_index(self,text):
    template=re.findall(r'(PRINT_INDEX)\s+(\w+)\s*\;',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        self.__OBJ[name].invert_index()
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

  def __getNumber(self,text):
    try:
      result = [int(item) for item in text.split(',')]
    except:
      return print('error')
    return result
  
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
    if temp[0].upper() not in ['CREATE','INSERT','PRINT_INDEX','SEARCH']:
      return print('ERROR')
    if temp[0].upper()=='SEARCH':
      self.search(text)    

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