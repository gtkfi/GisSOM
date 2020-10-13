import sys

__file__
__version__ = "1.0.1"

_js_dist_dependencies = [
    {
        "external_url": {
            "prod": [
                "https://unpkg.com/react@16.8.6/umd/react.production.min.js",
                "https://unpkg.com/react-dom@16.8.6/umd/react-dom.production.min.js",
                "https://unpkg.com/prop-types@15.7.2/prop-types.min.js",
            ],
            "dev": [
                "https://unpkg.com/react@16.8.6/umd/react.development.js",
                "https://unpkg.com/react-dom@16.8.6/umd/react-dom.development.js",
                "https://unpkg.com/prop-types@15.7.2/prop-types.js",
            ],
        },
        "relative_package_path": {
            "prod": [
                "react@16.8.6.min.js",
                "react-dom@16.8.6.min.js",
                "prop-types@15.7.2.min.js",
            ],
            "dev": [
                "react@16.8.6.js",
                "react-dom@16.8.6.js",
                "prop-types@15.7.2.js",
            ],
        },
        "namespace": "dash_renderer",
    }
]


_js_dist = [
    {
        "relative_package_path": "{}.min.js".format(__name__),
        "dev_package_path": "{}.dev.js".format(__name__),
        "external_url": "https://unpkg.com/dash-renderer@1.0.1"
        "/dash_renderer/dash_renderer.min.js",
        "namespace": "dash_renderer",
    },
    {
        "relative_package_path": "{}.min.js.map".format(__name__),
        "dev_package_path": "{}.dev.js.map".format(__name__),
        "external_url": "https://unpkg.com/dash-renderer@1.0.1"
        "/dash_renderer/dash_renderer.min.js.map",
        "namespace": "dash_renderer",
        "dynamic": True,
    },
]
