import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Single Responsibility Principle: Each class has one responsibility

class Entity:
    def __init__(self, entity_id, name):
        self.entity_id = entity_id
        self.name = name

    def to_csv_row(self):
        return [self.entity_id, self.name]

class Vehicle(Entity):
    def __init__(self, entity_id, name, model):
        super().__init__(entity_id, name)
        self.model = model

    def to_csv_row(self):
        return super().to_csv_row() + [self.model]

class Pedestrian(Entity):
    def __init__(self, entity_id, name, age):
        super().__init__(entity_id, name)
        self.age = age

    def to_csv_row(self):
        return super().to_csv_row() + [self.age]

# Open/Closed Principle: Entities can be extended without modifying existing code

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_entities_to_csv(self, entities):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Entity ID", "Name", "Model/Age"])
            for entity in entities:
                writer.writerow(entity.to_csv_row())

    def read_entities_from_csv(self):
        entities = []
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                entity_id, name, attribute = row
                if attribute.isdigit():  # Assuming age is a digit
                    entities.append(Pedestrian(entity_id, name, int(attribute)))
                else:
                    entities.append(Vehicle(entity_id, name, attribute))
        return entities

class XMLHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_entities_from_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        parsed_entities = []
        for entity in root.findall('.//Entity'):
            entity_id = entity.get('id')
            name = entity.find('Name').text
            model = entity.find('Model')
            if model is not None:
                parsed_entities.append(Vehicle(entity_id, name, model.text))
            else:
                age = entity.find('Age').text
                parsed_entities.append(Pedestrian(entity_id, name, age))
        return parsed_entities

    def create_sample_xml(self, entities):
        root = ET.Element("Entities")
        for entity in entities:
            entity_element = ET.SubElement(root, "Entity", id=str(entity.entity_id))
            name_element = ET.SubElement(entity_element, "Name")
            name_element.text = entity.name
            if isinstance(entity, Vehicle):
                model_element = ET.SubElement(entity_element, "Model")
                model_element.text = entity.model
            elif isinstance(entity, Pedestrian):
                age_element = ET.SubElement(entity_element, "Age")
                age_element.text = str(entity.age)
        tree = ET.ElementTree(root)
        with open(self.file_path, "wb") as file:
            tree.write(file)

        # Pretty print the XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(self.file_path, "w") as file:
            file.write(xml_str)

class EntityComparator:
    @staticmethod
    def compare_entities(csv_entities, xml_entities):
        for csv_entity in csv_entities:
            for xml_entity in xml_entities:
                if csv_entity.entity_id == xml_entity.entity_id and csv_entity.name == xml_entity.name:
                    print(f"Match found: {csv_entity.name} with ID {csv_entity.entity_id}")

# Example usage

# Creating entities
entities = [
    Vehicle(1, 'Car A', 'Model X'),
    Pedestrian(2, 'John Doe', 30),
    Vehicle(3, 'Car B', 'Model Y'),
    Pedestrian(4, 'Jane Doe', 25)
]

# Saving entities to CSV
csv_file_path = 'scenario.csv'  # Specify your CSV file path
csv_handler = CSVHandler(csv_file_path)
csv_handler.save_entities_to_csv(entities)

# Creating a sample XML file with the same entities
xml_file_path = 'sample_scenario.xml'  # Specify your XML file path
xml_handler = XMLHandler(xml_file_path)
xml_handler.create_sample_xml(entities)

# Reading and comparing entities from CSV and XML
csv_entities = csv_handler.read_entities_from_csv()
xml_entities = xml_handler.parse_entities_from_xml()
EntityComparator.compare_entities(csv_entities, xml_entities)
