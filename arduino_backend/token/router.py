from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["token"])
def get_tokens():
    return {"get": "token"}


@router.post("/", tags=["token"])
def add_token():
    return {"post": "token"}


@router.get("/{token_id}", tags=["token"])
def get_single_token():
    return {"single": "token"}


@router.put("/{token_id}", tags=["token"])
def edit_token():
    return {"edit": "token"}


@router.delete("/{token_id}", tags=["token"])
def delete_token():
    return {"delete": "token"}
