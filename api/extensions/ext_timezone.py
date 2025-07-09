import os
import time

from higgs_app import HiggsApp


def init_app(app: HiggsApp):
    os.environ["TZ"] = "UTC"
    # windows platform not support tzset
    if hasattr(time, "tzset"):
        time.tzset()
