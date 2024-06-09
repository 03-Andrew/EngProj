class Material:
    def __init__(self, id, category, name, price, measurement):
        self.id = id
        self.category = category
        self.name = name
        self.price = price
        self.measurement = measurement


class MaterialList:
    def __init__(self):
        self.materials = {}

    def add_material(self, material):
        self.materials[material.id] = material

    def read_materials(self):
        with open("items2.txt", 'r') as file:
            lines = file.readlines()
            category = None
            for line in lines:
                if not line.startswith("~"):
                    category = line.strip().rstrip(':')
                else:
                    item_id, name, price, measurement = line.strip().replace("~", "").split(',')
                    self.add_material(Material(item_id, category, name, int(price), measurement))

    def get_all_materials(self):
        return self.materials
