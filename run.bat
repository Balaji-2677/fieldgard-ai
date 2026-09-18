@echo off
title Crop Yield AI - Farmer Prediction Platform
echo =======================================================
echo          🌾 Crop Yield Prediction Platform 🌾
echo =======================================================
echo Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

set PYTHONIOENCODING=utf-8
echo Starting Flask web server at http://127.0.0.1:5000 ...
python app.py
pause
