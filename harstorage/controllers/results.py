import logging
import json
import os
import hashlib
import mimetypes
import time

from pylons import request, response, tmpl_context as c
from pylons import config
from pylons.controllers.util import redirect
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController, render
from harstorage.lib.HAR import HAR
from harstorage.lib.MongoHandler import MongoDB

log = logging.getLogger(__name__)

class ResultsController(BaseController):

    """
    Core controller of repository
    """

    def __before__(self):
        """Define version of static content"""

        c.rev = config['app_conf']['static_version']

    @restrict('GET')
    def index(self):
        """Home page with the latest test results"""

        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Data table
        c.metrics_table = list()
        for i in range(7):
            c.metrics_table.append(list())
        
        # Read aggregated data from database
        # Aggregation is based on unique labels and latest timestamps
        latest_results = mdb_handler.collection.group(
            key = ['label', 'url'],
            condition = None,
            initial = {"timestamp":'1970-01-01 01:00:00'},
            reduce = "\
                function(doc, prev) {                       \
                    if ( doc.timestamp > prev.timestamp ) { \
                        prev.timestamp = doc.timestamp;     \
                    }                                       \
                }"
        )

        # Numner of records
        c.rowcount = len(latest_results)

        # Populate data table with the latest test results
        for group in latest_results:
            result = mdb_handler.collection.find_one(
                {'label' : group['label'], 'timestamp' : group['timestamp']}
            )
            
            c.metrics_table[0].append( result['label']                          )
            c.metrics_table[1].append( result['url']                            )
            c.metrics_table[2].append( result['ps_scores']['Total Score']       )
            c.metrics_table[3].append( result["total_size"]                     )
            c.metrics_table[4].append( result["requests"]                       )
            c.metrics_table[5].append( round(result["full_load_time"]/1000.0,1) )
            c.metrics_table[6].append( result["timestamp"]                      )

        return render('./home.html')

    @restrict('GET')
    def details(self):
        """Page with test results"""

        # Try to fetch data for selecetor box
        try:
            c.url = request.GET['url']
            self._selectors(None, c.url)
            c.mode  = 'url'
            c.label = c.url
        # Use label parameter instead of URL parameter
        except:
            c.label = request.GET['label']
            self._selectors(c.label, None)
            c.mode  = 'label'
            c.url   = c.label
 
        return render('./details.html')
    
    def _selectors(self, label, url):
        """
        Create context data - a list of timestamps.
        Additionally generate URL for aggregation of test results

        @parameter label - label of set with test results
        @parameter url   - URL of set with test results
        """

        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Read data for selector box from database
        c.timestamp     = list()

        if label is not None:
            results = mdb_handler.collection.find(
                {"label" : label},
                fields = ["timestamp"],
                sort   = [("timestamp", -1)]
            )
            for result in results:
                c.timestamp.append(result["timestamp"])

            c.query  = "/superposed/display?"
            c.query += "step_1_label=" + label
            c.query += "&step_1_start_ts=" + min(c.timestamp)
            c.query += "&step_1_end_ts=" + max(c.timestamp)
        else:
            results = mdb_handler.collection.find(
                {"url" : url},
                fields = ["timestamp"],
                sort   = [("timestamp", -1)]
            )
            for result in results:
                c.timestamp.append(result["timestamp"])

            c.query = 'None'

    @restrict('GET')
    def timeline(self):
        """Generate data for timeline chart"""

        # Parameters from GET request
        url     = request.GET['url']
        label   = request.GET['label']
        mode    = request.GET['mode']
        
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # 5 Arrays for timeline chart
        ts_points       = str()
        time_points     = str()
        size_points     = str()
        req_points      = str()
        score_points    = str()
        
        # Read data for timeline from database in custom format
        # (hash separated)
        if mode == 'label':
            results = mdb_handler.collection.find(
                {"label" : label},
                fields = ["timestamp", "full_load_time", "total_size", "requests", "ps_scores"],
                sort   = [("timestamp", 1)]
            )
            for result in results:
                ts_points       += str(result["timestamp"]) + "#"
                time_points     += str(round(result["full_load_time"]/1000.0,1)) + "#"
                size_points     += str(result["total_size"]) + "#"
                req_points      += str(result["requests"]) + "#"
                score_points    += str(result["ps_scores"]["Total Score"]) + "#"
        else:
            results = mdb_handler.collection.find(
                {"url" : url},
                fields = ["timestamp", "full_load_time", "total_size", "requests", "ps_scores"],
                sort   = [("timestamp", 1)]
            )
            for result in results:
                ts_points       += str(result["timestamp"]) + "#"
                time_points     += str(round(result["full_load_time"]/1000.0,1)) + "#"
                size_points     += str(result["total_size"]) + "#"
                req_points      += str(result["requests"]) + "#"
                score_points    += str(result["ps_scores"]["Total Score"]) + "#"

        return ts_points[:-1]   + ";" \
             + time_points[:-1] + ";" \
             + size_points[:-1] + ";" \
             + req_points[:-1]  + ";" \
             + score_points[:-1]

    @restrict('GET')
    def runinfo(self):
        """Generate detailed data for each test run"""

        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Parameters from GET request
        timestamp = request.GET['timestamp']

        # MongoDB query
        test_results = mdb_handler.collection.find_one(
            {"timestamp":timestamp}
        )
        
        # HAR parsing
        har     = HAR(test_results['har'], True)
        har_id  = str(test_results['_id'])
        har.analyze()

        # Summary stats
        summary = { 'full_load_time'        : test_results['full_load_time'],
                    'onload_event'          : har.onload_event,
                    'start_render_time'     : har.start_render_time,
                    'time_to_first_byte'    : har.time_to_first_byte,
                    'total_dns_time'        : har.total_dns_time,
                    'total_transfer_time'   : har.total_transfer_time,
                    'total_server_time'     : har.total_server_time,
                    'avg_connecting_time'   : har.avg_connecting_time,
                    'avg_blocking_time'     : har.avg_blocking_time,
                    'total_size'            : test_results['total_size'],
                    'text_size'             : har.text_size,
                    'media_size'            : har.media_size,
                    'cache_size'            : har.cache_size,
                    'requests'              : test_results['requests'],
                    'redirects'             : har.redirects,
                    'bad_requests'          : har.bad_requests,
                    'domains'               : len(har.domains)
        }

        # Domains
        domains_req_ratio = dict()
        domains_weight_ratio = dict()

        for key,value in har.domains.items():
            domains_req_ratio[key] = value[0]
            domains_weight_ratio[key] = value[1]
        
        # Page Speed Scores
        scores = dict()
        
        for rule,score in test_results['ps_scores'].items():
            scores[rule] = score
        
        # Data for HAR Viewer
        filename = os.path.join( config['app_conf']['temp_store'], har_id )
        with open(filename, 'w') as file:
            file.write( test_results['har'].encode('utf-8') )

        # Final JSON
        return json.dumps({'summary'    : summary,
                           'pagespeed'  : scores,
                           'weights'    : har.weight_ratio(),
                           'requests'   : har.req_ratio(),
                           'd_weights'  : domains_weight_ratio,
                           'd_requests' : domains_req_ratio,
                           'har'        : har_id,
        })

    @restrict('GET')
    def harviewer(self):
        """HAR Viewer iframe"""

        # HAR Viewer customization via cookie
        response.set_cookie('phaseInterval', '-1', max_age=365*24*3600 )

        return render('./harviewer.html')
    
    @restrict('GET')
    def deleterun(self):
        """Controller for deletion of tests"""

        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Parameters from GET request
        label       = request.GET['label']
        timestamp   = request.GET['timestamp']
        mode        = request.GET['mode']

        if request.GET['all'] == 'true':
            all = True
        else:
            all = False
            
        # Remove document from collection
        if mode == 'label':
            if all:
                mdb_handler.collection.remove({"label":label})
            else:
                mdb_handler.collection.remove({"label":label, "timestamp":timestamp})
            count = mdb_handler.collection.find({"label":label}).count()
        else:
            if all:
                mdb_handler.collection.remove({"url":label})
            else:
                mdb_handler.collection.remove({"url":label, "timestamp":timestamp})
            count = mdb_handler.collection.find({"url":label}).count()

        if count:
            return ("details?" + mode + '=' + label)
        else:
            return ("/")

    @restrict('POST')
    def upload(self):
        """Controller for uploads of new test results"""

        # HAR initialization
        try:
            har = HAR(request.POST['file'].value)
        except:
            har = HAR(request.POST['file'])
        
        # Analysis of uploaded data
        if har.status == 'Successful':
            # Parsing imported HAR file
            har.analyze()
            
            # MongoDB handler
            mdb_handler = MongoDB()
            
            if config['app_conf']['ps_enabled'] == 'true':
                #Store HAR for Page Speed
                filename = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() )
                pagespeed_bin = os.path.join( config['app_conf']['bin_store'], "pagespeed_bin")
                outfile = filename + ".out"
                
                with open(filename,'w') as file:
                    file.write(json.dumps(har.har))
                
                # Run pagespeed_bin
                os.system(pagespeed_bin + \
                    " -input_file " + \
                    filename + \
                    " -output_format formatted_json " + \
                    "-output_file " + \
                    outfile)
                
                # Output report (JSON)
                filename = outfile
                with open(filename,'r') as file:
                    output = json.loads(file.read())

                # Page Speed scores
                scores = dict()
                
                scores['Total Score'] = int(output['score'])
                
                for rule in output['rule_results']:
                    scores[rule['localized_rule_name']]=int(rule['rule_score'])
            
            else:
                scores = dict()
                
                scores['Total Score'] = 100
            
            # Add document to collection
            mdb_handler.collection.insert({
                "label"          : har.label,
                "url"            : har.url,
                "timestamp"      : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "full_load_time" : har.full_load_time,
                "total_size"     : har.total_size,
                "requests"       : har.requests,
                "ps_scores"      : scores,
                "har"            : har.origin
            })

            try:
                if request.headers['automated'] == 'true': return 'Successful'
            except KeyError:
                redirect('/results/details?label=' + har.label) # redirect to details
        else:
            try:
                if request.headers['automated'] == 'true': return har.status # return exception
            except KeyError:
                c.error = har.status
                return render('./upload.html') # display error page

    @restrict('GET')
    def download(self):
        """Return serialized HAR file"""

        # Parameters from GET request
        id = request.GET['id']

        # Read HAR file from disk
        filename = os.path.join(config['app_conf']['temp_store'], id)
        with open(filename, 'r') as file:
            data = file.read()

        # JSON to JSON-P
        data = "onInputData(" + data + ");"

        # Add content type header
        response.content_type = mimetypes.guess_type(filename)[0] or 'text/plain'

        return data