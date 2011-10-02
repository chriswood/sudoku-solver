from django.conf.urls.defaults import *
from sudoku.solver.views import *

urlpatterns = patterns('',
    url(r'^$', main),
    #url(r'^home/$', main),
    #url(r'^/hey/', include('potpiebear.ppbapp.urls')),
)