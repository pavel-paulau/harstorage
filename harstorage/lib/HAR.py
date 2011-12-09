import json
from time import strptime, mktime
from re import sub

class HAR():
    def __init__(self, har):
        # Fix Fidler HAR format
        har = sub(
                '"pages":null',
                '"pages":[{\
                    "startedDateTime":"1970-01-01T00:00:00.000+03:00",\
                    "id":"Undefined",\
                    "title":"Undefined",\
                    "pageTimings": {}\
                }]',
                har)

        # Parsing
        try:
            self.har = json.loads(har)
            self.origin = har
            self.status = 'Successful'
        except ValueError as error:
            if len(har) == 0:
                self.status = 'Empty file'
            else:
                try:
                    self.har = json.loads(har.decode('latin-1').encode('utf-8'))
                    self.origin = har.decode('latin-1').encode('utf-8')
                    self.status = 'Successful'
                except Exception as error:
                    self.status = error            
        finally:
            self.full_load_time         = 0

            self.total_dns_time         = 0.0
            self.total_transfer_time    = 0.0
            self.total_server_time      = 0.0
            self.avg_connecting_time    = 0.0
            self.avg_blocking_time      = 0.0

            self.total_size             = 0.0
            self.text_size              = 0.0
            self.media_size             = 0.0
            self.cache_size             = 0.0

            self.redirects              = 0
            self.bad_requests           = 0
            
            self.domains = dict()
    
    # Convert bytes to kilobytes
    def b2k(self, value):
        return int( round( value/1024.0 ) )
    
    # Convert headers list to headers dictionary
    def h2d(self, headers):
        hd = dict()
        for header in headers:
            hd[header['name']] = header['value']
        return hd
    
    def analyze(self):
        # Fix Charles proxy format
        try:
            self.har['log']['pages']
        except:
            self.har['log']['pages'] = [{"startedDateTime":"1970-01-01T00:00:00.000+03:00",
                                         "id":"Undefined",
                                         "title":"Undefined",
                                         "pageTimings": {}
                                        }]

        # Temporary variables
        min_ts = 9999999999
        max_ts = 0
        
        for entry in self.har['log']['entries']:
            # Detailed timgings
            dns_time        = max( entry['timings']['dns'],                                0)
            transder_time   = max( entry['timings']['receive'] + entry['timings']['send'], 0)
            server_time     = max( entry['timings']['wait'],                               0)
            connecting_time = max( entry['timings']['connect'],                            0)
            blocking_time   = max( entry['timings']['blocked'],                            0)

            self.total_dns_time         += dns_time
            self.total_transfer_time    += transder_time
            self.total_server_time      += server_time
            self.avg_connecting_time    += connecting_time
            self.avg_blocking_time      += blocking_time

            # Full load time and time to first byte
            start_time = mktime( strptime(entry['startedDateTime'].partition('.')[0], "%Y-%m-%dT%H:%M:%S") )
            try:
                start_time += float( '0.' + entry['startedDateTime'].partition('.')[2].partition('+')[0] )
            except:
                start_time += float( '0.' + entry['startedDateTime'].partition('.')[2].partition('-')[0] )
            
            end_time =  start_time + entry['time']/1000.0
    
            if start_time < min_ts:
                min_ts = start_time
                self.time_to_first_byte = blocking_time + \
                                          dns_time + \
                                          connecting_time + \
                                          entry['timings']['send'] + \
                                          server_time

            if end_time > max_ts:
                max_ts = end_time

            # Total size
            size = entry['response']['bodySize']

            self.total_size += size
            
            # Text and media sizes
            mime_type = entry['response']['content']['mimeType'].partition(';')[0]
            if cmp(mime_type,''):
                mime_type = self.type_syn(mime_type)
                
                if mime_type.count('javascript') \
                or mime_type.count('text') \
                or mime_type.count('html') \
                or mime_type.count('xml') \
                or mime_type.count('json'):
                    self.text_size += size
                elif mime_type.count('flash') or mime_type.count('image'):
                    self.media_size += size
            
            # Cached size
            resp_headers = self.h2d(entry['response']['headers'])
            
            try:
                if not resp_headers['Cache-Control'].count('no-cache') \
                and not resp_headers['Cache-Control'].count('max-age=0'):                
                    date    = mktime( strptime(resp_headers['Date'],"%a, %d %b %Y %H:%M:%S GMT") )
                    expires = mktime( strptime(resp_headers['Expires'],"%a, %d %b %Y %H:%M:%S GMT") )
                    if expires > date:
                        self.cache_size += size
            except:
                pass
                    
            # Redirects and bad requests
            if entry['response']['status'] >=300 and entry['response']['status'] < 400:
                self.redirects += 1
            elif entry['response']['status']>=400:
                self.bad_requests += 1
                
            # List of hosts
            for header in entry['request']['headers']:
                if header['name'] == 'Host':
                    hostname = header['value']
                    self.domains[hostname] = [self.domains.get(hostname, [0,0])[0] + 1,
                                              self.domains.get(hostname, [0,0])[1] + self.b2k(size)]

        # Label
        self.label = self.har['log']['pages'][0]['id']

        # URL
        self.url = self.har['log']['entries'][0]['request']['url']

        # Requests
        self.requests = len( self.har['log']['entries'] )

        # Full load time
        try:
            self.full_load_time = self.har['log']['pages'][0]['pageTimings']['_myTime']
        except:
            self.full_load_time = int( (max_ts - min_ts)*1000 )

        # onLoad envent time
        try:
            self.onload_event = self.har['log']['pages'][0]['pageTimings']['onLoad']
        except:
            self.onload_event = 'n/a'

        # Render Start
        try:
            self.start_render_time = self.har['log']['pages'][0]['pageTimings']['_renderStart']
        except:
            self.start_render_time = 'n/a'

        # Average values
        self.avg_connecting_time = round(self.avg_connecting_time / self.requests,  0)
        self.avg_blocking_time   = round(self.avg_blocking_time    / self.requests, 0)
        
        # From bytes to kilobytes
        self.total_size = self.b2k( self.total_size )
        self.text_size  = self.b2k( self.text_size  )
        self.media_size = self.b2k( self.media_size )
        self.cache_size = self.b2k( self.cache_size )
    
    def type_syn(self, string):
        if string.count('javascript'):
            return 'javascript'
        elif string.count('flash'):
            return 'flash'
        elif string.count('text/plain') or string.count('html'):
            return 'text/html'
        elif string.count('xml'):
            return 'text/xml'
        elif string.count('css'):
            return 'text/css'
        elif string.count('gif'):
            return 'image/gif'
        elif string.count('png'):
            return 'image/png'
        elif string.count('jpeg') or string.count('jpg'):
            return 'image/jpeg'
        elif string.count('json'):
            return 'json'
        else:
            return 'other'
       
    def weight_ratio(self):
        resources = dict()        
        for entry in self.har['log']['entries']:
            mime_type = entry['response']['content']['mimeType'].partition(';')[0]
            if cmp(mime_type,''):
                mime_type = self.type_syn(mime_type)
                size = entry['response']['content']['size']
                resources[mime_type] = resources.get(mime_type,0) + self.b2k(size)
        return resources
        
    def req_ratio(self):
        resources = dict()        
        for entry in self.har['log']['entries']:
            mime_type = entry['response']['content']['mimeType'].partition(';')[0]
            if cmp(mime_type,''):
                mime_type = self.type_syn(mime_type)
                resources[mime_type] = resources.get(mime_type,0) + 1
        return resources