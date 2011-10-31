class Dimension(object):
    '''
        Basic 2 dimension representaion using cartesion coordinates
    '''

    def __init__(self, coords):
        try:
            self.x = int(coords[0])
            self.y = int(coords[1])
            self.cardinality = self.x * self.y
        except ValueError, e:
            # x and y not both valid integers or string representations
            raise

    def __str__(self):
        return('%s,%s' %(self.x, self.y))