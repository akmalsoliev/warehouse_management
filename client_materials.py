class Client():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class Material():
    def __init__(self, item_code = None, item_name= None, batch_number = None, color=None, color_name=None):
        self.item_code = item_code
        self.item_name = item_name
        self.batch_number = batch_number
        self.color = color
        self.color_name = color_name