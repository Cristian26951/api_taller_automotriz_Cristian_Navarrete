from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class VehiculoBase(BaseModel):
    placa_vehiculo: str = Field(
        ...,
        min_length = 3,
        max_length = 100,
        description = "Placa del vehiculo",
        example = "KLS-450"
    )
    descripcion_falla: str = Field(
        ...,
        min_length = 3,
        max_length = 100,
        description = "Descripcion de la falla",
        example = "Faros dañados"
    )
    costo_estimado: float = Field(
        ...,
        gt = 0,
        description = "Precio en COP/USD mayor a 0",
        example = 3000000.00
    )
    reparado: bool = Field(
        default = False,
        description = "Estado de reparación"
    )

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoUpdate(BaseModel):
    placa_vehiculo: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion_falla: Optional[str] = Field(None, min_length=2, max_length=100)
    costo_estimado: Optional[float] = Field(None, gt=0)
    reparado: Optional[bool] = None

class Vehiculo(VehiculoBase):
    id: UUID = Field(default_factory=uuid4, description="Identificador Único Universal (UUIDv4)")

    class Config:
        from_attributes = True