import xml.etree.ElementTree as ET

class Style:

    def __init__(self, name):
        Style.counter += 1
        self._id = Style.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("Style")
        el.set("id", str(self._id))
        el.set("name", self._name)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"

Style.counter = 0