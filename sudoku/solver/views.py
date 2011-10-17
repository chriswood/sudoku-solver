from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe


import string

# Ok so now the board is drawn with defaults
# now we need to let people enter values

def main(request):
    # hardcode this for now, but it can be any size square
    dimension = Dimension([9, 9])
    context_dict = {}

    if request.META['REQUEST_METHOD'] == 'POST':
        values = request.POST
    else:
        values = None
    puzzle = Puzzle(dimension, values)
    context_dict['board'] = puzzle.draw_board()
    context_dict['fields'] = puzzle.get_input_fields()
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


class Puzzle:
    """
    General class to model a puzzle. I'm just using a sudoku board
    now but this may be useful to subclass out later.
    """

    def __init__(self, dimension, values):
        """
            dimension is an instance of class dimension.
            values is a list of puzzle square contents
        """
        self.dimension = dimension
        if not values:
            self.values = self._get_defaults()
        else:
            self.values = self._process_values(values)

    def _process_values(self, values):
        '''
        Return sorted list of values. Only return the form elements holding
        puzzle board attributes (reason for thing < 3 business)
        '''
        return [values[k] for k in sorted(values.iterkeys()) if len(k) < 3]

    def _get_box_name(self, pos):
        '''
        Return the 2 dimension name for the position relative to the
        dimension of the puzzle (worst description ever)
        '''
        convert_list = string.uppercase[:self.dimension.x]
        x = convert_list[pos/self.dimension.x]
        # I figure not everyone appreciates zero indexing like me :)
        y = (pos % self.dimension.x) + 1
        return '%s%d' %(x, y)

    def _get_defaults(self):
        return [self._get_box_name(x) \
             for x in range(self.dimension.cardinality)]

    def get_input_fields(self):
        """
        Return the values needed to build the large form used to populate
        the puzzle board.
        """
        # first just draw the empty fields
        field_list = []
        value = ''
        for index, element in enumerate(range(self.dimension.cardinality)):
            field_dict = {
                'label': self._get_box_name(index),
                'value': value
            }
            field_list.append(field_dict)
        return field_list

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