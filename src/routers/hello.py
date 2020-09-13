from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["hello"])
def read_route():
    return {"Hello": "World"}
