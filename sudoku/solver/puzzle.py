from django.utils.safestring import mark_safe

import string

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
        self.html = ''
        
        if not values:
            self.values = self._get_defaults()
        elif values == 'sample':
            self.values = self.sample_puzzle()
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
        # I figure not everyone appreciates zero indexing :)
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
        # first, figure out the overarching structure for the board
        try:
            x = self.dimension.x ** .5
            # for sudoku this should never be a problem but just in case...
            assert(int(x) == x)
        except AssertionError:
            raise
        # build up the html via a few list comprehensions
        [self._outer(index, val, x) for index, val in enumerate(self.values)]
        return mark_safe(self.html)

    def _inner(self, i_nest, x):
        '''
        Build each individual inner cube within the puzzle.
        '''
        inner_html = ''
        if i_nest % x == 0:
            inner_html += '<tr>'
        inner_html += '<td width="27px" height="42px">'
        inner_html += self.values[i_nest]
        inner_html += '</td>'
        if i_nest % x == (x - 1):
            inner_html += '</tr>'
        self.html += inner_html

    def _outer(self, index, el, x):
        '''
        Build the outside framework for our puzzle board based on
        dimensions previously set.
        '''
        if index % (self.dimension.x * x) == 0:
            self.html += '<tr>'
        if index % self.dimension.x == 0:
            self.html += '<td><table cellpadding="8" border="1">'
            [self._inner(i_nest, x) for i_nest in range(index, index + self.dimension.x)]
        if index % self.dimension.x == (self.dimension.x - 1):
            self.html += '</table></td>'
        if index % self.dimension.x * x == (self.dimension.x * x) - 1:
            self.html += '</tr>'

    def sample_puzzle(self):
        '''
        Return a real sudoku puzzle for debugging and building this thing.
        Credit: This puzzle came from the sudoku wikipedia page
        '''
        return [
            '5', '3', '', '6', '', '', '', '9', '0',
            '', '7', '', '1', '9', '5', '', '', '', 
            '', '', '', '', '', '', '', '6', '', 
            '8', '', '', '4', '', '', '7', '', '',
            '', '6', '', '8', '', '3', '', '2', '', 
            '', '', '3', '', '', '1', '', '', '6', 
            '', '6', '', '', '', '', '', '', '', 
            '', '', '', '4', '1', '9', '', '8', '',
            '2', '8', '', '', '', '5', '', '7', '9',
        ]
        
        
        
