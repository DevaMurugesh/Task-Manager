# Vercel serverless function handler for FastAPI
# This file wraps the FastAPI app for Vercel deployment

import sys
import os
from mangum import Mangum

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app
from main import app

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")

# Vercel expects the handler to be exported as 'handler' or 'app'
# This is the entry point Vercel will call
