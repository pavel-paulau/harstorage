from pylons import request, tmpl_context as c
from pylons import config
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController, render
from harstorage.lib.MongoHandler import MongoDB
from harstorage.lib.Math import Histogram, Aggregator

class SuperposedController(BaseController):

    """
    Interface for aggregation and comparison of test results

    """

    def __before__(self):
        """Define version of static content"""

        c.rev = config["app_conf"]["static_version"]

    @restrict("GET")
    def create(self):
        """Render form with list of labels and timestamps"""

        # MongoDB handler
        md_handler = MongoDB()
        
        # List of labels
        c.labels = list()
        
        for label in md_handler.collection.distinct("label"):
            c.labels.append(label)
        
        return render("/create/core.html")
    
    @restrict("GET")
    def dates(self):
        """Return a list of timestamps for selected label"""

        # MongoDB handler
        md_handler = MongoDB()

        # Read label from GET request
        label = request.GET["label"]

        # Read data from database
        documents = md_handler.collection.find(
            {"label": label},
            fields = ["timestamp"],
            sort = [("timestamp", 1)])
        
        for document in documents:
            try:
                dates = dates + document["timestamp"] + ";"
            except:
                dates = document["timestamp"] + ";"

        return dates[:-1]

    @restrict("GET")
    def display(self):
        """Render page with column chart and data table"""

        # MongoDB handler
        md_handler = MongoDB()

        # Checkbox options
        c.chart_type = request.GET.get("chart", None)
        c.table = request.GET.get("table", "false")
        init = request.GET.get("metric", "true")

        c.chart = "true" if c.chart_type else "false"

        # Metric option
        c.metric = request.GET.get("metric", "Average")

        # Number of records
        if c.chart == "true" and c.table == "true" and init != "true":
            c.rowcount = len(request.GET) / 3 - 1
        else:
            c.rowcount = len(request.GET) / 3

        # Data containers        
        METRICS = ( "full_load_time", "requests", "total_size",
                    "ps_scores", "onload_event", "start_render_time",
                    "time_to_first_byte", "total_dns_time",
                    "total_transfer_time", "total_server_time",
                    "avg_connecting_time", "avg_blocking_time", "text_size",
                    "media_size", "cache_size", "redirects", "bad_requests",
                    "domains")

        c.headers = [   "Label", "Full Load Time (ms)", "Total Requests",
                        "Total Size (kB)", "Page Speed Score",
                        "onLoad Event (ms)", "Start Render Time (ms)",
                        "Time to First Byte (ms)", "Total DNS Time (ms)",
                        "Total Transfer Time (ms)", "Total Server Time (ms)",
                        "Avg. Connecting Time (ms)", "Avg. Blocking Time (ms)",
                        "Text Size (kB)", "Media Size (kB)", "Cache Size (kB)",
                        "Redirects", "Bad Rquests", "Domains"]

        TITLES = [ "Full Load Time", "Total Requests",
                   "Total Size", "Page Speed Score", "onLoad Event",
                   "Start Render Time", "Time to First Byte",
                   "Total DNS Time", "Total Transfer Time", "Total Server Time",
                   "Avg. Connecting Time", "Avg. Blocking Time", "Text Size",
                   "Media Size", "Cache Size", "Redirects", "Bad Rquests",
                   "Domains"]

        # Set of metrics to exclude (due to missing data)
        exclude = set()

        data = dict()
        
        for metric in METRICS:
            data[metric] = list()

        data["label"] = list()

        # Data table
        c.metrics_table = list()
        c.metrics_table.append(list())

        # Test results from database
        for row in range(c.rowcount):
            # Parameters from GET request
            label = request.GET["step_" + str(row+1) + "_label"]
            start_ts = request.GET["step_" + str(row+1) + "_start_ts"]
            end_ts = request.GET["step_" + str(row+1) + "_end_ts"]

            # Label
            c.metrics_table[0].append(label)

            data["label"].append(row)
            data["label"][row] = label

            # Fetch test results
            condition = {"label": label,
                         "timestamp": {"$gte": start_ts, "$lte": end_ts}}

            documents = md_handler.collection.find(condition, fields = METRICS)

            for metric in METRICS:
                data[metric].append(row)
                data[metric][row] = list()

            for document in documents:
                for metric in METRICS:
                    if metric != "ps_scores":
                        data[metric][row].append(document[metric])
                    else:
                        data[metric][row].append(document[metric]["Total Score"])

        # Aggregation
        c.points = str()

        for row in range(c.rowcount):
            c.points += data["label"][row] + "#"

        column = 1
        agg_handler = Aggregator()

        for metric in METRICS:
            c.metrics_table.append(list())

            c.points = c.points[:-1] + ";"
            for row in range(c.rowcount):
                if c.metric == "Average":
                    value = agg_handler.average(data[metric][row])
                elif c.metric == "Minimum":
                    value = agg_handler.minimum(data[metric][row])
                elif c.metric == "Maximum":
                    value = agg_handler.maximum(data[metric][row])
                elif c.metric == "90th Percentile":
                    value = agg_handler.percentile(data[metric][row], 0.9)
                elif c.metric == "Median":
                    value = agg_handler.percentile(data[metric][row], 0.5)

                if value == "n/a":
                    exclude.add(metric)
                else:
                    c.points += str(value) + "#"
                c.metrics_table[column].append(value)

            column += 1

        # Update list of titles
        if "onload_event" in exclude:
            TITLES.pop(TITLES.index("onLoad Event"))
        if "start_render_time" in exclude:
            TITLES.pop(TITLES.index("Start Render Time"))

        header = str()
        for title in TITLES:
            header += title + "#"

        c.points = header[:-1] + ";" + c.points[:-1]

        return render("/display/core.html")

    def histogram(self):
        """Render chart with histograms"""
        
        # MongoDB handler
        md_handler = MongoDB()

        # Option
        c.label = request.GET["label"]
        c.metric = request.GET["metric"]

        # Metrics
        METRICS = [ ("full_load_time", "Full Load Time"),
                    ("onload_event", "onLoad Event"),
                    ("start_render_time", "Start Render Time"),
                    ("time_to_first_byte", "Time to First Byte"),
                    ("total_dns_time", "Total DNS Time"),
                    ("total_transfer_time", "Total Transfer Time"),
                    ("total_server_time", "Total Server Time"),
                    ("avg_connecting_time", "Avg. Connecting Time"),
                    ("avg_blocking_time", "Avg. Blocking Time")]

        time_metrics = ["full_load_time", "onload_event", "start_render_time",
                        "time_to_first_byte"]

        c.metrics = list()

        # Read data from database
        condition = {"label": c.label}
        fields = (metric for metric, title in METRICS)

        documents = md_handler.collection.find(condition, fields = fields)

        full_data = list(document for document in documents)

        for metric, title in METRICS:
            try:
                data = (result[metric] for result in full_data)
                my_histogram = Histogram(data)

                if metric in time_metrics:
                    ranges = my_histogram.ranges(True)
                else:
                    ranges = my_histogram.ranges()

                frequencies = my_histogram.frequencies()

                if metric == c.metric:
                    c.data = ""

                    for occ_range in ranges:
                        c.data += occ_range + "#"

                    c.data = c.data[:-1] + ";"

                    for frequency in frequencies:
                        c.data += str(frequency) + "#"

                    c.data = c.data[:-1] + ";"

                    c.title = title

                c.metrics.append((metric, title))
            except IndexError:
                pass
            except TypeError:
                pass
            except ValueError:
                pass

        if len(c.metrics):
            return render("/histogram/core.html")
        else:
            c.message = "Sorry! You haven't enough data."
            return render("/error.html")