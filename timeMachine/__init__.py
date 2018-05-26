import sys
import os
import logging

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

logging.getLogger(__name__)


from .api.initialize import start
