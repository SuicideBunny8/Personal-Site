from logging import Filter
from pprint import pprint
import logging

class ManageSQLFilter(Filter):
    def filter(self, record):
        if (hasattr(record, 'funcName') and record.funcName == 'execute'):
            return False
        else:
            return True