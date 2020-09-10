#
#
#
# class compact_array(list):
#
#
#
#
#     def __init__(self,Type,*data):
#         assert Type in ['int','float','bool','str','dict','list','set','tuple'] , 'Invalid type'
#         assert data , 'Must provide values'
#         for k in range(len(data)):
#             assert Type in str(type(data[k])), \
#                 f'Invalid value found at index {k} must be of \'{Type}\' type'
#
#         self.Type = Type
#         self.container = data
#         list.__init__(self,list(self.container))
#
#     def __str__(self):
#         return f'{self.Type}: {self.container}'
#
#
#
#
#
#
#
# x = compact_array('str','d',0)
#this was changedf in master

from random import randrange
def numPlayers(cutOffRank,scores):
    x ,scores = [] , scores.copy()
    while len(set(x)) != cutOffRank:
      if scores:
        x.append(max(scores))
        scores.remove(max(scores))
      else:
        return len(x)
    return len(x)


x = [randrange(10) for _ in range(10)]
print(numPlayers(4,[20,40,60,60]))

# def calculateWindowMinimums(num, stockPriceDelta, windowSize):
#     delta = []
#     for k in range(len(stockPriceDelta)):
#         temp = []
#         for a in range(k, windowSize):
#             temp.append(stockPriceDelta[a])
#
#         windowSize += 1
#         delta.append(min(temp))
#     return delta
# print(calculateWindowMinimums(7, [0,4,2,73,11,5,60], 4))


