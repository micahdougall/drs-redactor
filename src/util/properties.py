from attrs import define, fields_dict
from jproperties import Properties


@define
class AppProperties:
    """Class to store properties as a config map"""
    
    project: str
    payload_schema: str
    inspect_config: str
    deidentify_config: str
    tags_file: str

    def __init__(self, properties_file):
        config = Properties()
        with open(properties_file, "rb") as props:
            config.load(props)

        for f in fields_dict(self.__class__).keys():
            setattr(self, f, config._properties.get(f.upper()))
