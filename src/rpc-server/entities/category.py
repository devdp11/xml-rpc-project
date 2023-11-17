import xml.etree.ElementTree as ET

class MarketCategoryItem:
    counter = 0  # Mover o contador para fora do construtor

    def __init__(self, name):
        MarketCategoryItem.counter += 1
        self._id = MarketCategoryItem.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("market_category")
        el.set("id", str(self._id))
        el.set("Name", self._name)
        return el

    def __str__(self):
        return f"Market Category {self._id}: {self._name}"