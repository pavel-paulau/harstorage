import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from harstorage.lib.base import BaseController, render

import harstorage.lib.helpers as h

from harstorage.model import Urls, Labels, TestResults, PageSpeed
from harstorage import model

log = logging.getLogger(__name__)

class ResultsController(BaseController):
    def index(self):
        my_session  = model.meta.Session
   
        urls        = my_session.query(Urls)
        labels      = my_session.query(Labels)
        testresults = my_session.query(TestResults)
        pagespeed   = my_session.query(PageSpeed)
        
        # Row count
        c.rowcount = testresults.count()
        
        c.metrics_table = list()
        for index in range(7):
            c.metrics_table.append(list())
            
        # Filling of metrics table
        for result in testresults.order_by(model.testresults_table.c.timestamp.desc()).all():
            label_id        = result.label_id
            pagespeed_id    = result.pagespeed_id
            url_id          = result.url_id
            
            c.metrics_table[0].append( labels.filter_by(id = label_id).first().label )
            c.metrics_table[1].append( urls.filter_by(id = url_id).first().url )
            c.metrics_table[2].append( pagespeed.filter_by(id = pagespeed_id).first().score )
            c.metrics_table[3].append( result.size )
            c.metrics_table[4].append( result.requests ) 
            c.metrics_table[5].append( result.time )
            c.metrics_table[6].append( result.timestamp )
            
        return render('./home.html')

    def details(self):
        c.label = request.GET['label']
        return render('./details.html')
