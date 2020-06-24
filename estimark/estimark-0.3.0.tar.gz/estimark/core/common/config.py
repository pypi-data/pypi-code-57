from typing import Dict, Any


Config = Dict[str, Any]


BASE: Config = {
    "mode": "BASE",
    "root_dir": "",
    "param_dir": "",
    "result_dir": "",
    "plot_dir": "",
    "strategies": ["base"],
    "strategy": {}
}


DEVELOPMENT_CONFIG: Config = {**BASE, **{
    "mode": "DEV",
    "factory": "CheckFactory",
    "strategies": ["base", "check"]
}}


PRODUCTION_CONFIG: Config = {**BASE, **{
    "mode": "PROD",
    "factory": "RstFactory",
    "strategies": ["base", "json", "rst"]
}}
