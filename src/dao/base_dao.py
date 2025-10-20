from abc import ABC, abstractmethod

class IBaseDAO(ABC):
    @abstractmethod
    def existe(self, id):
        pass
    
    @abstractmethod
    def alta(self, entidad):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_id(self, id):
        pass

    @abstractmethod
    def modificar(self, id, *args, **kwargs): 
        pass

    @abstractmethod
    def borrar(self, id):
        pass