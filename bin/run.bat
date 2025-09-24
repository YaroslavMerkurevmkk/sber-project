cd ..
call .venv\Scripts\activate.bat
cd src
uvicorn web.asgi:application --reload --port 8000