from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe


def main(request):
    # hardcode this for now, but it can be any size square
    dimension = Dimension([9, 9])
    context_dict = {}
    
    if request.META['REQUEST_METHOD'] == 'POST':
        # pull values from post
        #values = POST.values
        #values are a list, gotten like this me[row*3+col]
        pass
    else:
        values = None
    puzzle = Puzzle(dimension, values)
    context_dict['board'] = puzzle.draw_board()
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))

class Puzzle:
    """
    General class to model a puzzle. I'm just using a sudoku board
    now but this may be useful to subclass out later.
    """
    def __init__(self, dimension, values, puzzle_type='sudoku'):
        """
            dimension is an instance of class dimension.
            values is a list of puzzle square contents
        """
        self.puzzle_type = puzzle_type
        self.dimension = dimension
        if not values:
            self.values = self._get_defaults()
        else:
            self.values = values

    def _get_defaults(self):
        return ['NA' for x in range(self.dimension.cardinality)]

    def draw_board(self):
        '''
        Generate the html for the sudoku puzzle. Each td element should have
        a unique id corresponding to its position. We'll also fill in the board
        values already in memory.
        '''
        # first draw an empty board
        html = ''
        for index, el in enumerate(self.values):
            if index % self.dimension.x == 0:
                html += '<tr>'
            html += "<td id='%s'>%s</td>" %(index, el)
            if index % self.dimension.x == (self.dimension.x - 1):
                html += '</tr>'

        return mark_safe(html)

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