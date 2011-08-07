from harstorage.lib.HAR import HAR
from harstorage.lib.MongoHandler import MongoDB

import logging
import json
import os

from time import strftime, localtime

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.controllers.util import abort, redirect

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
        for index in range(7):
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
            self.timeline(None,c.url)
            c.mode='url'
        # Use Label instead of URL
        except:
            c.label = request.GET['label']
            self.timeline(c.label,None)
            c.mode='label'
 
        return render('./details.html')

    def timeline(self,label,url):
        # MongoDB handler
        mdb_handler = MongoDB()
        
        # 4 Hashes for timeline chart
        c.time_hash     = dict()
        c.size_hash     = dict()
        c.requests_hash = dict()
        c.score_hash    = dict()
        
        # Timestamps for selector
        c.timestamp     = list()

        # Querying data for timeline
        if label is not None:
            for result in mdb_handler.collection.find({"label":label}).sort("timestamp",-1):
                c.time_hash[result["timestamp"]]        = result["full_load_time"]
                c.size_hash[result["timestamp"]]        = result["total_size"]
                c.requests_hash[result["timestamp"]]    = result["requests"]
                c.score_hash[result["timestamp"]]       = result['ps_scores']['Total Score']

                c.timestamp.append(result["timestamp"])
        else:
            for result in mdb_handler.collection.find({"url":url}).sort("timestamp",-1):
                c.time_hash[result["timestamp"]]        = result["full_load_time"]
                c.size_hash[result["timestamp"]]        = result["total_size"]
                c.requests_hash[result["timestamp"]]    = result["requests"]
                c.score_hash[result["timestamp"]]       = result['ps_scores']['Total Score']

                c.timestamp.append(result["timestamp"])

            c.label = c.url

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
        
        # Resource stats
        weights = har.weight_ratio()
        requests = har.req_ratio()

        # Page Speed Scores
        scores =  { 'Total Score'                           :test_result['ps_scores']['Total Score'],
                    'Avoid CSS @import'                     :test_result['ps_scores']['Avoid CSS @import'],
                    'Avoid bad requests'                    :test_result['ps_scores']['Avoid bad requests'],
                    'Combine images into CSS sprites'       :test_result['ps_scores']['Combine images into CSS sprites'],
                    'Defer loading of JavaScript'           :test_result['ps_scores']['Defer loading of JavaScript'],
                    'Defer parsing of JavaScript'           :test_result['ps_scores']['Defer parsing of JavaScript'],
                    'Enable Keep-Alive'                     :test_result['ps_scores']['Enable Keep-Alive'],
                    'Enable compression'                    :test_result['ps_scores']['Enable compression'],
                    'Inline small CSS'                      :test_result['ps_scores']['Inline small CSS'],
                    'Inline small JavaScript'               :test_result['ps_scores']['Inline small JavaScript'],
                    'Leverage browser caching'              :test_result['ps_scores']['Leverage browser caching'],
                    'Make redirects cacheable'              :test_result['ps_scores']['Make redirects cacheable'],
                    'Minify CSS'                            :test_result['ps_scores']['Minify CSS'],
                    'Minify HTML'                           :test_result['ps_scores']['Minify HTML'],
                    'Minify JavaScript'                     :test_result['ps_scores']['Minify JavaScript'],
                    'Minimize redirects'                    :test_result['ps_scores']['Minimize redirects'],
                    'Minimize requests size'                :test_result['ps_scores']['Minimize requests size'],
                    'Optimize images'                       :test_result['ps_scores']['Optimize images'],
                    'Optimize order of styles and scripts'  :test_result['ps_scores']['Optimize order of styles and scripts'],
                    'Prefer asyncronous resources'          :test_result['ps_scores']['Prefer asyncronous resources'],
                    'Put CSS in the document head'          :test_result['ps_scores']['Put CSS in the document head'],
                    'Remove query string from statics'      :test_result['ps_scores']['Remove query string from statics'],
                    'Remove unused css'                     :test_result['ps_scores']['Remove unused css'],
                    'Serve resources from consistent URL'   :test_result['ps_scores']['Serve resources from consistent URL'],
                    'Serve scaled images'                   :test_result['ps_scores']['Serve scaled images'],
                    'Specify a Vary:Accept-Encoding'        :test_result['ps_scores']['Specify a Vary:Accept-Encoding'],
                    'Specify a cache validator'             :test_result['ps_scores']['Specify a cache validator'],
                    'Specify a character set'               :test_result['ps_scores']['Specify a character set'],
                    'Use efficient CSS selectors'           :test_result['ps_scores']['Use efficient CSS selectors'],
                }

        # Data for HAR Viewer
        filename = os.path.join( config['app_conf']['temp_store'], har_id )
        file = open(filename, 'w')
        file.write( test_result['har'] )
        file.close()

        # Final JSON
        return json.dumps({'summary'    :summary,
                           'pagespeed'  :scores,
                           'weights'    :har.weight_ratio(),
                           'requests'   :har.req_ratio(),
                           'har'        :har_id,
                            })
        
    def harviewer(self):
        c.url = h.url_for(str('/data/'+request.GET['har']))
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
        else:
            mdb_handler.collection.remove({"url":label,"timestamp":timestamp})

        return ("details?",mode,'=',label)

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
            
            # Add document to collection
            mdb_handler.collection.insert({
                "label"         :har.label,
                "url"           :har.url,
                "timestamp"     :strftime("%Y-%m-%d %H:%M:%S", localtime()),
                "full_load_time":har.full_load_time,
                "total_size"    :har.total_size,
                "requests"      :har.requests,
                "browser"       :har.browser,
                "ps_scores"     :{  'Total Score'                           :100,
                                    'Avoid CSS @import'                     :100,
                                    'Avoid bad requests'                    :100,
                                    'Combine images into CSS sprites'       :100,
                                    'Defer loading of JavaScript'           :100,
                                    'Defer parsing of JavaScript'           :100,
                                    'Enable Keep-Alive'                     :100,
                                    'Enable compression'                    :100,
                                    'Inline small CSS'                      :100,
                                    'Inline small JavaScript'               :100,
                                    'Leverage browser caching'              :100,
                                    'Make redirects cacheable'              :100,
                                    'Minify CSS'                            :100,
                                    'Minify HTML'                           :100,
                                    'Minify JavaScript'                     :100,
                                    'Minimize redirects'                    :100,
                                    'Minimize requests size'                :100,
                                    'Optimize images'                       :100,
                                    'Optimize order of styles and scripts'  :100,
                                    'Prefer asyncronous resources'          :100,
                                    'Put CSS in the document head'          :100,
                                    'Remove query string from statics'      :100,
                                    'Remove unused css'                     :100,
                                    'Serve resources from consistent URL'   :100,
                                    'Serve scaled images'                   :100,
                                    'Specify a Vary:Accept-Encoding'        :100,
                                    'Specify a cache validator'             :100,
                                    'Specify a character set'               :100,
                                    'Use efficient CSS selectors'           :100,
                                },
                "har"           :har.origin
            })
            
            redirect('/')
        else:
            # Display error page
            return render('./upload.html')
