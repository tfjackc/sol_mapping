import ee
import geemap
import solara

class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)