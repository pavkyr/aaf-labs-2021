class SQLparser:
  colection_name=None
  def __init__(self):
    self.colection_name='o'

  def __getNumber(self,text):
    new_text=text[text.index('{')+1:text.index('}')]
    result = [int(item) for item in new_text.split(',')]
    return result

  def  __mCreate(self, text):
    if len(text.split())==2:
      self.colection_name=str(text.split()[1])
      print(f'Collection {self.colection_name} has been created')
    else:
      print('error')

  def __mSearch(self, text):
    if text.split()[1]==self.colection_name:
      if len(text.split())==2:
        print(f'search in {text.split()[1]}')
      if text.lower().split()[2:4]==['where', 'intersects']:
        print(f'Search set of namber {self.__getNumber(text)} ({text.split()[3]}) in {self.colection_name}')
      if text.lower().split()[2:4]==['where', 'contains']:
        print(f'Search set of namber {self.__getNumber(text)} ({text.split()[3]}) in {self.colection_name}')
      if text.lower().split()[2:4]==['where', 'contained_by']:
        print(f'Search set of namber {self.__getNumber(text)} ({text.split()[3]}) in {self.colection_name}')
    else:
      print('not defined')
  
  def __mContains(self, text):
    if text.split()[1]==self.colection_name:
      print(f'Set of namber {self.__getNumber(text)} in the process of checking for in {self.colection_name}')
    else:
      print('not defined')

  def __mInsert(self, text):
    if text.split()[1]==self.colection_name:
      print(f'Set of namber {self.__getNumber(text)} has been added to {self.colection_name}')
    else:
      print('not defined')

  def process(self):
    flag=True
    while flag:
      text=input('>>')
      if text.lower().split()[0]=='create':
        self.__mCreate(text)
      elif text.lower().split()[0]=='insert':
        self.__mInsert(text)
      elif text.lower().split()[0]=='contains':
        self.__mContains(text)
      elif text.lower().split()[0]=='search':
        self.__mSearch(text)
      elif text=='q':
        flag=False
      else:
        print('not defined command')


p=SQLparser()
p.process()