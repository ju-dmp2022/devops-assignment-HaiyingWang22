import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi import HTTPException
import numpy as np

from calculator_helper import CalculatorHelper

from models import Calculation, User, ResultResponse, UserResponse, ErrorResponse

def normal_dist_sleep(mean=2, stddev=1, min_sleep=1, max_sleep=4):
    while True:
        # Generate a sleep time from a normal distribution
        sleep_time = np.random.normal(mean, stddev)
        # Check if the sleep time is within the allowed range
        if min_sleep <= sleep_time <= max_sleep:
            break  # If it's within the range, proceed

    # Sleep for the computed duration
    time.sleep(sleep_time)

# init FastAPI app
app = FastAPI(title='Calculator', docs_url='/', description="Calculator API", version='1.0.0')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# defining exceptional JSON-response
@app.exception_handler(Exception)
async def error_handler(request, exc):
    return JSONResponse({
        'detail': f'{exc}'
    })

@app.post('/calculate', operation_id='calculate', summary='Basic arithmetic calculation', response_model=ResultResponse, tags=["actions"], responses={500: {"model": ErrorResponse}})
async def calc(body: Calculation):
    try:
        result = body.calculate()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/register', operation_id='register', summary='Register new user', response_model=UserResponse, tags=["actions"], responses={409: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def register(body: User):
    try:
        result = body.register()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=409, detail='User already exists.')
    return result


@app.post('/login', operation_id='login', summary='Login a user', response_model=UserResponse, tags=["actions"], responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def login(body: User):
    try:
        result = body.login()
        normal_dist_sleep()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=400, detail='Wrong username of password.')
    return result

@app.get('/users/current', operation_id='users_current', summary='Get current logged in user', response_model=UserResponse, tags=["actions"], responses={204: {"model": None}, 500: {"model": ErrorResponse}})
async def users_current():
    def current_user():
        user = CalculatorHelper().get_current_user()
        if user is not None:
            response = UserResponse()
            response.username = user.username
            return response
        return None

    try:
        result = current_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=204, detail='No user has signed in.')
    return result


@app.post('/logout', operation_id='logout', summary='Logout current user', response_model=UserResponse, tags=["actions"], responses={500: {"model": ErrorResponse}})
async def logout():
    def logout():
        user = CalculatorHelper().logout()
        if user is not None:
            response = UserResponse()
            response.username = user.username
            return response
        return None

    try:
        result = logout()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=204, detail='No user has signed in.')
    return result

def main(args):
    import os
    import uvicorn
    import argparse

    def ifenv(key, default):
        return (
            {'default': os.environ.get(key)} if os.environ.get(key)
            else {'default': default}
        )

    parser = argparse.ArgumentParser(description='Calculator server')

    parser.add_argument('--port', type=int, default='5000', help='Port, 5000 is default')
    parser.add_argument("--loglevel", **ifenv('LOGLEVEL', 'DEBUG'), choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set Flask logging level, DEBUG is default")
    parser.add_argument('--debug', action='store_true', help='Flask debug')
    parser.add_argument('--no-debug', dest='debug', action='store_false', help='Flask no debug is default')
    parser.add_argument('-r', '--rest', action='store_true')
    parser.set_defaults(debug=True)

    args = parser.parse_args()

    # Listen on all network interfaces
    #app.run('0.0.0.0', port=args.flask_port, debug=args.debug)
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

