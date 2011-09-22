from harstorage.lib.HAR import HAR
from harstorage.lib.MongoHandler import MongoDB

import logging
import json
import os
import hashlib
from mimetypes import guess_type
from time import strftime, localtime

from pylons import request, response, tmpl_context as c
from pylons import config
from pylons.controllers.util import redirect

from harstorage.lib.base import BaseController, render
from harstorage.lib import helpers as h

log = logging.getLogger(__name__)

class ResultsController(BaseController):
    def index(self):
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Initial row count
        c.rowcount = 0
        
        # Result table canvas
        c.metrics_table = list()
        for i in range(7):
            c.metrics_table.append(list())
        
        # Result aggregation based on unique label and latest timestamp
        latest_results = mdb_handler.collection.group(
            key=['label'],
            condition=None,
            initial={"timestamp":'1970-01-01 01:00:00'},
            reduce="\
                function(doc, prev) {                       \
                    if ( doc.timestamp > prev.timestamp ) { \
                        prev.timestamp = doc.timestamp;     \
                    }                                       \
                }"
        )
        
        # Populate result table with latest results
        for set in latest_results:
            result = mdb_handler.collection.find_one({'label':set['label'],'timestamp':set['timestamp']})
            
            c.metrics_table[0].append( result['label']                      )
            c.metrics_table[1].append( result['url']                        )
            c.metrics_table[2].append( result['ps_scores']['Total Score']   )
            c.metrics_table[3].append( result["total_size"]                 )
            c.metrics_table[4].append( result["requests"]                   ) 
            c.metrics_table[5].append( result["full_load_time"]             )
            c.metrics_table[6].append( result["timestamp"]                  )
            
            c.rowcount += 1
        
        return render('./home.html')
    
    def details(self):
        # Try to fetch details for URL
        try:
            c.url = request.GET['url']
            self.selectors(None,c.url)
            c.mode  = 'url'
            c.label = c.url
        # Use Label instead of URL
        except:
            c.label = request.GET['label']
            self.selectors(c.label,None)
            c.mode  = 'label'
            c.url   = c.label
 
        return render('./details.html')
    
    def selectors(self,label,url):
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Timestamps for selector
        c.timestamp     = list()

        # Querying data for timeline
        if label is not None:
            for result in mdb_handler.collection.find({"label":label}).sort("timestamp",-1):
                c.timestamp.append(result["timestamp"])
        else:
            for result in mdb_handler.collection.find({"url":url}).sort("timestamp",-1):
                c.timestamp.append(result["timestamp"])

    def timeline(self):
        # Options
        url     = request.POST['url']
        label   = request.POST['label']
        mode    = request.POST['mode']
        
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # 4 Hashes for timeline chart
        time_hash     = dict()
        size_hash     = dict()
        requests_hash = dict()
        score_hash    = dict()
        
        # Querying data for timeline
        if mode == 'label':
            for result in mdb_handler.collection.find({"label":label}).sort("timestamp",-1):
                time_hash[result["timestamp"]]        = result["full_load_time"]
                size_hash[result["timestamp"]]        = result["total_size"]
                requests_hash[result["timestamp"]]    = result["requests"]
                score_hash[result["timestamp"]]       = result['ps_scores']['Total Score']
        else:
            for result in mdb_handler.collection.find({"url":url}).sort("timestamp",-1):
                time_hash[result["timestamp"]]        = result["full_load_time"]
                size_hash[result["timestamp"]]        = result["total_size"]
                requests_hash[result["timestamp"]]    = result["requests"]
                score_hash[result["timestamp"]]       = result['ps_scores']['Total Score']
        
        return json.dumps({
            "time_hash"     : time_hash,
            "size_hash"     : size_hash,
            "requests_hash" : requests_hash,
            "score_hash"    : score_hash
        })

    def runinfo(self):
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Timestamp from request
        timestamp = request.POST['timestamp']
        
        # MongoDB query
        test_result = mdb_handler.collection.find_one({"timestamp":timestamp})
        
        # HAR initialization
        har     = HAR( test_result['har'] )
        har_id  = str(test_result['_id'])
        har.analyze()

        # Summary stats
        summary = {'score'          :test_result['ps_scores']['Total Score'],
                    'full_time'     :test_result['full_load_time'],
                    'total_size'    :test_result['total_size'],
                    'requests'      :test_result['requests'],
                    'dns'           :har.dns,
                    'transfer'      :har.transfer,
                    'connecting'    :har.connecting,
                    'server'        :har.server,
                    'blocked'       :har.blocked,
                    'text_size'     :har.text_size,
                    'media_size'    :har.media_size,
                    'cache_size'    :har.cached,
                    'redirects'     :har.redirects,
                    'bad_req'       :har.bad_req,
                    'hosts'         :har.hosts
                    }
        
        # Page Speed Scores
        scores = dict()
        
        for rule,score in test_result['ps_scores'].items():
            if rule != 'Total Score':
                scores[rule] = score
        
        # Data for HAR Viewer
        filename = os.path.join( config['app_conf']['temp_store'], har_id )
        file = open(filename, 'w')
        file.write( test_result['har'].encode('utf-8') )
        file.close()

        # Final JSON
        return json.dumps({'summary'    :summary,
                           'pagespeed'  :scores,
                           'weights'    :har.weight_ratio(),
                           'requests'   :har.req_ratio(),
                           'har'        :har_id,
                            })
        
    def harviewer(self):
        # HAR Viewer customization
        response.set_cookie('phaseInterval', '-1')
        
        c.url = h.url_for(str('/results/download?id='+request.GET['har']))
        return render('./harviewer.html')
    
    def deleterun(self):
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # Request parameters
        label       = request.POST['label']
        timestamp   = request.POST['timestamp']
        mode        = request.POST['mode']
        
        # Remove document from collection
        if mode == 'label':
            mdb_handler.collection.remove({"label":label,"timestamp":timestamp})
            count = mdb_handler.collection.find({"label":label}).count()
        else:
            mdb_handler.collection.remove({"url":label,"timestamp":timestamp})
            count = mdb_handler.collection.find({"url":label}).count()

        if count:
            return ("details?",mode,'=',label)
        else:
            return ("/")

    def search(self):
        c.search_text = request.POST['search_text']
        return render('./search.html')

    def upload(self):
        # HAR initialization
        try:
            har = HAR( request.POST['file'].value )
        except:
            har = HAR( request.POST['file'] )
        
        # Check for initialization status
        if har.status == 'Ok':
            # Parsing imported HAR file
            har.analyze()
            
            # MongoDB handler
            mdb_handler = MongoDB()
            
            # Fix time format
            for entry in har.har['log']['entries']:
                entry['startedDateTime'] = entry['startedDateTime'].replace('+0000','+00:00')

            for page in har.har['log']['pages']:
                page['startedDateTime'] = page['startedDateTime'].replace('+0000','+00:00')
            
            if config['app_conf']['ps_enabled'] == 'true':
                #Store HAR for Page Speed
                filename = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() )
                pagespeed_bin = os.path.join( config['app_conf']['bin_store'], "pagespeed_bin")
                outfile = filename + ".out"
                
                file = open(filename,'w')
                file.write(json.dumps(har.har))
                file.close()
                
                # Run pagespeed_bin
                os.system(pagespeed_bin + \
                    " -input_file " + \
                    filename + \
                    " -output_format formatted_json " + \
                    "-output_file " + \
                    outfile)
                
                # Output report (JSON)
                filename = outfile
                file = open(filename,'r')
                output = json.loads(file.read())
                file.close()

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
                "label"         :har.label,
                "url"           :har.url,
                "timestamp"     :strftime("%Y-%m-%d %H:%M:%S", localtime()),
                "full_load_time":har.full_load_time,
                "total_size"    :har.total_size,
                "requests"      :har.requests,
                "browser"       :har.browser,
                "ps_scores"     :scores,
                "har"           :har.origin
            })
            
            redirect('/results/details?label=' + har.label)
        else:
            # Display error page
            return render('./upload.html')

    def download(self):
        id = request.GET['id']
        
        filename = os.path.join( config['app_conf']['temp_store'], id )
        file = open(filename, 'r')
        data = file.read()
        file.close()
        
        response.content_type = guess_type(filename)[0] or 'text/plain'
        return data