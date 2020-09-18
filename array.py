


class compact_array(list):

    def __init__(self,Type,*data):
        assert Type in [int,float,bool,str,dict,list,set,tuple] , 'Invalid type'
        assert data , 'Must provide values'
        for k in range(len(data)):
            assert isinstance(data[k],Type) , \
                f'Invalid value found at index {k} must be of \'{Type}\' type'

        self.Type = Type
        self.container = data

    def __str__(self):
        return f'{str(self.Type)[7:12]} : {self.container}'








print(compact_array(str,'d','a'))


