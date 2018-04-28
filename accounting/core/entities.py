class Material:
    id: int
    title: str
    description: str
    cost: float
    petrol_station: int

    def __init__(self, params):
        """
        - Title:
        - Description:
        - cost:
        :param params: parameters as dictionary
        """
        self.id = None
        self.title = params['title']
        self.description = params['description']
        self.cost = params['cost']


class PetrolStation:
    id: int
    title: str
    location: str
