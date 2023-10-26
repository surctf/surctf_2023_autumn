#!/bin/bash

socat TCP-LISTEN:8000,fork,reuseaddr "EXEC:python3 main.py"