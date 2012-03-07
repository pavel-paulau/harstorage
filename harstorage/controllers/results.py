import json
import os
import hashlib
import mimetypes
import time
import re
import functools
import platform

from pylons import request, response, tmpl_context as c
from pylons import config
from pylons.controllers.util import redirect
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController, render
from harstorage.lib.HAR import HAR
from harstorage.lib.MongoHandler import MongoDB

class ResultsController(BaseController):

    """
    Core controller of repository
    """

    def __before__(self):
        """Define version of static content"""

        c.rev = config["app_conf"]["static_version"]

    @restrict("GET")
    def index(self):
        """Home page with the latest test results"""

        # Migration (harstorage v1.0)
        migration_handler = MongoDB(collection = "migration")
        if hasattr(c, "message"): return render("/error.html")

        status = migration_handler.collection.find_one({"status": "ok"})
        if status is None: redirect("/migration/status")

        # MongoDB handler
        mdb_handler = MongoDB()
        if hasattr(c, "message"): return render("/error.html")

        # Read aggregated data from database
        # Aggregation is based on unique labels, urls and latest timestamps
        latest_results = mdb_handler.collection.group(
            key = ["label", "url"],
            condition = None,
            initial = {"timestamp": "1970-01-01 01:00:00"},
            reduce = "\
                function(doc, prev) {                     \
                    if (doc.timestamp > prev.timestamp) { \
                        prev.timestamp = doc.timestamp;   \
                    }                                     \
                }")

        key = lambda timestamp: timestamp["timestamp"]
        latest_results = sorted(latest_results, key = key, reverse = True)

        # Numner of records
        c.rowcount = len(latest_results)

        # Populate data table with the latest test results
        c.metrics_table = [[], [], [], [], [], []]

        fields = ["timestamp", "label", "url", "total_size", "requests",
                    "full_load_time"]

        for group in latest_results:
            condition = {"label": group["label"], "timestamp": group["timestamp"]}

            result = mdb_handler.collection.find_one(condition, fields = fields)

            c.metrics_table[0].append(result["timestamp"])
            c.metrics_table[1].append(result["label"])
            c.metrics_table[2].append(result["url"])
            c.metrics_table[3].append(result["total_size"])
            c.metrics_table[4].append(result["requests"])
            c.metrics_table[5].append(round(result["full_load_time"]/1000.0, 1))

        return render("/home/core.html")

    @restrict("GET")
    def details(self):
        """Page with test results"""

        # Try to fetch data for selecetor box
        try:
            c.label = request.GET["url"]
            c.mode = "url"
        # Use label parameter instead of URL parameter
        except:
            c.label = request.GET["label"]
            c.mode = "label"

        # Generate context for selector
        self._set_options_in_selector(c.mode, c.label)

        # Define url for data aggregation
        if c.mode == "label":
            c.query = "/superposed/display?" + \
                      "step_1_label=" + c.label + \
                      "&step_1_start_ts=" + min(c.timestamp) + \
                      "&step_1_end_ts=" + max(c.timestamp)
            c.histo = "true"
        else:
            c.histo = "false"
            c.query = "None"
 
        return render("/details/core.html")
    
    def _set_options_in_selector(self, mode, label):
        """
        Create context data - a list of timestamps.

        @parameter label - label of set with test results
        @parameter url   - URL of set with test results
        """

        # Read data for selector box from database
        results = MongoDB().collection.find(
            {mode: label},
            fields = ["timestamp"],
            sort = [("timestamp", -1)])

        c.timestamp = list()

        for result in results:
            c.timestamp.append(result["timestamp"])


    @restrict("GET")
    def timeline(self):
        """Generate data for timeline chart"""

        # Parameters from GET request
        label = request.GET["label"]
        mode = request.GET["mode"]

        # Metrics
        METRICS = ( "timestamp", "full_load_time", "requests", "total_size",
                    "ps_scores", "onload_event", "start_render_time",
                    "time_to_first_byte", "total_dns_time",
                    "total_transfer_time", "total_server_time",
                    "avg_connecting_time", "avg_blocking_time", "text_size",
                    "media_size", "cache_size", "redirects", "bad_requests",
                    "domains")

        TITLES = [ "Full Load Time", "Total Requests",
                   "Total Size", "Page Speed Score", "onLoad Event",
                   "Start Render Time", "Time to First Byte",
                   "Total DNS Time", "Total Transfer Time", "Total Server Time",
                   "Avg. Connecting Time", "Avg. Blocking Time", "Text Size",
                   "Media Size", "Cache Size", "Redirects", "Bad Rquests",
                   "Domains"]

        # Set of metrics to exclude (due to missing data)
        exclude = set()
        data = list()
        for index in range(len(METRICS)):
            data.append(str())

        # Read data for timeline from database in custom format (hash separated)
        results = MongoDB().collection.find(
            {mode: label},
            fields = METRICS,
            sort = [("timestamp", 1)])

        for result in results:
            index = 0
            for metric in METRICS:
                if metric != "ps_scores":
                    point = str(result[metric])
                else:
                    point = str(result[metric]["Total Score"])
                if point == "n/a":
                    exclude.add(metric)
                data[index] += point + "#"
                index += 1

        # Update list of titles
        if "onload_event" in exclude:
            TITLES.pop(TITLES.index("onLoad Event"))
        if "start_render_time" in exclude:
            TITLES.pop(TITLES.index("Start Render Time"))

        header = str()
        for title in TITLES:
            header += title + "#"

        output = header[:-1] + ";"

        for dataset in data:
            if not dataset.count("n/a"):
                output += dataset[:-1] + ";"

        return output[:-1]

    @restrict("GET")
    def runinfo(self):
        """Generate detailed data for each test run"""

        # Parameters from GET request
        timestamp = request.GET["timestamp"]

        # DB query
        test_results = MongoDB().collection.find_one({"timestamp": timestamp})

        # Domains breakdown
        domains_req_ratio = dict()
        domains_weight_ratio = dict()

        for hostname, value in test_results["domains_ratio"].items():
            hostname = re.sub("\|", ".", hostname)
            domains_req_ratio[hostname] = value[0]
            domains_weight_ratio[hostname] = value[1]

        # Summary stats
        summary = { "full_load_time":       test_results["full_load_time"],
                    "onload_event":         test_results["onload_event"],
                    "start_render_time":    test_results["start_render_time"],
                    "time_to_first_byte":   test_results["time_to_first_byte"],
                    "total_dns_time":       test_results["total_dns_time"],
                    "total_transfer_time":  test_results["total_transfer_time"],
                    "total_server_time":    test_results["total_server_time"],
                    "avg_connecting_time":  test_results["avg_connecting_time"],
                    "avg_blocking_time":    test_results["avg_blocking_time"],
                    "total_size":           test_results["total_size"],
                    "text_size":            test_results["text_size"],
                    "media_size":           test_results["media_size"],
                    "cache_size":           test_results["cache_size"],
                    "requests":             test_results["requests"],
                    "redirects":            test_results["redirects"],
                    "bad_requests":         test_results["bad_requests"],
                    "domains":              test_results["domains"]}

        # Page Speed Scores
        scores = dict()
        for rule, score in test_results["ps_scores"].items():
            scores[rule] = score

        # Data for HAR Viewer
        har_id = str(test_results["_id"])

        filename = os.path.join(config["app_conf"]["temp_store"], har_id)
        with open(filename, "w") as file:
            file.write(test_results["har"].encode("utf-8"))

        # Final JSON
        return json.dumps({"summary":       summary,
                           "pagespeed":     scores,
                           "weights":       test_results["weights_ratio"],
                           "requests":      test_results["requests_ratio"],
                           "d_weights":     domains_weight_ratio,
                           "d_requests":    domains_req_ratio,
                           "har":           har_id})

    @restrict("GET")
    def harviewer(self):
        """HAR Viewer iframe"""

        # HAR Viewer customization via cookie
        response.set_cookie("phaseInterval", "-1", max_age=365*24*3600 )

        return render("/harviewer.html")
    
    @restrict("GET")
    def deleterun(self):
        """Controller for deletion of tests"""

        # MongoDB handler
        mdb_handler = MongoDB()

        # Parameters from GET request
        label = request.GET["label"]
        timestamp = request.GET["timestamp"]
        mode = request.GET["mode"]

        if request.GET["all"] == "true":
            all = True
        else:
            all = False
            
        # Remove document from collection
        if mode == "label":
            if all:
                mdb_handler.collection.remove({"label": label})
            else:
                mdb_handler.collection.remove({"label": label, "timestamp": timestamp})
            count = mdb_handler.collection.find({"label": label}).count()
        else:
            if all:
                mdb_handler.collection.remove({"url": label})
            else:
                mdb_handler.collection.remove({"url": label, "timestamp":timestamp})
            count = mdb_handler.collection.find({"url": label}).count()

        if count:
            return ("details?" + mode + "=" + label)
        else:
            return ("/")

    def upload_rest(function):
        @functools.wraps(function)
        def wrapper(*args):
            result, ext = function(*args)

            if result == True:
                try:
                    if request.headers["automated"] == "true":
                        return "Successful"
                except KeyError:
                    redirect("/results/details?label=" + ext)
            else:
                try:
                    if request.headers["automated"] == "true":
                        return ext
                except KeyError:
                    c.error = ext
                    return render("/upload.html")

        return wrapper

    @restrict("POST")
    @upload_rest
    def upload(self):
        """Controller for uploads of new test results"""

        # HAR initialization
        try:
            har = HAR(request.POST["file"].value)
        except:
            har = HAR(request.POST["file"])
        
        # Analysis of uploaded data
        if har.parsing_status == "Successful":
            # Parsing imported HAR file
            try:
                har.analyze()
            except Exception as error:
                return False, ": ".join([type(error).__name__, error.message])
            
            # Evaluate Page Speed scores
            if config["app_conf"]["ps_enabled"] == "true":
                scores = self._get_pagespeed_scores(har.har)
            else:
                scores = dict([("Total Score", 100)])
            
            # Add document to collection
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            result = {  "label":                har.label,
                        "url":                  har.url,
                        "timestamp":            timestamp,
                        "full_load_time":       har.full_load_time,
                        "onload_event":         har.onload_event,
                        "start_render_time":    har.start_render_time,
                        "time_to_first_byte":   har.time_to_first_byte,
                        "total_dns_time":       har.total_dns_time,
                        "total_transfer_time":  har.total_transfer_time,
                        "total_server_time":    har.total_server_time,
                        "avg_connecting_time":  har.avg_connecting_time,
                        "avg_blocking_time":    har.avg_blocking_time,
                        "total_size":           har.total_size,
                        "text_size":            har.text_size,
                        "media_size":           har.media_size,
                        "cache_size":           har.cache_size,
                        "requests":             har.requests,
                        "redirects":            har.redirects,
                        "bad_requests":         har.bad_requests,
                        "domains":              len(har.domains),
                        "ps_scores":            scores,
                        "har":                  har.origin,
                        "weights_ratio":        har.weight_ratio(),
                        "requests_ratio":       har.req_ratio(),
                        "domains_ratio":        har.domains}

            # MongoDB handler
            mdb_handler = MongoDB()
            if hasattr(c, "message"):
                return False, c.message
            else:
                mdb_handler.collection.insert(result)

            return True, har.label
        else:
            return False, har.parsing_status

    def _get_pagespeed_scores(self, har):
        #Store HAR for Page Speed binary
        hashname = hashlib.md5().hexdigest()
        temp_store = config["app_conf"]["temp_store"]
        filename = os.path.join(temp_store, hashname)

        with open(filename, "w") as file:
            file.write(json.dumps(har))

        # STDOUT,STDERR
        os_type = platform.system()

        if os_type == "Linux":
            std_out = " > /dev/null 2>&1"
        elif os_type == "Windows":
            std_out = " > NUL 2>&1"
        else:
            std_out = ""

        # Run pagespeed_bin
        bin_store = config["app_conf"]["bin_store"]
        pagespeed_bin = os.path.join(bin_store, "pagespeed_bin")

        outfile = filename + ".out"

        os.system(pagespeed_bin + \
            " -input_file " + filename + \
            " -output_format formatted_json" + \
            " -output_file " + outfile + \
            std_out)

        # Output report (JSON)
        with open(outfile, "r") as file:
            output = json.loads(file.read())

        # Final scores
        scores = dict()
        scores["Total Score"] = int(output["score"])
        for rule in output["rule_results"]:
            scores[rule["localized_rule_name"]] = int(rule["rule_score"])

        return scores

    @restrict("GET")
    def download(self):
        """Return serialized HAR file"""

        # Parameters from GET request
        id = request.GET["id"]

        # Read HAR file from disk
        filename = os.path.join(config["app_conf"]["temp_store"], id)
        with open(filename, "r") as file:
            data = file.read()

        # JSON to JSON-P
        data = "onInputData(" + data + ");"

        # Add content type header
        response.content_type = mimetypes.guess_type(filename)[0] or "text/plain"

        return data