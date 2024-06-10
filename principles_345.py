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

class Vehicle(Entity):
    def __init__(self, entity_id, name, model):
        super().__init__(entity_id, name)
        self.model = model

    def to_csv_row(self):
        return super().to_csv_row() + [self.model]

    def to_xml_element(self):
        entity_element = super().to_xml_element()
        model_element = ET.SubElement(entity_element, "Model")
        model_element.text = self.model
        return entity_element

class Pedestrian(Entity):
    def __init__(self, entity_id, name, age):
        super().__init__(entity_id, name)
        self.age = age

    def to_csv_row(self):
        return super().to_csv_row() + [self.age]

    def to_xml_element(self):
        entity_element = super().to_xml_element()
        age_element = ET.SubElement(entity_element, "Age")
        age_element.text = str(self.age)
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
            writer.writerow(["Entity ID", "Name", "Model/Age"])
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

# Example usage demonstrating LSP
entities = [
    Vehicle(1, 'Car A', 'Model X'),
    Pedestrian(2, 'John Doe', 30)
]

csv_handler = CSVHandler('entities.csv')
xml_handler = XMLHandler('entities.xml')

csv_saver = EntitySaver(csv_handler)
xml_saver = EntitySaver(xml_handler)

for entity in entities:
    csv_saver.save(entity)
    xml_saver.save(entity)
