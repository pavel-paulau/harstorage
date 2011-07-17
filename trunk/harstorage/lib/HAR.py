import json
from time import strftime, strptime, mktime
from math import ceil

class HAR():
    def __init__(self,har):
        try:
            self.har = json.loads(har)
            self.status = 'Ok'
        except:
            self.status = "Failed to read HAR"
    
    def total_size(self):
        size = 0.0
        for entry in self.har['log']['entries']:
            size += entry['response']['bodySize']
        return int( ceil( size/1024 ) )

    def req_num(self):
        return len( self.har['log']['entries'] )

    def full_time(self):
        min = 9999999999
        max = 0
        for entry in self.har['log']['entries']:
            start_time = mktime(strptime(entry['startedDateTime'].partition('.')[0], "%Y-%m-%dT%H:%M:%S"))
            start_time += float( entry['startedDateTime'].partition('.')[2].partition('+')[0] ) / 1000
            
            end_time =  start_time +  entry['time']/1000
    
            if start_time < min: min = start_time
            if end_time > max: max = end_time

        return (max - min)*1000
        
    def weight_ratio(self):
        resources = dict()        
        for entry in self.har['log']['entries']:
            type = entry['response']['content']['mimeType'].partition(';')[0]
            size = entry['response']['content']['size']
            try:
                resources[type] += size
            except:
                resources[type] = size
        return resources
        
    def req_ratio(self):
        resources = dict()        
        for entry in self.har['log']['entries']:
            type = entry['response']['content']['mimeType'].partition(';')[0]
            try:
                resources[type] += 1
            except:
                resources[type] = 1
        return resources
