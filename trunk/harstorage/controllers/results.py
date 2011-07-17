import logging
import json

from harstorage.lib.HAR import HAR
from harstorage.lib.MongoHandler import MongoHandler

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

    def timeline(self,label):
        my_session  = model.meta.Session
   
        testresults = my_session.query(TestResults)
        labels      = my_session.query(Labels)
        pagespeed   = my_session.query(PageSpeed)

        label_id = labels.filter_by(label = label).first().id
    
        c.time_hash     = dict()
        c.size_hash     = dict()
        c.requests_hash = dict()
        c.score_hash    = dict()
        c.timestamp     = list()
        for result in testresults.filter_by(label_id = label_id).order_by(model.testresults_table.c.timestamp.desc()).all():
            c.time_hash[result.timestamp]       = result.time
            c.size_hash[result.timestamp]       = result.size
            c.requests_hash[result.timestamp]   = result.requests
            c.score_hash[result.timestamp]      = pagespeed.filter_by(id = result.pagespeed_id).first().score

            c.timestamp.append(result.timestamp)

    def harviewer(self):
        return render('./harviewer.html')

    def details(self):
        c.label = request.GET['label']
        self.timeline(c.label)
            
        return render('./details.html')

    def runinfo(self):
        timestamp = request.POST['timestamp']

        my_session  = model.meta.Session
        testresults = my_session.query(TestResults)
        pagespeed   = my_session.query(PageSpeed)

        pagespeed_id    = testresults.filter_by(timestamp = timestamp).first().pagespeed_id
        har_key         = testresults.filter_by(timestamp = timestamp).first().har_key
        
        har = HAR(MongoHandler().read_from_mongo(har_key))
        
        summary = {'score':pagespeed.filter_by(id = pagespeed_id).first().score,
                    'time':testresults.filter_by(timestamp = timestamp).first().time,
                    'size':testresults.filter_by(timestamp = timestamp).first().size,
                    'requests':testresults.filter_by(timestamp = timestamp).first().requests,
                    }
        
        weights = dict()
        for type,size in har.weight_ratio().items():
            weights[type] = size

        requests = dict()
        for type,num in har.req_ratio().items():
            requests[type] = num



        scores =  {'Avoid CSS @import':pagespeed.filter_by(id = pagespeed_id).first().avoid_import,
                            'Avoid bad requests':pagespeed.filter_by(id = pagespeed_id).first().avoid_bad_req,
                            'Combine images into CSS sprites':pagespeed.filter_by(id = pagespeed_id).first().combine_images,
                            'Defer loading of JavaScript':pagespeed.filter_by(id = pagespeed_id).first().defer_load_js,
                            'Defer parsing of JavaScript':pagespeed.filter_by(id = pagespeed_id).first().defer_pars_js,
                            'Enable Keep-Alive':pagespeed.filter_by(id = pagespeed_id).first().enable_keepalive,
                            'Enable compression':pagespeed.filter_by(id = pagespeed_id).first().enable_gzip,
                            'Inline small CSS':pagespeed.filter_by(id = pagespeed_id).first().inline_css,
                            'Inline small JavaScript':pagespeed.filter_by(id = pagespeed_id).first().inline_js,
                            'Leverage browser caching':pagespeed.filter_by(id = pagespeed_id).first().leverage_cache,
                            'Make redirects cacheable':pagespeed.filter_by(id = pagespeed_id).first().make_redirects_cacheable,
                            'Minify CSS':pagespeed.filter_by(id = pagespeed_id).first().minify_css,
                            'Minify HTML':pagespeed.filter_by(id = pagespeed_id).first().minify_html,
                            'Minify JavaScript':pagespeed.filter_by(id = pagespeed_id).first().minify_js,
                            'Minimize redirects':pagespeed.filter_by(id = pagespeed_id).first().minimize_redirects,
                            'Minimize requests size':pagespeed.filter_by(id = pagespeed_id).first().minimize_req_size,
                            'Optimize images':pagespeed.filter_by(id = pagespeed_id).first().optimize_images,
                            'Optimize order of styles and scripts':pagespeed.filter_by(id = pagespeed_id).first().optimize_order,
                            'Prefer asyncronous resources':pagespeed.filter_by(id = pagespeed_id).first().prefer_async,
                            'Put CSS in the document head':pagespeed.filter_by(id = pagespeed_id).first().put_css_in_head,
                            'Remove query string from statics':pagespeed.filter_by(id = pagespeed_id).first().remove_query_string,
                            'Remove unused css':pagespeed.filter_by(id = pagespeed_id).first().remove_unused_css,
                            'Serve resources from consistent URL':pagespeed.filter_by(id = pagespeed_id).first().serve_from_consistent_url,
                            'Serve scaled images':pagespeed.filter_by(id = pagespeed_id).first().serve_scaled_images,
                            'Specify a Vary:Accept-Encoding':pagespeed.filter_by(id = pagespeed_id).first().specify_vary,
                            'Specify a cache validator':pagespeed.filter_by(id = pagespeed_id).first().specify_cache_validator,
                            'Specify a character set':pagespeed.filter_by(id = pagespeed_id).first().specify_char_set,
                            'Use efficient CSS selectors':pagespeed.filter_by(id = pagespeed_id).first().use_efficient_selectors,
                            }
        


        return json.dumps({'summary'    :summary,
                           'pagespeed'  :scores,
                           'weights'    :weights,
                           'requests'   :requests
                            })
        
    def search(self):
        c.search_text = request.POST['search_text']
        return render('./search.html')

    def upload(self):
        return render('./upload.html')
