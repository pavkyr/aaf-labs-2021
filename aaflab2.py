class mySQL:
  tablename=None
  df=None
  index=0

  def __init__(self):
    while self.tablename==None:
      print('CREATE THE TABLE:')
      text=input('>>>')
      if text=='q':
        break
      patern=re.findall(r'(CREATE)\s+(\w+)\s+\(([^)]+)\)',text.upper())
      try:
        if  patern[0][0]=='CREATE' and text[-1]==';' and len(patern)!=0:
          pat=re.findall(r'\(([^)]+)\)',text)
          columns=[str(item) for item in pat[0].split(',')]
          print(columns)
          self.tablename=re.findall(r'\w+',text)[1]
        else:
          print('syntax error')
      except:
        print('syntax error')
    self.df=pd.DataFrame(columns=columns)

  def __getNumber(self,text):
    result = [int(item) for item in text.split(',')]
    return result

  def get_tupl(self,text,template):
    if text[-1]==';' and len(template)!=0:
      result=list(template[0])
      f=re.findall(r'\w+',text)
      if f[1]==self.tablename:
        result[1]=self.tablename
        num=self.__getNumber(result[-1])
        return result[:-1],num
      else:
        return print('undefined table name')
    else:
      return print('syntax error')

  def insertTable(self,num):
    self.df.loc[self.index]=num
    self.index+=1

  def containsTable(self,num):
    for i in self.df.index:
      if set(num)==set(self.df.iloc[i,:]):
        return True
      else:
        return False

  def searchIntersectsTable(self,num):
    row_list=[]
    for i in self.df.index:
      z=set(self.df.iloc[i,:]).intersection(set(num))
      if z!=set():
        row_list.append(self.df.iloc[i,:])
    temd = pd.DataFrame(row_list,columns=self.df.columns)
    temd=temd.dropna()
    return print (temd)

  def searchContainsTable(self,num):
    row_list=[]
    for i in self.df.index:
      if set(num)==set(self.df.iloc[i,:]):
        row_list.append(self.df.iloc[i,:])
    temd = pd.DataFrame(row_list,columns=self.df.columns)
    temd=temd.dropna()
    return print(temd)

  def searchContained_byTable(self,num):
    row_list=[]
    for i in self.df.index:
      z=set(self.df.iloc[i,:]).intersection(set(num))
      if z==set(self.df.iloc[i,:]):
        row_list.append(self.df.iloc[i,:])
    temd = pd.DataFrame(row_list,columns=self.df.columns)
    return print(temd)

  def insert(self,text):
    template=re.findall(r'(INSERT)\s+(\w+)\s+\{([^}]+)\}',text.upper())
    try:
      self.insertTable(self.get_tupl(text,template)[1])
    except:
      print('ERROR')

  def contains(self,text):
    template=re.findall(r'(CONTAINS)\s+(\w+)\s+\{([^}]+)\}',text.upper())
    try:
      return self.containsTable(self.get_tupl(text,template)[1])
    except:
      print('ERROR')

  def search(self,text):
    template=re.findall(r'(SEARCH)\s+(\w+)\s+(WHERE)\s+(INTERSECTS|CONTAINED_BY|CONTAINS)\s+\{([^}]+)\}',text.upper())
    if len(template)==0:
      return print('syntax error')
    if template[0][3]=='INTERSECTS':
      try:
        return self.searchIntersectsTable(self.get_tupl(text,template)[1])
      except:
        print('')
    if template[0][3]=='CONTAINS':
      try:
        return self.searchContainsTable(self.get_tupl(text,template)[1])
      except:
        print('')
    if template[0][3]=='CONTAINED_BY':
      try:
        return self.searchContained_byTable(self.get_tupl(text,template)[1]) 
      except:
        print('')

  def show_df(self):
    print(self.df)

  def process(self):
    RUN=True
    while RUN:
      text=input('>>>')
      if text=='q':
        RUN=False
      splited=re.findall(r'[^\\n]+',text)
      for i in splited:
        temp=re.findall(r'\w+',i)
        if temp[0].upper()=='INSERT':
          self.insert(i)
        if temp[0].upper()=='SEARCH':
          print(self.search(i))
        if temp[0].upper()=='CONTAINS':
          print(self.contains(i))

m=mySQL()
print(m.tablename)
m.process()
m.df