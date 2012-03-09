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
        if hasattr(c, "message"): return render("/error.html")
        
        # List of labels
        c.labels = list()
        
        for label in md_handler.collection.distinct("label"):
            c.labels.append(label)
        
        return render("/create/core.html")
    
    @restrict("GET")
    def dates(self):
        """Return a list of timestamps for selected label"""

        # Read label from GET request
        label = request.GET["label"]

        # Read data from database
        documents = MongoDB().collection.find(
            {"label": label},
            fields = ["timestamp"],
            sort = [("timestamp", 1)])

        dates = str()
        for document in documents:
            dates += document["timestamp"] + ";"

        return dates[:-1]

    @restrict("GET")
    def display(self):
        """Render page with column chart and data table"""

        # MongoDB handler
        md_handler = MongoDB()
        if hasattr(c, "message"): return render("/error.html")

        # Checkbox options
        c.chart_type = request.GET.get("chart", None)
        c.table = request.GET.get("table", "false")
        init = request.GET.get("metric", "true")

        c.chart = "true" if c.chart_type else "false"

        # Aggregation option
        c.agg_type = request.GET.get("metric", "Average")

        # Number of records
        if c.chart == "true" and c.table == "true" and init != "true":
            c.rowcount = len(request.GET) / 3 - 1
        else:
            c.rowcount = len(request.GET) / 3

        # Data table
        c.headers = [   "Label", "Full Load Time (ms)", "Total Requests",
                        "Total Size (kB)", "Page Speed Score",
                        "onLoad Event (ms)", "Start Render Time (ms)",
                        "Time to First Byte (ms)", "Total DNS Time (ms)",
                        "Total Transfer Time (ms)", "Total Server Time (ms)",
                        "Avg. Connecting Time (ms)", "Avg. Blocking Time (ms)",
                        "Text Size (kB)", "Media Size (kB)", "Cache Size (kB)",
                        "Redirects", "Bad Rquests", "Domains"]
        c.metrics_table = list()
        c.metrics_table.append(list())

        # Chart points
        c.points = str()

        # Aggregator
        aggregator = Aggregator()        

        # Test results from database
        for row_index in range(c.rowcount):
            # Parameters from GET request
            label    = request.GET["step_" + str(row_index + 1) + "_label"]
            start_ts = request.GET["step_" + str(row_index + 1) + "_start_ts"]
            end_ts   = request.GET["step_" + str(row_index + 1) + "_end_ts"]

            # Add label
            c.metrics_table[0].append(label)
            c.points += label + "#"

            # Fetch test results
            condition = {"label": label, "timestamp": {"$gte": start_ts, "$lte": end_ts}}
            documents = md_handler.collection.find(condition, fields = aggregator.METRICS)

            # Add data row to aggregator
            aggregator.add_row(label, row_index, documents)            

        # Aggregated data per column
        column = 1
        for metric in aggregator.METRICS:
            c.metrics_table.append(list())
            c.points = c.points[:-1] + ";"

            for row_index in range(c.rowcount):
                data_list = aggregator.data[metric][row_index]
                value = aggregator.get_aggregated_value(data_list, c.agg_type, metric)

                c.points += str(value) + "#"
                c.metrics_table[column].append(value)

            column += 1

        # Names of series
        titles = str()
        for title in aggregator.TITLES:
            titles += title + "#"

        # Final chart points
        c.points = titles[:-1] + ";" + c.points[:-1]
        c.points = aggregator.exclude_missing(c.points)

        return render("/display/core.html")

    def histogram(self):
        """Render chart with histograms"""
        
        # MongoDB handler
        md_handler = MongoDB()
        if hasattr(c, "message"): return render("/error.html")

        # Options
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
                histogram = Histogram(data)

                if metric in time_metrics:
                    ranges = histogram.ranges(True)
                else:
                    ranges = histogram.ranges()

                frequencies = histogram.frequencies()

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