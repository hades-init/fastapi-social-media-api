import multiprocessing

# Server socket - listen for incoming requests
bind = "0.0.0.0:8000"

# Workers
# 2 x CPU cores + 1
workers = 2 * multiprocessing.cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Process-naming
# proc_name = "fastapi-app"