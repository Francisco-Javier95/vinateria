class Privilegio:

    # constructor
    def __init__(self, privilegio_id, privilegio_privilegio):
        self.privilegio_id = privilegio_id
        self.privilegio_privilegio = privilegio_privilegio

    def mostrar_info (self):
        return f"Privilegio: {self.privilegio_privilegio}"

class Privilegio_nombre:
    # Constructor
    def __init__(self, privilegio_privilegio):
        self.privilegio_privilegio = privilegio_privilegio