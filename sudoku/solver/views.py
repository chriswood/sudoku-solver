from django.shortcuts import render_to_response
from django.template import RequestContext

from puzzle import Puzzle
from sudoku.solver.utilities import (
    Dimension,
    is_post
)
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
    puzzle = Puzzle(dimension, 'sample', None)
    context_dict['board'] = puzzle.draw_board()
    context_dict['fields'] = puzzle.get_input_fields()
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))
    
def main(request, action=None):
    '''
    Process the requests for updating values in the puzzle, and generating
    new puzzles (coming soon).
    I hardcoded 9x9, but all code in this program is flexible
    for any dimension, providing it is a square. So we should be able to
    handle different puzzle square type games just by writing a new solver.
    '''
    dimension = Dimension([9, 9])
    context_dict = {}
    values = request.POST if is_post(request) else None

    puzzle = Puzzle(dimension, values, action)
    context_dict['board'] = puzzle.draw_board()
    context_dict['fields'] = puzzle.get_input_fields()
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))
