from timeMachine.server import create_app, session_factory
from timeMachine.crypto.initialize import main


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
    # main(session_factory)
    pass
