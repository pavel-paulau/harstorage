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
        time_hash     = dict()
        size_hash     = dict()
        requests_hash = dict()
        score_hash    = dict()
        
        # Initial row count
        c.rowcount = 0
        
        # Summary table canvas
        c.metrics_table = list()
        for index in range(6):
            c.metrics_table.append(list())
        
        # Iteration
        for index in range( len(request.POST) /3 ):
            # Parameters
            label       = request.POST[ 'step_'+str(index+1)+'_label' ]
            start_ts    = request.POST[ 'step_'+str(index+1)+'_start_ts' ]
            end_ts      = request.POST[ 'step_'+str(index+1)+'_end_ts' ]
            
            # Average stats
            time, size, req, score = self.get_avg( label,start_ts,end_ts )
            
            # Ordered labels
            label = str(index + 1) + " - " + label
            
            # Data for table
            c.metrics_table[0].append( label    )
            c.metrics_table[1].append( score    )
            c.metrics_table[2].append( size     )
            c.metrics_table[3].append( req      ) 
            c.metrics_table[4].append( time     )
            
            c.rowcount += 1
            
            # Data for timeline
            time_hash[label]        = time
            size_hash[label]        = size
            requests_hash[label]    = req
            score_hash[label]       = score
        
        c.json = json.dumps({
            "time_hash"     : time_hash,
            "size_hash"     : size_hash,
            "requests_hash" : requests_hash,
            "score_hash"    : score_hash
        })
        
        return render('./display.html')
        
    def get_avg(self,label,start_ts,end_ts):
        # MongoDB handler
        md_handler = MongoDB()
        
        avg_size    = 0
        avg_time    = 0
        avg_req     = 0
        avg_score   = 0
        count       = md_handler.collection.find({'label':label,"timestamp" : {"$gte" : start_ts, "$lte" : end_ts} }).count()
        
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