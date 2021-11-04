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
    print(self.__DICT)
  
  def showInvertIndex(self):
    print(self.__INVERT_DICT)

class SQL:
  __tablename=None
  __invert_dict=None

  def __init__(self):
    self.__tablename='o'
    self.__invert_dict={}
    self.d=Table()
  
  def create(self,text):
    template=re.findall(r'(CREATE)\s+(\w+)\s*\;',text.upper())
    if len(template)!=0:
      self.__tablename=re.findall(r'\w\s+(\w)\s*;',text)[0]
      self.d=Table()
    else:
      print('error')
  
  def insert(self,text):
    template=re.findall(r'(INSERT)\s+(\w+)\s+\{([^}]+)\}\s*\;',text.upper())
    if len(template)!=0:
      if list(template[0])[1]==self.__tablename.upper():
        self.d.addToTable(self.__getNumber(list(template[0])[-1]))
        return self.d.showTable() 
      else:
        return print('wrong name')
    else:
      return print('error')

  def print_index(self,text):
    template=re.findall(r'(PRINT_INDEX)\s+(\w+)\s*\;',text.upper())
    if len(template)!=0:
      if list(template[0])[1]==self.__tablename.upper():
        self.d.invert_index()
        return self.d.showInvertIndex() 
      else:
        return print('wrong name')
    else:
      return print('error')


  def __getNumber(self,text):
    result = [int(item) for item in text.split(',')]
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
      print('table name is: ',self.__tablename)  
    if temp[0].upper()=='INSERT':
      self.insert(text)
    if temp[0].upper()=='PRINT_INDEX':
      self.print_index(text)
    if temp[0].upper() not in ['CREATE','INSERT','PRINT_INDEX']:
      return print('ERROR')
  
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