from timeMachine.server import create_app
from timeMachine.crypto.initialize import main
from timeMachine.database.models import User, Profile, all_DB_tables


app, Session = create_app()
@app.shell_context_processor
def make_shell_context():
    """Create a shell context for Flask"""
    return {'session': Session(), 'User': User, 'Profile':Profile, \
            'tables': all_DB_tables()}

main(Session)
app.run(host='0.0.0.0', port=8080, debug=True)
