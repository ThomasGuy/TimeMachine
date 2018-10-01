from timeMachine.server import create_app
from timeMachine.crypto.initialize import main
from timeMachine.database.models import User, Profile, all_DB_tables
from werkzeug.serving import run_simple
import watchdog

app, Session = create_app()


@app.shell_context_processor
def make_shell_context():
    """Create a shell context for Flask"""
    return {'session': Session(), 'User': User, 'Profile': Profile,
            'tables': all_DB_tables()}


main(Session)
# app.run(host='localhost', port=8080, debug=True)
if __name__ == '__main__':
    app.debug = True
    run_simple(
        'localhost',
        9090,
        app,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        static_files={'timeMachine/server': ('static/sass/**/*.sass')},
        reloader_type="watchdog")
