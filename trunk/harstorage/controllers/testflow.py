from harstorage.lib.MongoHandler import MongoDB

import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from harstorage.lib.base import BaseController, render

log = logging.getLogger(__name__)

class TestflowController(BaseController):
    def create(self):
        # MongoDB handler
        md_handler = MongoDB()
        
        # List of labels
        c.labels    = list()
        for label in md_handler.collection.distinct('label'):
            c.labels.append(label)
        
        return render('./create.html')
    
    def dates(self):
        # Label
        label = request.POST['label']
        
        # MongoDB handler
        md_handler = MongoDB()
        
        dates = dict()
        index = 0
        for document in md_handler.collection.find({'label':label}).sort("timestamp",-1):
            dates[index] = (document['timestamp'])
            index += 1
        
        return json.dumps(dates)
            
    def display(self):
        # 4 Hashes for timeline chart
        c.time_hash     = dict()
        c.size_hash     = dict()
        c.requests_hash = dict()
        c.score_hash    = dict()
        
        
        for index in range( len(request.POST) /3 ):
            label       = request.POST[ 'step_'+str(index+1)+'_label' ]
            start_ts    = request.POST[ 'step_'+str(index+1)+'_start_ts' ]
            end_ts      = request.POST[ 'step_'+str(index+1)+'_end_ts' ]
            
            time, size, req, score = self.get_avg( label,start_ts,end_ts )
            
            label = str(index+1) + " - " + label
            c.time_hash[label]        = time
            c.size_hash[label]        = size
            c.requests_hash[label]    = req
            c.score_hash[label]       = score

        return render('./display.html')
        
    def get_avg(self,label,start_ts,end_ts):
        # MongoDB handler
        md_handler = MongoDB()
        
        avg_size    = 0
        avg_time    = 0
        avg_req     = 0
        avg_score   = 0
        count       = md_handler.collection.find({'label':label,"timestamp" : {"$gte" : start_ts, "$lte" : end_ts} }).count()
        
        print count
        
        for document in md_handler.collection.find({'label':label,"timestamp" : {"$gte" : start_ts, "$lte" : end_ts} }):
            avg_size    += document["total_size"]
            avg_time    += document["full_load_time"]
            avg_req     += document["requests"]
            avg_score   += document['ps_scores']['Total Score']
            
        avg_size    /= count
        avg_time    /= count
        avg_req     /= count
        avg_score   /= count
        
        return avg_time, avg_size, avg_req, avg_score