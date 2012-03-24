import json
import time
import re

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

class Bytes(float):

    """
    Extended integer
    """

    def __add__(self, other):
        """
        @return - result of addition
        """

        return Bytes(self.__float__() + other)

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
        """
        Page Speed requires strict date format for every entry and every page.
        Therefor original dates must be modified
        """

        # Entry level
        for entry in har["log"]["entries"]:
            if entry["startedDateTime"].rfind("+") != -1:
                start_ts = entry["startedDateTime"].replace("+", "-")
                entry["startedDateTime"] = start_ts

            long_time, dot, seconds = entry["startedDateTime"].partition(".")
            milliseconds, dash, timezone = seconds.partition("-")
            milliseconds = milliseconds.replace("Z", "")

            entry["startedDateTime"] = long_time + dot + milliseconds + "+00:00"

        # Page level
        for page in har["log"]["pages"]:
            if page["startedDateTime"].rfind("+") != -1:
                start_ts = page["startedDateTime"].replace("+", "-")
                page["startedDateTime"] = start_ts

            long_time, dot, seconds = page["startedDateTime"].partition(".")
            milliseconds, dash, timezone = seconds.partition("-")
            milliseconds = milliseconds.replace("Z", "")

            page["startedDateTime"] = long_time + dot + milliseconds + "+00:00"

        return har

class HAR():

    """
    HAR Parser
    """

    def __init__(self, har, fixed=False):
        """Deserialize HAR file and initialize variables"""

        # Check file size. If size is null it breaks parsing and return
        # error status
        if len(har) == 0:
            self.parsing_status = "Empty file"
        else:
            try:
                if not fixed:
                    # Unfortunately Fidler and Charles Proxy do not
                    # strictly follow HAR 1.2 specification. HttpWatch uses
                    # weird encoding. Trying to fix that when first time meet
                    # the file.
                    har = Fixer.fix_har(har)

                # Deserialize HAR file, fix issues related to Page Speed and
                # store original file for HAR Viewer
                self.har = json.loads(har)
                self.har = Fixer.fix_pagespeed(self.har)
                self.origin = har

                # Initial varaibles and counters
                self.init_variables()

                self.parsing_status = "Successful"

            except Exception as error:
                self.parsing_status = ": ".join([type(error).__name__, error.message])

    def init_variables(self):
        self.full_load_time = 0

        self.total_dns_time      = 0.0
        self.total_transfer_time = 0.0
        self.total_server_time   = 0.0
        self.avg_connecting_time = 0.0
        self.avg_blocking_time   = 0.0

        self.total_size = Bytes(0)
        self.text_size  = Bytes(0)
        self.media_size = Bytes(0)
        self.cache_size = Bytes(0)

        self.redirects    = 0
        self.bad_requests = 0

        self.domains = dict()

    def analyze(self):
        """Extract data from HAR container"""

        # Temporary extremes
        self.min_timestamp = 10 ** 14
        self.max_timestamp = 0

        # Parse each entry of page
        for self.entry in self.har["log"]["entries"]:
            # Micro timgings
            self.total_dns_time      += self.get_dns_time()
            self.total_transfer_time += self.get_transfer_time()
            self.total_server_time   += self.get_server_time()
            self.avg_connecting_time += self.get_connecting_time()
            self.avg_blocking_time   += self.get_blocking_time()

            # Update Request/Page time frame
            self.update_timeframe()

            # Time to first byte
            self.time_to_first_byte = self.get_time_to_first_byte()

            # Size of response body
            self.total_size += self.get_response_size()

            # Size of text (JavaScript, CSS, HTML, XML, JSON, plain text)
            # and media (images, flash) files
            if self.is_text():
                self.text_size += self.get_response_size()
            elif self.is_media():
                self.media_size += self.get_response_size()

            # Cached size
            if self.is_long_term_cache():
                self.cache_size += self.get_response_size()

            # Redirects (3xx) and bad requests (4xx, 5xx)
            if self.is_redirect():
                self.redirects += 1
            elif self.is_bad_request():
                self.bad_requests += 1

            # Update domain info
            self.update_domain_info()

        # Label
        self.label = self.get_label()

        # URL
        self.url = self.get_url()

        # Requests
        self.requests = self.get_number_of_requests()

        # Full load time
        self.full_load_time = self.get_full_load_time()

        # onLoad envent time
        self.onload_event = self.get_onload_event()

        # Render Start
        self.start_render_time = self.get_start_render_time()

        # Average values
        self.avg_connecting_time = self.get_avg_connecting_time()
        self.avg_blocking_time = self.get_avg_blocking_time()

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
                size = Bytes(entry["response"]["content"]["size"])
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

    def get_dns_time(self):
        dns_time = self.entry["timings"]["dns"]
        return max(dns_time, 0)

    def get_transfer_time(self):
        receive_time = max(self.entry["timings"]["receive"], 0)
        send_time = max(self.entry["timings"]["send"], 0)
        return receive_time + send_time

    def get_send_time(self):
        send_time = self.entry["timings"]["send"]
        return max(send_time, 0)

    def get_server_time(self):
        server_time = self.entry["timings"]["wait"]
        return max(server_time, 0)
    
    def get_connecting_time(self):
        connecting_time = self.entry["timings"]["connect"]
        return max(connecting_time, 0)
    
    def get_blocking_time(self):
        blocking_time = self.entry["timings"]["blocked"]
        return max(blocking_time, 0)

    def update_timeframe(self):
        # Original time format: 2000-01-01T00:00:00.000+00:00
        seconds, dot, milliseconds = self.entry["startedDateTime"].partition(".")
        seconds = time.strptime(seconds, "%Y-%m-%dT%H:%M:%S")
        seconds = time.mktime(seconds)

        # Exclude timezone
        try:
            milliseconds = milliseconds.partition("+")[0]
        except:
            milliseconds = milliseconds.partition("-")[0]
        milliseconds = milliseconds.replace("Z", "")

        time_request_started = seconds + float("0." + milliseconds)
        time_request_completed = time_request_started + self.entry["time"]/1000.0

        if time_request_completed > self.max_timestamp:
            self.max_timestamp = time_request_completed

        if time_request_started < self.min_timestamp:
            self.min_timestamp = time_request_started
            self.is_first = True
        else:
            self.is_first = False
            

    def get_time_to_first_byte(self):
        if self.is_first:
            return self.get_blocking_time() + \
                   self.get_dns_time() + \
                   self.get_connecting_time() + \
                   self.get_send_time() + \
                   self.get_server_time()
        else:
            return self.time_to_first_byte

    def get_response_size(self):
        compressed_size = Bytes(max(self.entry["response"]["bodySize"], 0))
        if compressed_size == 0:
            return Bytes(self.entry["response"]["content"]["size"])
        else:
            return compressed_size

    def is_text(self):
        mime_type = self.entry["response"]["content"]["mimeType"].partition(";")[0]
        if cmp(mime_type, ""):
            mime_type = self.get_normalized_value(mime_type)

            if mime_type.count("javascript") \
            or mime_type.count("text") \
            or mime_type.count("html") \
            or mime_type.count("xml") \
            or mime_type.count("json"):
                return True
        return False

    def is_media(self):
        mime_type = self.entry["response"]["content"]["mimeType"].partition(";")[0]

        if cmp(mime_type, ""):
            mime_type = self.get_normalized_value(mime_type)
            if mime_type.count("flash") or mime_type.count("image"):
                return True
        return False

    def is_long_term_cache(self):
        headers = Headers(self.entry["response"]["headers"])

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
                    return True
        except:
            pass
        return False

    def is_redirect(self):
        if self.entry["response"]["status"] >= 300 \
        and self.entry["response"]["status"] < 400:
            return True

    def is_bad_request(self):
        if self.entry["response"]["status"] >= 400:
            return True

    def get_label(self):
        return self.har["log"]["pages"][0]["id"]

    def get_url(self):
        return self.har["log"]["entries"][0]["request"]["url"][:512]

    def get_number_of_requests(self):
        return len(self.har["log"]["entries"])

    def get_full_load_time(self):
        try:
            return self.har["log"]["pages"][0]["pageTimings"]["_myTime"]
        except:
            return int((self.max_timestamp - self.min_timestamp) * 1000)

    def get_onload_event(self):
        try:
            onload_event = self.har["log"]["pages"][0]["pageTimings"]["onLoad"]
            if onload_event > 0:
                return onload_event                
        except TypeError: # dynaTrace bug
            return self.har["log"]["pages"][0]["pageTimings"][0]["onLoad"]
        except KeyError:
            pass        
        return "n/a"

    def get_start_render_time(self):
        try:
            return self.har["log"]["pages"][0]["pageTimings"]["_renderStart"]
        except:
            return "n/a"

    def get_avg_connecting_time(self):
        return round(self.avg_connecting_time / self.requests, 0)        

    def get_avg_blocking_time(self):
        return round(self.avg_blocking_time / self.requests, 0)

    def update_domain_info(self):
        domain = self.entry["request"]["url"].partition("//")[-1].partition("/")[0]

        # WORKAROUND: Mongo prevents using dots in key names
        mongo_domain = re.sub("\.","|", domain)

        # {DOMAIN: [NUMBER OF REQUESTS, TOTAL DATA FROM HOST IN KB], ...}
        domain_requests  = self.domains.get(mongo_domain, [0, 0])[0]
        domain_data_size = self.domains.get(mongo_domain, [0, 0])[1]

        domain_requests  += 1
        domain_data_size += self.get_response_size().to_kilobytes()

        self.domains[mongo_domain] = [domain_requests, domain_data_size]