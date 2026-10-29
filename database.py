from typing import List
from models import Vehiculo
from uuid import uuid4

db_vehiculos: List[Vehiculo] = []

def cargar_datos_semilla():
    if not db_vehiculos:
        db_vehiculos.extend([
            Vehiculo(
                id = uuid4(),
                placa_vehiculo = "KOJ-789",
                descripcion_falla = "Eje de tranmision roto",
                costo_estimado = 2500000.00,
                reparado = False
            ),
            Vehiculo(
                id = uuid4(),
                placa_vehiculo = "LAP-693",
                descripcion_falla = "Cambiar filtro de aceite",
                costo_estimado = 40000.00,
                reparado = False
            ),
            Vehiculo(
                id = uuid4(),
                placa_vehiculo = "BOT-896",
                descripcion_falla = "Pastillas de freno desgastadas",
                costo_estimado = 150000.00,
                reparado = False
            )
        ])