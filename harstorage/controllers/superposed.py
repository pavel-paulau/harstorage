from harstorage.lib.MongoHandler import MongoDB

import logging

from pylons import request, tmpl_context as c
from pylons import config

from harstorage.lib.base import BaseController, render

log = logging.getLogger(__name__)

class SuperposedController(BaseController):
    def create(self):
        # Version for static content
        c.rev = config['app_conf']['static_version']

        # MongoDB handler
        md_handler = MongoDB()
        
        # List of labels
        c.labels    = list()
        labels = md_handler.collection.distinct('label')

        for label in labels:
            c.labels.append(label)
        
        return render('./create.html')
    
    def dates(self):
        # Label
        label = request.GET['label']

        # MongoDB handler
        md_handler = MongoDB()
        
        dates = str()

        documents = md_handler.collection.find({
            'label':label
        })
        
        documents.sort('timestamp', 1)

        for document in documents:
            dates += document['timestamp'] + ';'

        return dates[:-1]

    def display(self):
        # Version for static content
        c.rev = config['app_conf']['static_version']

        # MongoDB handler
        md_handler = MongoDB()

        # 5 Arrays for timeline chart
        lbl_points      = str()
        time_points     = str()
        size_points     = str()
        req_points      = str()
        score_points    = str()

        # Initial row count
        c.rowcount = 0

        # Summary table canvas
        c.metrics_table = list()
        for index in range(6):
            c.metrics_table.append( list() )

        # Aggregation
        for index in range( len(request.GET) /3 ):
            # Parameters
            label       = request.GET[ 'step_' + str(index+1) + '_label'    ]
            start_ts    = request.GET[ 'step_' + str(index+1) + '_start_ts' ]
            end_ts      = request.GET[ 'step_' + str(index+1) + '_end_ts'   ]

            # Test results
            documents = md_handler.collection.find({
                'label'     : label,
                'timestamp' : { '$gte':start_ts, '$lte':end_ts }
            })

            # Average stats
            time, size, req, score = self.average(documents)

            # Data for table
            c.metrics_table[0].append( label )
            c.metrics_table[1].append( score )
            c.metrics_table[2].append( size  )
            c.metrics_table[3].append( req   )
            c.metrics_table[4].append( time  )

            c.rowcount += 1

            lbl_points      += str(label) + '#'
            time_points     += str(time)  + '#'
            size_points     += str(size)  + '#'
            req_points      += str(req)   + '#'
            score_points    += str(score) + '#'

        c.points = lbl_points[:-1]  + ';' \
                 + time_points[:-1] + ';' \
                 + size_points[:-1] + ';' \
                 + req_points[:-1]  + ';' \
                 + score_points[:-1]

        return render('./display.html')

    def average(self, documents):
        # Variables
        avg_size    = 0
        avg_time    = 0
        avg_req     = 0
        avg_score   = 0

        # Averaging
        for document in documents:
            avg_time    += round(document['full_load_time']/1000.0, 1)
            avg_size    += document['total_size']
            avg_req     += document['requests']
            avg_score   += document['ps_scores']['Total Score']

        count = documents.count()

        avg_time    = round( avg_time  / count, 1 )
        avg_size    = int( round( avg_size  / count, 0 ) )
        avg_req     = int( round( avg_req   / count, 0 ) )
        avg_score   = int( round( avg_score / count, 0 ) )

        return avg_time, avg_size, avg_req, avg_score