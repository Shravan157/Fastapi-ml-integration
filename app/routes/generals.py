from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=['General Endpoints']
)


@router.get('/')
def base_url():
    return JSONResponse(content={'message':'welcome to the app'},status_code=200)
