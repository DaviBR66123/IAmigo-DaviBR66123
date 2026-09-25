class Validações:

    def _validar_id(self, valor):
        if valor is None:
            raise ValueError("O id não pode ser vazio.")

        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O id só pode conter números.")

        if valor <= 0:
            raise ValueError("O id deve ser maior que zero.")

        return valor