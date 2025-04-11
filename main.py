from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import auth
from db.session import init

app = FastAPI(default_response_class=ORJSONResponse,
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              )
app.include_router(auth.router, prefix='/auth')
init()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
