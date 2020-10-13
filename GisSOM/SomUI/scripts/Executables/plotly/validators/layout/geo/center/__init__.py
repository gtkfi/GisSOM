import _plotly_utils.basevalidators


class LonValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="lon", parent_name="layout.geo.center", **kwargs):
        super(LonValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )


import _plotly_utils.basevalidators


class LatValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="lat", parent_name="layout.geo.center", **kwargs):
        super(LatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )
