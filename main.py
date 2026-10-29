from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID

from models import Vehiculo, VehiculoCreate, VehiculoUpdate
from database import db_vehiculos, cargar_datos_semilla

app = FastAPI(
    title="API Gestión de Vehículos y Fallas - SENA ADSO",
    description="API RESTful para la gestión de vehículos y reparaciones en memoria utilizando Pydantic y FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    cargar_datos_semilla()

@app.get(
    "/",
    tags=["Raíz"],
    summary="Mensaje de Bienvenida"
)
def welcome():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Vehículos (SENA ADSO)",
        "documentacion": "/docs"
    }

@app.get(
    "/vehiculos",
    response_model=List[Vehiculo],
    status_code=status.HTTP_200_OK,
    tags=["Vehículos"],
    summary="Obtener todos los vehículos"
)
def get_vehiculos():
    return db_vehiculos

@app.get(
    "/vehiculos/{vehiculo_id}",
    response_model=Vehiculo,
    status_code=status.HTTP_200_OK,
    tags=["Vehículos"],
    summary="Buscar vehículo por ID"
)
def get_vehiculo_por_id(vehiculo_id: UUID):
    for vehi in db_vehiculos:
        if vehi.id == vehiculo_id:
            return vehi

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El vehículo con ID '{vehiculo_id}' no fue encontrado en el catálogo."
    )

@app.post(
    "/vehiculos",
    response_model=Vehiculo,
    status_code=status.HTTP_201_CREATED,
    tags=["Vehículos"],
    summary="Registrar nuevo vehículo"
)
def create_vehiculo(vehiculo_in: VehiculoCreate):
    for vehi in db_vehiculos:
        if vehi.placa_vehiculo.upper() == vehiculo_in.placa_vehiculo.upper():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un vehículo registrado con la placa '{vehiculo_in.placa_vehiculo}'."
            )

    nuevo_vehiculo = Vehiculo(**vehiculo_in.model_dump())
    db_vehiculos.append(nuevo_vehiculo)
    return nuevo_vehiculo

@app.put(
    "/vehiculos/{vehiculo_id}",
    response_model=Vehiculo,
    status_code=status.HTTP_200_OK,
    tags=["Vehículos"],
    summary="Actualizar vehículo por ID"
)
def update_vehiculo(vehiculo_id: UUID, vehiculo_update: VehiculoUpdate):
    for index, vehi in enumerate(db_vehiculos):
        if vehi.id == vehiculo_id:
            datos_actualizados = vehiculo_update.model_dump(exclude_unset=True)
            vehiculo_modificado = vehi.model_copy(update=datos_actualizados)
            db_vehiculos[index] = vehiculo_modificado
            return vehiculo_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El vehículo con ID '{vehiculo_id}' no existe."
    )

@app.delete(
    "/vehiculos/{vehiculo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Vehículos"],
    summary="Eliminar vehículo por ID"
)
def delete_vehiculo(vehiculo_id: UUID):
    for index, vehi in enumerate(db_vehiculos):
        if vehi.id == vehiculo_id:
            vehiculo_eliminado = db_vehiculos.pop(index)
            return {
                "mensaje": "Vehículo eliminado exitosamente",
                "vehiculo_eliminado": vehiculo_eliminado
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El vehículo con ID '{vehiculo_id}' no existe."
    )