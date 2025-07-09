import logging
import traceback
import os
class ErrorLogger():
    def __init__(self):
        self.log_file = "error_log.txt"
        
        
        logging.basicConfig(
            filename=self.log_file,
            filemode='w',
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def record(self,e):
        logging.exception(e)








def local():
    the_ErrorLogger = ErrorLogger()
    try:
        1 / 0
    except Exception as e:
        print("=== print_exc ===")
        traceback.print_exc()

        print("\n=== using error logger===")
        the_ErrorLogger.record(e)


# local()