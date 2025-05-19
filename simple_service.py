import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import traceback

# Create a basic direct file logger that doesn't depend on the logging module
log_file = "C:\\Temp\\service_debug.log"

def log(message):
    try:
        with open(log_file, "a") as f:
            f.write(f"{time.ctime()} - {message}\n")
    except:
        # If we can't write to the log, there's not much we can do
        pass

# Make sure the log directory exists
try:
    if not os.path.exists("C:\\Temp"):
        os.makedirs("C:\\Temp")
    log("Service module loaded")
except Exception as e:
    # Can't do much if this fails
    pass

class SimpleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SimpleService"
    _svc_display_name_ = "Simple Python Service"
    
    def __init__(self, args):
        log("Service __init__ called")
        try:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.is_running = True
            log("Service initialized successfully")
        except Exception as e:
            log(f"Error in init: {str(e)}")
            log(traceback.format_exc())
    
    def SvcStop(self):
        log("SvcStop called")
        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.is_running = False
            log("Service stop pending")
        except Exception as e:
            log(f"Error in SvcStop: {str(e)}")
            log(traceback.format_exc())
    
    def SvcDoRun(self):
        log("SvcDoRun called")
        try:
            # Report service status to SCM
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            log("Reported SERVICE_START_PENDING")
            
            # Immediately report that we're running
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            log("Reported SERVICE_RUNNING")
            
            self.main()
        except Exception as e:
            log(f"Error in SvcDoRun: {str(e)}")
            log(traceback.format_exc())
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
    
    def main(self):
        log("Entered main service loop")
        try:
            while self.is_running:
                # Just sleep briefly and log
                log("Service is running")
                rc = win32event.WaitForSingleObject(self.hWaitStop, 3000)
                if rc == win32event.WAIT_OBJECT_0:
                    log("Stop event received")
                    break
            log("Exited main service loop")
        except Exception as e:
            log(f"Error in main loop: {str(e)}")
            log(traceback.format_exc())

if __name__ == '__main__':
    log(f"Script called with arguments: {sys.argv}")
    try:
        if len(sys.argv) == 1:
            log("Starting service dispatcher")
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(SimpleService)
            log("About to call StartServiceCtrlDispatcher")
            servicemanager.StartServiceCtrlDispatcher()
            log("After StartServiceCtrlDispatcher") # This line won't execute until the service stops
        else:
            log(f"Handling command line: {sys.argv}")
            win32serviceutil.HandleCommandLine(SimpleService)
    except Exception as e:
        log(f"Exception in main block: {str(e)}")
        log(traceback.format_exc())
