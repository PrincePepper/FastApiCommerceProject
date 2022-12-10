import json


class SOURCE:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.address = ""
        self.properties = json

    def get_about_me(self):
        return {"id": self.id,
                "name": self.name,
                "address": self.address,
                "properties": self.properties}

    def get_properties(self):
        return self.properties
