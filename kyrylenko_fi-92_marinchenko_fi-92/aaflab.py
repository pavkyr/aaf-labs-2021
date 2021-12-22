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
    for i in self.__DICT[self.__index-1]:
      if i not in self.__INVERT_DICT:
        self.__INVERT_DICT[i]=set()
      if i in self.__INVERT_DICT.keys():
        self.__INVERT_DICT[i].add(self.__index-1)

  def contains(self,find):
    if len(find)==0:
      print('False') 
    else:
      newdict={}
      for i in find:
        if i in self.__INVERT_DICT.keys():
          newdict[i]=self.__INVERT_DICT.get(i)
        else:
          print('False')
          return

      temp=set()
      i=0
      for item in newdict.values():
        if i==0:
          temp=item.copy()
        temp.intersection_update(item)
        i+=1

      res=[]
      for i in temp:
        if find ==self.__DICT.get(i):
          res.append(self.__DICT.get(i))

      if len(res)!=0:
        print('True')
      else:
        print('False')  


  def scontains(self,find):
    if len(find)==0:
      self.showTable()
    else:
      a=set()
      i=0
      for item in find:
        if all(elem in self.__INVERT_DICT.keys() for elem in find):
          if i==0:
            a=self.__INVERT_DICT.get(item).copy()
          else:
            a.intersection_update(self.__INVERT_DICT.get(item))
          i+=1
        else:
          print ('{}')
          break
      for i in a:
        print(self.__DICT.get(i))
      

  def intersects(self,find):
    if len(find)==0:
      self.showTable()
    else:
      a=set()
      for i in find:
        if i in self.__INVERT_DICT.keys():
          a.update((self.__INVERT_DICT.get(i)))

      for i in a:
        print(self.__DICT.get(i))

  def contained_by(self,find):
    a=set()
    for i in find:
      if i in self.__INVERT_DICT.keys():
        a.update((self.__INVERT_DICT.get(i)))
    for i in a:
      if self.__DICT.get(i).issubset(find):
        print(self.__DICT.get(i))

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
    template=re.findall(r'\s*(CREATE)\s+(\w+)\s*;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      self.__tablenames.append(name)
      self.__OBJ[name]=Table()
    else:
      print('error')
  
  def insert(self,text):
    template=re.findall(r'\s*(INSERT)\s+(\w+)\s+\{([^}]+)\}\s*\;\s*',text.upper())
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
    template=re.findall(r'\s*(PRINT_INDEX)\s+(\w+)\s*\;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].showInvertIndex() 
      else:
        return print('wrong name')
    else:
      return print('error')

  def newsearch(self,text):
    template=re.findall(r'\s*(SEARCH)\s+(\w+)\s*(\w+|)\s*(CONTAINS|CONTAINED_BY|INTERSECTS|)\s*(\{([^}]+|)\}|)\s*;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      temp=template[0]
      if name in self.__tablenames:
        if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='INTERSECTS' and temp[4]!='':
          return self.__OBJ[name].intersects(self.__getNumber(list(template[0])[-1])) 
        if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='CONTAINED_BY' and temp[4]!='':
          return self.__OBJ[name].contained_by(self.__getNumber(list(template[0])[-1])) 
        if temp[0].upper()=='SEARCH' and temp[2].upper()=='WHERE' and temp[3].upper()=='CONTAINS':
          return self.__OBJ[name].scontains(self.__getNumber(list(template[0])[-1]))     
        if temp[0].upper()=='SEARCH' and temp[2]=='' and temp[3]=='' and temp[4]=='' and temp[5]=='':
          return self.__OBJ[name].showTable()
        else:
          return print('error3') 
      else:
        return print('wrong name')
    else:
      return print('error2')
        

  def contains(self,text):
    template=re.findall(r'\s*(CONTAINS)\s+(\w+)\s+\{([^}]+|)\}\s*\;\s*',text.upper())
    if len(template)!=0:
      name=re.findall(r'\w\s+(\w+)',text)[0]
      if name in self.__tablenames:
        return self.__OBJ[name].contains(self.__getNumber(list(template[0])[-1])) 
      else:
        return print('wrong name')
    else:
      return print('error1')   


  def __getNumber(self,text):
    if text.isspace() or len(text)==0:
      return set()
    else:
      try:
        result = [int(item) for item in text.split(',')]
      except:
        return print('')
      return set(result)
    
  def input_text(self):
    a=[]
    while 1:
      text=input('>>>')
      a.append(text+' ')
      if len(text)!=0 and text[-1]==';':
        break
      elif len(re.findall(r'\s*.EXIT\s*',text.upper()))!=0:
        return None
    e=[]
    t=re.split(r'(?:\\n)',''.join(a))
    for i in t:
      if i != '':
        e.append(i)
    return e


  def parser(self,text):
    temp=re.findall(r'\w+',text)
    if temp[0].upper()=='CREATE':
      self.create(text) 
    elif temp[0].upper()=='INSERT':
      self.insert(text)
    elif temp[0].upper()=='PRINT_INDEX':
      self.print_index(text) 
    elif temp[0].upper()=='SEARCH':
      self.newsearch(text)
    elif temp[0].upper()=='CONTAINS':
      self.contains(text)
    elif temp[0].upper() not in ['CREATE','INSERT','PRINT_INDEX','SEARCH','CONTAINS']:
      return print('ERROR')
           

  def process(self):
    print('for exit print ".exit"')
    FLAG=True
    while FLAG:
      LISTTEXT=self.input_text()
      if LISTTEXT==None:
        break
      for i in LISTTEXT:
        self.parser(i)

s=SQL()
s.process()