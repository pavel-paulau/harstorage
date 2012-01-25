import logging
import math

from pylons import request, tmpl_context as c
from pylons import config

from harstorage.lib.base import BaseController, render
from harstorage.lib.MongoHandler import MongoDB
from pylons.decorators.rest import restrict

log = logging.getLogger(__name__)

class SuperposedController(BaseController):

    """
    Interface for aggregation and comparison of test results

    """

    def __before__(self):
        """Define version of static content"""

        c.rev = config['app_conf']['static_version']

    @restrict('GET')
    def create(self):
        """Render form with list of labels and timestamps"""

        # MongoDB handler
        md_handler = MongoDB()
        
        # List of labels
        c.labels    = list()
        
        for label in md_handler.collection.distinct('label'):
            c.labels.append(label)
        
        return render('./create/core.html')
    
    @restrict('GET')
    def dates(self):
        """Return a list of timestamps for selected label"""

        # Read label from GET request
        label = request.GET['label']

        # MongoDB handler
        md_handler = MongoDB()

        # Read data from database
        documents = md_handler.collection.find(
            {'label' : label},
            fields  = ['timestamp'],
            sort    = [('timestamp', 1)]
        )
        
        for document in documents:
            try:
                dates = dates + document['timestamp'] + ';'
            except:
                dates = document['timestamp'] + ';'

        return dates[:-1]

    @restrict('GET')
    def display(self):
        """Render page with column chart and data table"""

        # MongoDB handler
        md_handler = MongoDB()

        # Checkbox options
        c.chart_type    = request.GET.get('chart', None)        
        c.table         = request.GET.get('table', 'false')
        init            = request.GET.get('metric', 'true')

        c.chart = 'true' if c.chart_type else 'false'

        # Metric option
        c.metric = request.GET.get('metric', 'Average')

        # Number of records
        if c.chart == 'true' and c.table == 'true' and init != 'true':
            c.rowcount = len(request.GET) / 3 - 1
        else:
            c.rowcount = len(request.GET) / 3

        # Data containers        
        metrics = [ 'full_load_time', 'requests', 'total_size',
                    'ps_scores', 'onload_event', 'start_render_time',
                    'time_to_first_byte', 'total_dns_time',
                    'total_transfer_time', 'total_server_time',
                    'avg_connecting_time', 'avg_blocking_time', 'text_size',
                    'media_size', 'cache_size', 'redirects', 'bad_requests',
                    'domains']

        c.headers = [   'Label', 'Full Load Time (ms)', 'Total Requests',
                        'Total Size (kB)', 'Page Speed Score',
                        'onLoad Event (ms)', 'Start Render Time (ms)',
                        'Time to First Byte (ms)', 'Total DNS Time (ms)',
                        'Total Transfer Time (ms)', 'Total Server Time (ms)',
                        'Avg. Connecting Time (ms)', 'Avg. Blocking Time (ms)',
                        'Text Size (kB)', 'Media Size (kB)', 'Cache Size (kB)',
                        'Redirects', 'Bad Rquests', 'Domains']

        c.points = str()
        data = dict()
        for metric in metrics:
            data[metric] = list()
        data['label'] = list()

        # Data table
        c.metrics_table = list()
        c.metrics_table.append(list())

        # Test results from database
        for row in range(c.rowcount):
            # Parameters from GET request
            label       = request.GET[ 'step_' + str(row+1) + '_label'    ]
            start_ts    = request.GET[ 'step_' + str(row+1) + '_start_ts' ]
            end_ts      = request.GET[ 'step_' + str(row+1) + '_end_ts'   ]

            # Label
            c.metrics_table[0].append(label)

            data['label'].append(row)
            data['label'][row] = label

            # Fetch test results
            documents = md_handler.collection.find(
                {'label'     : label,
                 'timestamp' : { '$gte':start_ts, '$lte':end_ts }
                },
                fields = metrics
            )

            for metric in metrics:
                data[metric].append(row)
                data[metric][row] = list()

            for document in documents:
                for metric in metrics:
                    if metric != 'ps_scores':
                        data[metric][row].append(document[metric])
                    else:
                        data[metric][row].append(document[metric]['Total Score'])

        # Aggregation
        for row in range(c.rowcount):
            c.points += data['label'][row] + '#'

        column = 1
        for metric in metrics:
            c.metrics_table.append(list())

            c.points = c.points[:-1] + ';'
            for row in range(c.rowcount):
                if c.metric == 'Average':
                    average = self._average(data[metric][row])
                    c.points += str(average) + '#'
                    c.metrics_table[column].append(average)
                elif c.metric == 'Minimum':
                    minimum = self._minimum(data[metric][row])
                    c.points += str(minimum) + '#'
                    c.metrics_table[column].append(minimum)
                elif c.metric == 'Maximum':
                    maximum = self._maximum(data[metric][row])
                    c.points += str(maximum) + '#'
                    c.metrics_table[column].append(maximum)
                elif c.metric == '90th Percentile':
                    percentile = self._percentile(data[metric][row], 0.9)
                    c.points += str(percentile) + '#'
                    c.metrics_table[column].append(percentile)
                elif c.metric == 'Median':
                    percentile = self._percentile(data[metric][row], 0.5)
                    c.points += str(percentile) + '#'
                    c.metrics_table[column].append(percentile)

            column += 1

        c.points = c.points[:-1]

        return render('./display/core.html')

    def _average(self, results):
        """
        @parameter results - a list of test results

        @return - the average value
        """

        try:
            num = len( results )
            total_sum = sum(results)
            return int( round( total_sum / num, 0 ) )
        except TypeError:
            return 'n/a'

    def _minimum(self, results):
        """
        @parameter results - a list of test results

        @return - the minimum value
        """

        return min(results)

    def _maximum(self, results):
        """
        @parameter results - a list of test results

        @return - the maximum value
        """

        return max(results)

    def _percentile(self, results, percent, key=lambda x:x):
        """
        @parameter results - a list of test results
        @parameter percent - a float value from 0.0 to 1.0
        @parameter key - optional key function to compute value from each element of N.

        @return - the percentile
        """

        data = sorted(results)

        k = (len(data) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)
        
        if f == c:
            return key(data[int(k)])
        else:
            try:
                return key(data[int(f)]) * (c-k) + key(data[int(c)]) * (k-f)
            except TypeError:
                return 'n/a'