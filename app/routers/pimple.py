from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.schemas import CreatePimpleSchema, DeletePimpleSchema, UpdatePimpleSchema
from app.services import PimpleService

router = APIRouter()


@router.get("/pimple", status_code=status.HTTP_200_OK)
async def get_pimples(service: Annotated[PimpleService, Depends(PimpleService)]):
    return await service.get_all()


@router.get("/pimple/{obj_uuid}", status_code=status.HTTP_200_OK)
async def get_pimple(obj_uuid: str, service: Annotated[PimpleService, Depends(PimpleService)]):
    return await service.get(obj_uuid)


@router.post("/pimple", status_code=status.HTTP_201_CREATED)
async def create_pimple(obj: CreatePimpleSchema, service: Annotated[PimpleService, Depends(PimpleService)]):
    return await service.create(obj)


@router.patch("/pimple/{obj_uuid}", status_code=status.HTTP_200_OK)
async def update_pimple(
    obj: UpdatePimpleSchema,
    obj_uuid: str,
    service: Annotated[PimpleService, Depends(PimpleService)],
):
    return await service.update(obj=obj, obj_uuid=obj_uuid)


@router.delete("/pimple/{obj_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pimple(obj_uuid: str, service: Annotated[PimpleService, Depends(PimpleService)]):
    return await service.delete(obj=DeletePimpleSchema(disappeared_at=datetime.now()), obj_uuid=obj_uuid)
