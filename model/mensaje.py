from typing import Dict

class Mensaje():
    def __init__(self, message_spec):
        self.texto = message_spec.get("texto")

    def to_dict(self):
        return {
            "texto": self.texto
        }

    def format(self,cambios:Dict={}):
        nombres_a_cambiar = cambios.keys()
        nuevo_texto = self.texto

        for n in nombres_a_cambiar:
            nuevo_texto = nuevo_texto.replace("@@{n}",nombres_a_cambiar[n])

        return nuevo_texto

