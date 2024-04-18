from fastapi import APIRouter, Depends


collars_router = APIRouter()
router_name = "/collars"


@collars_router.post(f"{router_name}/add_dog")
def add_dog():
    pass


@collars_router.post(f"{router_name}/add_collar")
def add_collar():
    pass


@collars_router.post(f"{router_name}/link")
def link_dog_collar():
    pass


@collars_router.post(f"{router_name}/remove_dog")
def remove_dog():
    pass


@collars_router.post(f"{router_name}/remove_collar")
def remove_collar():
    pass


@collars_router.post(f"{router_name}/unlink")
def unlink_dog_collar():
    pass
