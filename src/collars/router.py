from fastapi import APIRouter, Depends


collars_router = APIRouter()
router_name = "/collars"


@collars_router.post(f"{router_name}/add_dog")
def add_dog():
    pass
