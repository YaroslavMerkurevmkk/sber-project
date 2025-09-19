#!/bin/bash

clear
source venv/bin/activate
cd src
uvicorn web.asgi:application --reload --port 8000
