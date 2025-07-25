import sys
from src.logger import logging

def error_message_detail(error, sys_module: sys):
    _, _, exc_tb = sys_module.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in Python script name [{0}] at line number [{1}]: {2}".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, sys_module: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, sys_module)

    def __str__(self):
        return self.error_message

# Test Block
if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        raise CustomException(e, sys)
