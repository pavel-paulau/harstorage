import json
from time import strptime, mktime
from math import ceil
from re import sub

class HAR():
    def __init__(self,har):
        try:
            # Base case
            self.har = json.loads(har)
            self.origin = har
            self.status = 'Ok'
        except:
            try:
                # Fix for latin-1
                self.har = json.loads(har.decode('latin-1').encode('utf-8'))
                self.origin = har.decode('latin-1').encode('utf-8')
                self.status = 'Ok'
            except:
                try:
                    # Fix for unicode
                    temp = sub("'","\"", sub("u'","\"", har) )
                    self.har = json.loads( temp )
                    self.origin = temp 
                    self.status = 'Ok'
                except:
                    self.status = "Failed to read HAR"
                    
        self.total_size = self.text_size = self.media_size = self.cached = 0
        self.full_load_time = self.dns = self.transfer = self.connecting = self.server = self.blocked = 0
        self.redirects = self.bad_req = 0
        self.hosts = 0
    
    # Convert Bytes to Kilobytes
    def b2k(self,value):
        return int( ceil( value/1024 ) )
    
    # Convert headers list to headers dictionary
    def h2d(self,headers):
        hd = dict()
        for header in headers:
            hd[header['name']] = header['value']
        return hd
    
    def analyze(self):
        # Label
        self.label = self.har['log']['pages'][0]['id']

        # URL
        self.url = self.har['log']['entries'][0]['request']['url']
        
        # Browser
        self.browser = self.har['log']['browser']['name']
        
        # Requests
        self.requests = len( self.har['log']['entries'] )
        
        min = 9999999999
        max = 0
        
        hosts = list()
        
        for entry in self.har['log']['entries']:
            # Full load time
            start_time = mktime( strptime(entry['startedDateTime'].partition('.')[0], "%Y-%m-%dT%H:%M:%S") )
            start_time += float( entry['startedDateTime'].partition('.')[2].partition('+')[0] ) / 1000
            
            end_time =  start_time + entry['time']/1000
    
            if start_time < min: min = start_time
            if end_time > max: max = end_time
        
            # Detailed timgings
            self.dns += entry['timings']['dns']
            self.transfer += entry['timings']['receive'] + entry['timings']['send']
            self.server += entry['timings']['wait']
            self.connecting += entry['timings']['connect']
            self.blocked += entry['timings']['blocked']
            
            # Total size
            self.total_size += entry['response']['bodySize']
            
            # Text and media sizes
            mime_type = entry['response']['content']['mimeType'].partition(';')[0]
            if cmp(mime_type,''):
                mime_type = self.type_syn(mime_type)
                
                if mime_type.count('javascript') \
                or mime_type.count('text') \
                or mime_type.count('html') \
                or mime_type.count('xml') \
                or mime_type.count('json'):
                    self.text_size += entry['response']['bodySize']
                elif mime_type.count('flash') or mime_type.count('image'):
                    self.media_size += entry['response']['bodySize']
            
            # Cached size
            resp_headers = self.h2d(entry['response']['headers'])
            
            try:
                if not resp_headers['Cache-Control'].count('no-cache') \
                and not resp_headers['Cache-Control'].count('max-age=0'):                
                    date    = mktime( strptime(resp_headers['Date'],"%a, %d %b %Y %H:%M:%S GMT") )
                    expires = mktime( strptime(resp_headers['Expires'],"%a, %d %b %Y %H:%M:%S GMT") )
                    if expires > date:
                        self.cached += entry['response']['bodySize']
            except:
                pass
                    
            # Redirects and bad requests
            if entry['response']['status'] >=300 and entry['response']['status'] < 400:
                self.redirects += 1
            elif entry['response']['status']>=400:
                self.bad_req += 1
                
            # List of hosts
            for header in entry['request']['headers']:
                if header['name'] == 'Host':
                    if header['value'] not in hosts:
                        hosts.append( header['value'] )
            
        # Full load time
        self.full_load_time = int( (max - min)*1000 )
        
        # Average values
        self.connecting = self.connecting / self.requests
        self.blocked    = self.blocked / self.requests
        
        # From bytes to kilobytes
        self.total_size = self.b2k( self.total_size )
        self.text_size  = self.b2k( self.text_size  )
        self.media_size = self.b2k( self.media_size )
        self.cached     = self.b2k( self.cached     )
        
        # Hosts count
        self.hosts = len(hosts)
    
    def type_syn(self,string):
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
                try:
                    resources[mime_type] += size / 1024
                except:
                    resources[mime_type] = size / 1024
        return resources
        
    def req_ratio(self):
        resources = dict()        
        for entry in self.har['log']['entries']:
            mime_type = entry['response']['content']['mimeType'].partition(';')[0]
            if cmp(mime_type,''):
                mime_type = self.type_syn(mime_type)
                try:
                    resources[mime_type] += 1
                except:
                    resources[mime_type] = 1
        return resources