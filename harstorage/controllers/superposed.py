from pylons import request, tmpl_context as c
from pylons import config
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController, render
from harstorage.lib.MongoHandler import MongoDB
from harstorage.lib.math_helpers import Histogram, Aggregator


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
        if hasattr(c, "message"):
            return render("/error.html")

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
            fields=["timestamp"],
            sort=[("timestamp", 1)])

        dates = str()
        for document in documents:
            dates += document["timestamp"] + ";"

        return dates[:-1]

    @restrict("GET")
    def display(self):
        """Render page with column chart and data table"""

        # MongoDB handler
        md_handler = MongoDB()
        if hasattr(c, "message"):
            return render("/error.html")

        # Checkbox options
        c.chart_type = request.GET.get("chart", None)
        c.table = request.GET.get("table", "false")
        init = request.GET.get("metric", "true")
        forOverview = request.GET.get("overview", "false")

        c.chart = "true" if c.chart_type else "false"

        # Aggregation option
        c.agg_type = request.GET.get("metric", "Average")

        # Aggregation option
        c.timeFormat = request.GET.get("timeFormat", "ms")

        # Number of records
        rows = [x for x in request.GET if "_label_hidden" in x]
        c.rowcount = len(rows)

        if c.timeFormat == "s":
            fltLabel = "Full Load Time (s)"
            usrLabel = "User Ready Time (s)"
            adsLabel = "Ads Time (s)"
        else:
            fltLabel = "Full Load Time (ms)"
            usrLabel = "User Ready Time (ms)"
            adsLabel = "Ads Time (ms)"

        # Data table
        c.headers = ["Label", fltLabel, usrLabel, "Total Requests",
                     "Total Size (kB)", "Page Speed Score",
                     "onLoad Event (ms)", "Start Render Time (ms)",
                     "Time to First Byte (ms)", "Total DNS Time (ms)",
                     "Total Transfer Time (ms)", "Total Server Time (ms)",
                     "Avg. Connecting Time (ms)", "Avg. Blocking Time (ms)",
                     "Text Size (kB)", "Media Size (kB)", "Cache Size (kB)",
                     "Redirects", "Bad Rquests", "Domains", adsLabel]
        c.metrics_table = list()
        c.metrics_table.append(list())

        # Chart points
        c.points = str()

        # Aggregator
        aggregator = Aggregator()

        # Test results from database
        for row_index in range(c.rowcount):
            # Parameters from GET request
            label  = request.GET[ 'step_' + str(row_index+1) + '_label_hidden' ]
            start_ts = request.GET["step_" + str(row_index + 1) + "_start_ts"]
            end_ts = request.GET["step_" + str(row_index + 1) + "_end_ts"]

            # Fetch test results
            labels = label.split(",")
            condition = {
                "label": { '$in': labels},
                "timestamp": {"$gte": start_ts, "$lte": end_ts}
            }
            fields = list()
            for metric in self.METRICS:
                fields.append(metric)
            fields.append("pagename")

            documents = md_handler.collection.find(condition,
                                                   fields=fields)

            # Add data row to aggregator
            if forOverview == "true":
                try:
                    pagename = documents[0]["pagename"]
                except:
                    pagename = label[:40]

                aggregator.add_row(pagename, row_index, documents)
                c.metrics_table[0].append(pagename)
                c.points += pagename + "#"
            else:
                # Add label
                c.metrics_table[0].append(label[:40])
                c.points += label[:40] + "#"
                aggregator.add_row(label[:40], row_index, documents)                

        # Aggregated data per column
        column = 1
        for metric in aggregator.METRICS:
            c.metrics_table.append(list())
            c.points = c.points[:-1] + ";"

            for row_index in range(c.rowcount):
                data_list = aggregator.data[metric][row_index]
                if len(data_list) <= 0:
                    value = 0
                else:
                    value = aggregator.get_aggregated_value(data_list, c.agg_type,
                                                        metric)

                c.points += str(value) + "#"

                tableValue = value
                if metric == "full_load_time" or metric == "user_ready_time" or metric == "ads_full_time":
                    if c.timeFormat == "s":
                        tableValue = round(tableValue / 1000, 2)

                c.metrics_table[column].append(tableValue)

            column += 1

        # Names of series
        titles = str()
        for title in aggregator.TITLES:
            titles += title + "#"

        # Final chart points
        c.points = titles[:-1] + ";" + c.points[:-1]
        c.points = aggregator.exclude_missing(c.points)

        if forOverview == "true":
            return render("/dashboard/overview/core.html")
        else:
            return render("/display/core.html")

    def histogram(self):
        """Render chart with histograms"""

        # MongoDB handler
        md_handler = MongoDB()
        if hasattr(c, "message"):
            return render("/error.html")

        # Options
        c.label = request.GET["label"]
        c.metric = request.GET["metric"]

        # Metrics
        METRICS = [("full_load_time", "Full Load Time"),
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
        documents = md_handler.collection.find(condition, fields=fields)

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
