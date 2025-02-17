#!/bin/bash
# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Run FastAPI application on Azure App Service. (Ignoring all other files, except those in the /api directory)
# Note: Remember to configure the Azure App Service to run the startup.sh script (Settings -> Configuration -> General Settings -> Startup Command -> "startup.sh".
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app