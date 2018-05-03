from datetime import datetime


class Material:
    id: int
    title: str
    description: str
    cost: float

    def __init__(self, params):
        self.id = params['id'] if 'id' in params else None
        self.title = params['title']
        self.description = params['description']
        self.cost = float(params['cost'])


class PetrolStation:
    id: int
    title: str
    location: str

    def __init__(self, params):
        self.id = params['id'] if 'id' in params else None
        self.title = params['title']
        self.location = params['location']


class MaterialsOnPetrolStation:
    materials: dict
    petrol_station: PetrolStation
    date_of_incoming: datetime
    number: int

    def __init__(self, params):
        self.materials = params['materials']
        self.petrol_station = params['petrol_station']
        self.date_of_incoming = params['date_of_incoming']
        self.number = params['number']
