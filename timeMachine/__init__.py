import sys
import os
import logging
import logging.config

current_dir = os.path.dirname(os.path.realpath(__file__))
package_dir = os.path.realpath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, package_dir)


# If applicable, delete the existing log file to generate a fresh log
#  file during each execution
# if os.path.isfile(package_dir + "/logs/timeMachine.log"):
#     os.remove(package_dir + "/logs/timeMachine.log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=package_dir + '/logs/timeMachine.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')
# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
# logging.getLogger(__name__).addHandler(console)

from timeMachine.server import create_app, session_factory
from timeMachine.crypto.initialize import main


app = create_app()
main(session_factory)
