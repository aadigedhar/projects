import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import logging
import traceback

# Configure logging to a file with full permissions
log_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'service_log.log'))
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyPythonService"
    _svc_display_name_ = "My Python Service"
    _svc_description_ = "Python Service Example"

    def __init__(self, args):
        try:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
            self.is_running = True
            self.timeout = 3000  # 3 seconds
            logging.info('Service initialized')
        except Exception as e:
            logging.error(f"Service init error: {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def SvcStop(self):
        try:
            logging.info('Stopping service...')
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.is_running = False
            logging.info('Service stop pending...')
        except Exception as e:
            logging.error(f"SvcStop error: {str(e)}")
            logging.error(traceback.format_exc())

    def SvcDoRun(self):
        try:
            logging.info('Starting service...')
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            self.main()
        except Exception as e:
            logging.error(f"SvcDoRun error: {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def main(self):
        try:
            logging.info('Service is now running')
            # Your service code here - keep this minimal for startup
            while self.is_running:
                # Use RC_WAIT to make the service responsive to stop requests
                result = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                if result == win32event.WAIT_OBJECT_0:
                    # Stop signal received
                    break
                
                # Do minimal work here - just enough to show it's working
                logging.info('Service heartbeat')
                
                # More complex work should go here, but be careful not to block for too long
                
            logging.info('Service main loop completed')
        except Exception as e:
            logging.error(f"Main loop error: {str(e)}")
            logging.error(traceback.format_exc())

if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(MyPythonService)
            servicemanager.StartServiceCtrlDispatcher()
        except Exception as e:
            logging.error(f"Service dispatcher error: {str(e)}")
            logging.error(traceback.format_exc())
    else:
        win32serviceutil.HandleCommandLine(MyPythonService)
