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

print('two')
