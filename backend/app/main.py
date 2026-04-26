from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION

)

# link the routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/')
async def root(): 
    return {
        'message': 'Welcome to StyleStep AI',
        'version': settings.VERSION,
        'docs': f'{settings.API_V1_STR}/docs'
    }
