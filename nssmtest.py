import time
import sys
import os

# Set up logging
log_file = "C:\\Temp\\python_worker.log"

def log(message):
    with open(log_file, "a") as f:
        f.write(f"{time.ctime()} - {message}\n")

log("Script started")

# Your actual service code here
try:
    while True:
        log("Worker is running")
        # Do your work here
        time.sleep(10)
except KeyboardInterrupt:
    log("Service stopped by keyboard interrupt")
except Exception as e:
    log(f"Error: {str(e)}")
    import traceback
    log(traceback.format_exc())
