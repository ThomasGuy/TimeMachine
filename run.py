from timeMachine.server import create_app, session_factory
from timeMachine.crypto.initialize import main2
from timeMachine.database.models import User, Profile, all_DB_tables


main2(session_factory)

app = create_app()
# @app.shell_context_processor
# def make_shell_context():
#     """Create a shell context for Flask"""
#     return {'session': session_factory(), 'User': User, 'Profile':Profile, \
#             'tables': all_DB_tables()}

app.run(debug=True)
