class Product:
    def __init__(self, id, name, price, id_category):
        self.id = id
        self.name = name
        self.price = price
        self.id_category = id_category

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'id_category': self.id_category
        }