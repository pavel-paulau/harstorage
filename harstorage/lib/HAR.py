import json
import time
import re

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

class bytes(float):

    """
    Extended integer
    """

    def __add__(self, other):
        """
        @return - result of addition
        """

        return bytes(self.__float__() + other)

    def to_kilobytes(self):
        """
        @return - value in kilobytes
        """

        return int(round(self.__float__()/1024.0))

class Headers():

    """
    Manipulation with HTTP headers
    """

    def __init__(self, headers):
        """
        @parameter headers - list of headers

        @as_dictionary - dictionary of headers
        """

        self.as_dict = dict()
        for header in headers:
            self.as_dict[header["name"]] = header["value"]

class Fixer():

    """
    Fix issues with broken HAR format
    """

    @staticmethod
    def apply_workaround_for_httpwatch(har):
        """HttpWatch workaround"""

        return har.decode("latin-1").encode("utf-8")

    @staticmethod
    def apply_workaround_for_fiddler(har):
        """Fiddler workaround"""

        har = har.partition("{")[1] + har.partition("{")[-1]

        return re.sub('"pages":null',
                      '"pages":[{\
                      "startedDateTime": "1970-01-01T00:00:00.000+00:00",\
                      "id": "Undefined","title": "Undefined",\
                      "pageTimings": {}}]',
                      har)

    @staticmethod
    def apply_workaround_for_charles(har):
        """Charles Proxy workaround"""

        return re.sub('"log":{',
                      '"log": {"pages": [{\
                      "startedDateTime": "1970-01-01T00:00:00.000+00:00",\
                      "id": "Undefined","title": "Undefined",\
                      "pageTimings": {}}],',
                      har)

    @staticmethod
    def fix_har(har):
        """Choose workaround and apply it"""

        if har.rfind('"name" : "HttpWatch') > 0:
            har = Fixer().apply_workaround_for_httpwatch(har)
        elif har.rfind('"name":"Fiddler"') > 0:
            har = Fixer().apply_workaround_for_fiddler(har)
        elif har.rfind('"name":"Charles Proxy"') > 0:
            har = Fixer().apply_workaround_for_charles(har)

        return har

    @staticmethod
    def fix_pagespeed(har):
        """Page Speed workaround"""

        # Entry level
        for entry in har["log"]["entries"]:
            if entry["startedDateTime"].rfind("+") != -1:
                start_ts = entry["startedDateTime"].replace("+", "-")
                entry["startedDateTime"] = start_ts

            long_time, dot, seconds = entry["startedDateTime"].partition(".")
            milliseconds, dash, timezone = seconds.partition("-")

            entry["startedDateTime"] = long_time + dot + milliseconds + "+00:00"

        # Page level
        for page in har["log"]["pages"]:
            if page["startedDateTime"].rfind("+") != -1:
                start_ts = page["startedDateTime"].replace("+", "-")
                page["startedDateTime"] = start_ts

            long_time, dot, seconds = page["startedDateTime"].partition(".")
            milliseconds, dash, timezone = seconds.partition("-")

            page["startedDateTime"] = long_time + dot + milliseconds + "+00:00"

        return har

class HAR():

    """
    HAR Parser
    """

    def __init__(self, har, fixed=False):
        """Deserialize HAR file and initialize variables"""

        # Check file size
        if len(har) == 0:
            self.parsing_status = "Empty file"
        else:
            try:
                if not fixed:
                    # Fix Fidler, HttpWatch and Charles Proxy issues
                    har = Fixer.fix_har(har)

                # Deserialize HAR file            
                self.har = json.loads(har)
                self.origin = har

                # Fix Page Speed issues with timezones
                self.har = Fixer.fix_pagespeed(self.har)

                # Initial varaibles and counters
                self.full_load_time = 0

                self.total_dns_time      = 0.0
                self.total_transfer_time = 0.0
                self.total_server_time   = 0.0
                self.avg_connecting_time = 0.0
                self.avg_blocking_time   = 0.0

                self.total_size = bytes(0)
                self.text_size  = bytes(0)
                self.media_size = bytes(0)
                self.cache_size = bytes(0)

                self.redirects    = 0
                self.bad_requests = 0

                self.domains = dict()

                # Parsing status
                self.parsing_status = "Successful"
                
            except Exception as error:
                self.parsing_status = error
    
    

    def analyze(self):
        """Extract data from HAR container"""

        # Temporary variables
        min_ts = 10 ** 14
        max_ts = 0

        # Parse each entry of page
        for entry in self.har["log"]["entries"]:
            # Detailed timgings
            dns_time        = max(entry["timings"]["dns"], 0)
            transfer_time   = entry["timings"]["receive"] + entry["timings"]["send"]
            transfer_time   = max(transfer_time, 0)
            server_time     = max(entry["timings"]["wait"], 0)
            connecting_time = max(entry["timings"]["connect"], 0)
            blocking_time   = max(entry["timings"]["blocked"], 0)

            self.total_dns_time      += dns_time
            self.total_transfer_time += transfer_time
            self.total_server_time   += server_time
            self.avg_connecting_time += connecting_time
            self.avg_blocking_time   += blocking_time

            # Full load time and time to first byte
            start_time = time.mktime(time.strptime(
                    entry["startedDateTime"].partition(".")[0],
                    "%Y-%m-%dT%H:%M:%S"))
            
            try:
                start_ts = entry["startedDateTime"].partition(".")[-1].partition("+")[0]
            except:
                start_ts = entry["startedDateTime"].partition(".")[-1].partition("-")[0]
            start_time += float("0." + start_ts)
            
            end_time = start_time + entry["time"]/1000.0
    
            if start_time < min_ts:
                min_ts = start_time
                self.time_to_first_byte = blocking_time + \
                                          dns_time + \
                                          connecting_time + \
                                          entry["timings"]["send"] + \
                                          server_time

            if end_time > max_ts:
                max_ts = end_time

            # Size of response body
            compressed_size = bytes(max(entry["response"]["bodySize"], 0))
            if compressed_size == 0:
                size = bytes(entry["response"]["content"]["size"])
            else:
                size = compressed_size

            self.total_size += size
            
            # Size of text (JavaScript, CSS, HTML, XML, JSON, plain text)
            # and media (images, flash) files
            mime_type = entry["response"]["content"]["mimeType"].partition(";")[0]
            if cmp(mime_type,""):
                mime_type = self.get_normalized_value(mime_type)
                
                if mime_type.count("javascript") \
                or mime_type.count("text") \
                or mime_type.count("html") \
                or mime_type.count("xml") \
                or mime_type.count("json"):
                    self.text_size += size
                elif mime_type.count("flash") or mime_type.count("image"):
                    self.media_size += size

            # Cached size
            headers = Headers(entry["response"]["headers"])

            try:
                cache_control = headers.as_dict["Cache-Control"]

                if not cache_control.count("no-cache") \
                and not cache_control.count("max-age=0"):

                    # Extract DATE from HTTP header
                    date = headers.as_dict["Date"]
                    date = time.strptime(date, DATE_FORMAT)
                    date = time.mktime(date)

                    # Extract EXPIRES from HTTP header
                    expires = headers.as_dict["Expires"]
                    expires = time.strptime(expires, DATE_FORMAT)
                    expires = time.mktime(expires)

                    if expires > date:
                        self.cache_size += size
            except:
                pass

            # Redirects and bad requests
            if entry["response"]["status"] >= 300 and entry["response"]["status"] < 400:
                self.redirects += 1
            elif entry["response"]["status"] >= 400:
                self.bad_requests += 1
                
            # List of hosts
            hostname = entry["request"]["url"].partition("//")[-1].partition("/")[0]

            md_hostname = re.sub("\.","|", hostname)

            self.domains[md_hostname] = [
                self.domains.get(md_hostname, [0,0])[0] + 1,
                self.domains.get(md_hostname, [0,0])[1] + size.to_kilobytes()
            ]

        # Label
        self.label = self.har["log"]["pages"][0]["id"]

        # URL
        self.url = self.har["log"]["entries"][0]["request"]["url"]

        # Requests
        self.requests = len( self.har["log"]["entries"] )

        # Full load time
        try:
            self.full_load_time = self.har["log"]["pages"][0]["pageTimings"]["_myTime"]
        except:
            self.full_load_time = int((max_ts - min_ts)*1000)

        # onLoad envent time
        try:
            self.onload_event = self.har["log"]["pages"][0]["pageTimings"]["onLoad"]
        except:
            try:
                self.onload_event = self.har["log"]["pages"][0]["pageTimings"][0]["onLoad"] # dynaTrace bug
            except:                
                self.onload_event = "n/a"

        # Render Start
        try:
            self.start_render_time = self.har["log"]["pages"][0]["pageTimings"]["_renderStart"]
        except:
            self.start_render_time = "n/a"

        # Average values
        self.avg_connecting_time = round(self.avg_connecting_time / self.requests, 0)
        self.avg_blocking_time = round(self.avg_blocking_time / self.requests, 0)

        # From bytes to kilobytes
        self.total_size = self.total_size.to_kilobytes()
        self.text_size  = self.text_size.to_kilobytes()
        self.media_size = self.media_size.to_kilobytes()
        self.cache_size = self.cache_size.to_kilobytes()
       
    def weight_ratio(self):
        """Breakdown by size of page objects"""

        resources = dict()        
        for entry in self.har["log"]["entries"]:
            mime_type = entry["response"]["content"]["mimeType"].partition(";")[0]
            if cmp(mime_type, ""):
                mime_type = self.get_normalized_value(mime_type)
                size = bytes(entry["response"]["content"]["size"])
                resources[mime_type] = resources.get(mime_type, 0) + size.to_kilobytes()
        return resources
        
    def req_ratio(self):
        """Breakdown by number of page objects"""
        
        resources = dict()
        for entry in self.har["log"]["entries"]:
            mime_type = entry["response"]["content"]["mimeType"].partition(";")[0]
            if cmp(mime_type, ""):
                mime_type = self.get_normalized_value(mime_type)
                resources[mime_type] = resources.get(mime_type, 0) + 1
        return resources

    def get_normalized_value(self, string):
        """
        @parameter string - MIME type

        @return - normilized MIME type
        """

        if string.count("javascript"):
            return "javascript"
        elif string.count("flash"):
            return "flash"
        elif string.count("text/plain") or string.count("html"):
            return "text/html"
        elif string.count("xml"):
            return "text/xml"
        elif string.count("css"):
            return "text/css"
        elif string.count("gif"):
            return "image/gif"
        elif string.count("png"):
            return "image/png"
        elif string.count("jpeg") or string.count("jpg"):
            return "image/jpeg"
        elif string.count("json"):
            return "json"
        else:
            return "other"