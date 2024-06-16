class Material:
    def __init__(self, id, category, name, price, measurement, stock):
        self.id = id
        self.category = category
        self.name = name
        self.price = price
        self.measurement = measurement
        self.stock = stock

    def sell_items(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        else:
            print(f"Not enough stock available for {self.name}")
            return False


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
                    item_id, name, price, measurement, stock = line.strip().replace("~", "").split(',')
                    self.add_material(Material(item_id, category, name, int(price), measurement, int(stock)))

    def get_all_materials(self):
        return self.materials

    def get_all_categories(self):
        categories = []
        for material in self.materials.values():
            if material.category not in categories:
                categories.append(material.category)
        return categories

    def sell_items(self, item_id, quantity):
        if item_id in self.materials:
            material = self.materials[item_id]
            if material.sell_items(quantity):
                self.update_stock_in_file(item_id, material.stock)
        else:
            print("Material not found.")



    def update_stock_in_file(self, item_id, new_stock):
        with open("items2.txt", 'r') as file:
            lines = file.readlines()
        with open("items2.txt", 'w') as file:
            for line in lines:
                if line.startswith("~" + str(item_id)):
                    parts = line.strip().split(',')
                    parts[-1] = str(new_stock)
                    line = ",".join(parts) + "\n"
                file.write(line)
