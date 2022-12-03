#!/bin/bash
cd app && python3.8 -m uvicorn main:app --host 0.0.0.0 --port 3000
