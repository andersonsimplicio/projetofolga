class FuncionarioEscala:
    def __init__(self, nome, turno):
        self.nome = nome
        self.turno = turno
        self.escala = []

    def add_escala(self, dia):
        self.escala.append(dia)

    def add_folga(self, dia):
        self.escala[dia] = "E"

    def add_extra(self, dia):
        self.escala[dia] = "E"
