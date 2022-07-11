from typing import Optional


class Ownership:

    def __init__(self, id: int, value: int, rent_value: int):
        self.id = id
        self.value = value
        self.rent_value = rent_value
        self.owner: Optional[int] = None

