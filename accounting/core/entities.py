from datetime import datetime


class Material:
    title: str
    description: str
    cost: float

    def __init__(self, params):
        """
        - Title:
        - Description:
        - cost:
        :param params: parameters as dictionary
        """
        self.title = params['title']
        self.description = params['description']
        self.cost = params['cost']


class PetrolStation:
    title: str
    location = datetime.now()
    materials: dict
