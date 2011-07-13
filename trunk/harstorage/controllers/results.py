import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from harstorage.lib.base import BaseController, render

import harstorage.lib.helpers as h

from harstorage.model import Urls, Hars, Metrics, PageSpeed
from harstorage import model

log = logging.getLogger(__name__)

class ResultsController(BaseController):

    def index(self):
        my_session  = model.meta.Session
   
        urls        = my_session.query(Urls)
        metrics     = my_session.query(Metrics)
        hars        = my_session.query(Hars)
        pagespeed   = my_session.query(PageSpeed)
        
        # Row count
        c.rowcount = metrics.count()
        
        c.metrics_table = list()
        for index in range(7):
            c.metrics_table.append(list())
            
        # Filling of metrics table
        for metric in metrics.order_by(model.metrics_table.c.timestamp.desc()).all():
            har_id        = metric.har_id
            pagespeed_id  = metric.pagespeed_id
            url_id        = metric.url_id
            
            c.metrics_table[0].append( urls.filter_by(id = url_id).first().label )
            c.metrics_table[1].append( urls.filter_by(id = url_id).first().url )
            c.metrics_table[2].append( pagespeed.filter_by(id = pagespeed_id).first().score )
            c.metrics_table[3].append( hars.filter_by(id = har_id).first().total_size )
            c.metrics_table[4].append( hars.filter_by(id = har_id).first().requests ) 
            c.metrics_table[5].append( hars.filter_by(id = har_id).first().full_time )
            c.metrics_table[6].append( metric.timestamp )
            
        return render('./home.html')