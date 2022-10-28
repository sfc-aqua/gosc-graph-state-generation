import random

nodeList={1:[2,3],
      2:[1,3],
      3:[1,2],
}

def getEdge():
  i = random.choice(list(nodeList))
  j = random.choice(nodeList[i])
  return [i,j]

def contract(n1,n2):
  for i in nodeList[n2]:
    if(i!=n1):
        nodeList[n1].append(i)
  nodeList.pop(n2)
  for key,value in nodeList.items():
    value[:] = [n1 if x==n2 else x for x in value]
    value[:] = [x for x in value if x!=key]

def karger():
  while (len(nodeList) > 2):
    edge = getEdge()
    contract(edge[0],edge[1])
  val = len(list(nodeList.values())[0])
  print(val)
  return val

karger()
