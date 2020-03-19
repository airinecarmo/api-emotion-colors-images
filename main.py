from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from server.gunicorn import Gunicorn, number_of_workers

from server.routers import image_analysis_router
from utils.http_responses import build_error_response

if __name__ == '__main__':

    app = FastAPI(
        title="API for Analysis Colors and Emotions in Images",
        version="1.0.0",
        description="This API aims to analyse images by colors and their emotions.")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(image_analysis_router.router)

    app.debug = True

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request, exc):
        return build_error_response(400, str(exc))


    options = {
        #'bind': '{}:{}'.format(config['API_HOST_NAME'], config['API_PORT']),
        'bind': '0.0.0.0:8080',
        'timeout': 100000000000,
        #'keep-alive': config['KEEP_ALIVE'],
        'workers': number_of_workers(4),
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'log-level': 'warning'
    }

    Gunicorn(app=app, options=options).run()