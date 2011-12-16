from harstorage.lib.MongoHandler import MongoDB

import math

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

            results = {
                        'full_load_time': [],
                        'total_size'    : [],
                        'requests'      : [],
                        'score'         : []
            }

            for document in documents:
                results['full_load_time'].append(document['full_load_time'])
                results['total_size'].append(document['total_size'])
                results['requests'].append(document['requests'])
                results['score'].append(document['ps_scores']['Total Score'])

            # Aggregated stats
            c.metric = request.GET.get('metric', 'Average')

            if c.metric == 'Average':
                time, size, req, score = self.average(results)
            elif c.metric == 'Minimum':
                time, size, req, score = self.minimum(results)
            elif c.metric == 'Maximum':
                time, size, req, score = self.maximum(results)
            elif c.metric == '90th Percentile':
                time, size, req, score = self.percentile(results, 0.9)
            elif c.metric == 'Median':
                time, size, req, score = self.percentile(results, 0.5)

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

    def average(self, results):
        '''
        @parameter results - a dictionary with test results

        @return - the average value for each subset of results
        '''

        # Number or results
        num = len( results['full_load_time'] )

        # Sum
        avg_time    = sum(results['full_load_time'])
        avg_size    = sum(results['total_size']    )
        avg_req     = sum(results['requests']      )
        avg_score   = sum(results['score']         )

        # Averaging
        avg_time    = round( avg_time  / num / 1000.0, 1 )
        avg_size    = int( round( avg_size  / num, 0 ) )
        avg_req     = int( round( avg_req   / num, 0 ) )
        avg_score   = int( round( avg_score / num, 0 ) )

        return avg_time, avg_size, avg_req, avg_score

    def minimum(self, results):
        '''
        @parameter results - a dictionary with test results

        @return - the minimum value for each subset of results
        '''

        min_time    = round( min(results['full_load_time']) / 1000.0, 1 )
        min_size    = min(results['total_size']    )
        min_req     = min(results['requests']      )
        min_score   = min(results['score']         )

        return min_time, min_size, min_req, min_score

    def maximum(self, results):
        """
        @parameter results - a dictionary with test results

        @return - the maximum value for each subset of results
        """

        max_time    = round( max(results['full_load_time']) / 1000.0, 1 )
        max_size    = max(results['total_size']    )
        max_req     = max(results['requests']      )
        max_score   = max(results['score']         )

        return max_time, max_size, max_req, max_score

    def percentile(self, results, percent, key=lambda x:x):
        """
        @parameter results - a dictionary with test results
        @parameter percent - a float value from 0.0 to 1.0
        @parameter key - optional key function to compute value from each element of N.

        @return - the percentile for each subset of results
        """

        k = (len(results['full_load_time']) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)

        for label, data in results.items():
            data = sorted(data)

            if f == c:
                percentile = key(data[int(k)])
            else:
                percentile = key(data[int(f)]) * (c-k) + key(data[int(c)]) * (k-f)

            if label == 'full_load_time':
                percentile_time = round( percentile / 1000.0, 1 )
            elif label == 'total_size':
                percentile_size = int( round( percentile,   0 ) )
            elif label == 'requests':
                percentile_req = int( round( percentile,    0 ) )
            else:
                percentile_score = int( round( percentile,  0 ) )

        return percentile_time, percentile_size, percentile_req, percentile_score