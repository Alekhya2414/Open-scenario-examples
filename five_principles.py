import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from abc import ABC, abstractmethod

# Interface Segregation Principle (ISP)
class CSVExportable(ABC):
    @abstractmethod
    def to_csv_row(self):
        pass

class XMLExportable(ABC):
    @abstractmethod
    def to_xml_element(self):
        pass

# Entity classes implementing interfaces
class Entity(CSVExportable, XMLExportable):
    def __init__(self, entity_id, name):
        self.entity_id = entity_id
        self.name = name

    def to_csv_row(self):
        return [self.entity_id, self.name]

    def to_xml_element(self):
        entity_element = ET.Element("Entity", id=str(self.entity_id))
        name_element = ET.SubElement(entity_element, "Name")
        name_element.text = self.name
        return entity_element

class LightStateAction(Entity):
    def __init__(self, entity_id, name, user_defined_light_type):
        super().__init__(entity_id, name)
        self.user_defined_light_type = user_defined_light_type

    def to_csv_row(self):
        return super().to_csv_row() + [self.user_defined_light_type]

    def to_xml_element(self):
        entity_element = super().to_xml_element()
        light_state_action_element = ET.SubElement(entity_element, "LightStateAction")
        light_type_element = ET.SubElement(light_state_action_element, "LightType")
        user_defined_light_element = ET.SubElement(light_type_element, "UserDefinedLight")
        user_defined_light_element.set("userDefinedLightType", self.user_defined_light_type)
        return entity_element

# Dependency Inversion Principle (DIP)
class PersistenceHandler(ABC):
    @abstractmethod
    def save(self, entity: Entity):
        pass

class CSVHandler(PersistenceHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, entity: Entity):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Entity ID", "Name", "UserDefinedLightType"])
            writer.writerow(entity.to_csv_row())

class XMLHandler(PersistenceHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, entity: Entity):
        root = ET.Element("Entities")
        root.append(entity.to_xml_element())
        tree = ET.ElementTree(root)
        tree.write(self.file_path)

# High-level module depending on abstraction
class EntitySaver:
    def __init__(self, handler: PersistenceHandler):
        self.handler = handler

    def save(self, entity: Entity):
        self.handler.save(entity)

# Example XML parsing function to demonstrate reading the XML file
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    parsed_entities = []
    for action in root.findall('.//PrivateAction'):
        entity_id = 1  # Adjust as needed
        name = "LightStateAction"
        light_type = action.find('.//UserDefinedLight').get('userDefinedLightType')
        parsed_entities.append(LightStateAction(entity_id, name, light_type))
    return parsed_entities

# Example usage demonstrating LSP
entities = [
    LightStateAction(1, 'Light State Action', 'myLights')
]

# Save to CSV and XML using different handlers
csv_handler = CSVHandler('entity.csv')
xml_handler = XMLHandler('entity.xml')

csv_saver = EntitySaver(csv_handler)
xml_saver = EntitySaver(xml_handler)

for entity in entities:
    csv_saver.save(entity)
    xml_saver.save(entity)

# Parsing the provided XML file
parsed_entities = parse_xml('scenario.xml')
for entity in parsed_entities:
    print(f'Parsed Entity: {entity.name} with UserDefinedLightType: {entity.user_defined_light_type}')
