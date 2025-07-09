from higgs_app import HiggsApp


def init_app(app: HiggsApp):
    import warnings

    warnings.simplefilter("ignore", ResourceWarning)
