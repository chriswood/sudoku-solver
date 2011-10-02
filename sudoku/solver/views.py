from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def main(request):    
    context_dict = {}
    context_dict['hey'] = 'man'
    
    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))
