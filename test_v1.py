import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import logging

# Setup logging to a location that definitely has write permissions
log_dir = "C:\\Temp"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, "minimal_service_log.txt")

# Open the log file immediately to verify permissions
with open(log_file, "a") as f:
    f.write(f"\n\n--- Service script started at {time.ctime()} ---\n")

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MinimalService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MinimalPythonService"
    _svc_display_name_ = "Minimal Python Service"
    
    def __init__(self, args):
        with open(log_file, "a") as f:
            f.write("Service __init__ called\n")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        
    def SvcStop(self):
        with open(log_file, "a") as f:
            f.write("SvcStop called\n")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        
    def SvcDoRun(self):
        with open(log_file, "a") as f:
            f.write("SvcDoRun called\n")
        self.main()
        
    def main(self):
        with open(log_file, "a") as f:
            f.write("Main method entered\n")
        while self.is_running:
            with open(log_file, "a") as f:
                f.write(f"Service running at {time.ctime()}\n")
            # Just wait a bit and do nothing
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    with open(log_file, "a") as f:
        f.write(f"Script executed with args: {sys.argv}\n")
    
    try:
        if len(sys.argv) == 1:
            with open(log_file, "a") as f:
                f.write("About to PrepareToHostSingle\n")
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(MinimalService)
            with open(log_file, "a") as f:
                f.write("About to StartServiceCtrlDispatcher\n")
            servicemanager.StartServiceCtrlDispatcher()
            with open(log_file, "a") as f:
                f.write("After StartServiceCtrlDispatcher\n")
        else:
            win32serviceutil.HandleCommandLine(MinimalService)
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"EXCEPTION: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
