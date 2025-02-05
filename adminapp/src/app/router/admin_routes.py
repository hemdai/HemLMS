from fastapi.routing import APIRouter


admin_router = APIRouter()


@admin_router.get("/home")
async def home():
    return {"message": "Hello World"}
