from django.conf.urls.defaults import *
from sudoku.solver.views import *

urlpatterns = patterns('',
    url(r'^$', main),
    url(r'^sample/$', sample),
    url(r'^(?P<action>\w+)/$', main)
)