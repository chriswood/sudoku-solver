from django.shortcuts import render_to_response
from django.template import RequestContext

from puzzle import Puzzle
from sudoku.solver.utilities import Dimension
from django.views.decorators.csrf import csrf_exempt


# Ok so now the board is drawn with defaults
# now we need to let people enter values

@csrf_exempt
def sample(request):
    '''
    This was split off from the below function to bypass the csrf token check
    on ajax calls, but leave it in place for all other requests. This returns
    a sample puzzle for development, and for solving once anyway ;)
    '''
    dimension = Dimension([9, 9])
    context_dict = {}
    puzzle = Puzzle(dimension, 'sample')
    context_dict['board'] = puzzle.draw_board()
    context_dict['fields'] = puzzle.get_input_fields()
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))
    
def main(request):
    '''
    Process the requests for updating values in the puzzle, and generating
    new puzzles (coming soon)
    '''
    # I don't really think it is common to have a sudoku puzzle with dimensions
    # other than 9 by 9, but, if someone made a puzzle based hex magic squares 
    # for instance, we'll be ready for them! All code in this program is flexible
    # for any dimension (at great pains, hopefully an 81x81 or something is coming
    # for true fanatics :) ), providing it is a perfect square. 
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
