from django.utils.safestring import mark_safe
from math import floor, ceil, sqrt
import string

class Puzzle:
    """
    General class to model a puzzle. I'm just using a sudoku board
    now but this may be useful to subclass out later.
    """

    def __init__(self, dimension, values, action):
        """
            dimension is an instance of class dimension.
            values is a list of puzzle square contents
        """
        self.dimension = dimension
        self.html = ''
        self.values = values
        
        if not values:
            # initial page view
            self._get_defaults()
        elif values == 'sample':
            self.sample_puzzle()
        elif action == 'all':
            # In the future this could be a level of how much of a hint
            # someone wants, so like 'A1' for just that square, or a range
            # such as A1 - A7
            self._process_values()
            self._solve_puzzle()

        else:
            # normal behavior, update the board with cell values
            self._process_values()

    def _process_values(self):
        '''
        Return sorted list of values. Only return the form elements holding
        puzzle board attributes (reason for thing < 3 business)
        '''
        self.values = [self.values[k] for k in sorted(self.values.iterkeys()) if len(k) < 3]
        
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
        '''
        Defaults are just the grid labels, to make it a bit easier to fill in
        '''
        self.values = [self._get_box_name(x) \
             for x in range(self.dimension.cardinality)]

    def _inner(self, i_nest, x):
        '''
        Build each individual inner cube within the puzzle.
        '''
        inner_html = ''
        if i_nest % x == 0:
            inner_html += '<tr>'
        inner_html += '<td width="27px" height="42px" align="center">'
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

    def _solve_puzzle(self):
        '''
        Solve the puzzle for the given problem (sudoku for now)
        and return the board values
        '''
        # We need to know which box we are trying to solve. One at a time.
        # Figure that box out, then set it in the puzzle values
        # This goes down the brute force method. But, once we can solve
        # each square via some method, brute force or better, then we can
        # look for and apply simplifiers.
        # There should be some sort of test to see which box will be easiest.
        # This can rely on various scores, such as how many boxes are filled in.
        # So first, maybe we decide which box is solved easiest if we apply
        # brute force.

        # Also we should solve the "gimmes" if there are any first.
        gimmes = self.find_gimmes()

    def find_gimmes(self):
        '''
        Return list of indices which should be easy to find
        '''
        gimmes = [] #list of indexes which can be easily solved
        for index, square in enumerate(self.values[:1]):
            if self._test_for_gimme(index):
                gimmes.append(index)
        return gimmes

    def _test_for_gimme(self, index):
        #we need the other values in this outer box
        # and we need all the values in this vertical column
        box_vals = self._get_box_values(index)
        col_vals = self._get_col_values(index)
        return True

    def _get_box_values(self, index):
        '''
        Return all the values in a box given an index
        '''
        #[self.values[k] for k in sorted(self.values.iterkeys()) if len(k) < 3]
        #we have [1,2,3,4,5,6,7, etc...]
        start = int(floor(index / self.dimension.x))
        end = start + self.dimension.x
        return [el for el in self.values[start:end]]

    def _get_col_values(self, index):
        '''
        Return list of values for the column this index is in
        '''
        # liberty taken with terminology, but this gives you A, B, C (for 9*9)
        trirant = int(floor(float(index)/float(len(self.values)) * sqrt(self.dimension.x)))
        trirant = string.uppercase[trirant]

        print "trirant = %s" %(trirant)

    def get_input_fields(self):
        """
        Return the values needed to build the large form used to populate
        the puzzle board.
        """
        # first just draw the empty fields
        field_list = []

        for index, element in enumerate(range(self.dimension.cardinality)):
            value = self.values[index]
            label = self._get_box_name(index)
            field_dict = {
                'label': self._get_box_name(index),
                'value': value if value != label else ''
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

    def sample_puzzle(self):
        '''
        Return a real sudoku puzzle for debugging and building this thing.
        Credit: This puzzle came from the sudoku wikipedia page
        '''
        self.values = [
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
