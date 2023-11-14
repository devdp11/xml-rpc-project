import xml.etree.ElementTree as ET

class Brand:

    def __init__(self, name: str, country: str):
        Brand.counter += 1
        self._id = Brand.counter
        self._name = name
        self._country = country
        self._models = []

    def add_model(self, model):
        self._models.append(model)

    def to_xml(self):
        el = ET.Element("Brand")
        el.set("id", str(self._id))
        el.set("name", self._name)

        # Assuming self._country is a string representing the country identifier
        country_el = ET.Element("Country")
        country_el.text = self._country
        el.append(country_el)

        models_el = ET.Element("Models")
        for model in self._models:
            models_el.append(model.to_xml())

        el.append(models_el)

        return el

    def __str__(self):
        return f"{self._name} ({self._id})"

Brand.counter = 0