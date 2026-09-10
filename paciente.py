class Paciente:
    def __init__(self, rut:str, nombre:str, edad:int, prevision:str):
        self.rut = rut
        self.nombre = nombre
        self.edad = edad
        self.prevision = prevision

    @property
    def rut(self)->str:
        return self._rut

    @rut.setter
    def rut(self, rut:str)->None:
        self._rut = rut