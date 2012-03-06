from pylons import tmpl_context as c
from pylons import config
from pylons.controllers.util import redirect

from harstorage.lib.base import BaseController, render
from harstorage.lib.MongoHandler import MongoDB
from harstorage.lib.HAR import HAR

class MigrationController(BaseController):

    def __before__(self):
        """Define version of static content"""

        c.rev = config["app_conf"]["static_version"]

    def status(self):
        return render("/migration.html")

    def migration(self):
        # MongoDB handler
        mdb_handler = MongoDB()
        if hasattr(c, "message"): return render("/error.html")

        for document in mdb_handler.collection.find(fields=["_id", "har"]):
            id = document["_id"]

            har = HAR(document["har"], True)

            har.analyze()

            domains_req_ratio = dict()
            domains_weight_ratio = dict()

            for key, value in har.domains.items():
                domains_req_ratio[key] = value[0]
                domains_weight_ratio[key] = value[1]

            data = {"full_load_time":       har.full_load_time,
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
                    "weights_ratio":        har.weight_ratio(),
                    "requests_ratio":       har.req_ratio(),
                    "domains_ratio":        har.domains}

            mdb_handler.collection.update({"_id": id}, {"$set": data})

        migration_handler = MongoDB(collection = "migration")
        migration_handler.collection.insert({"status": "ok"})

        redirect("/")