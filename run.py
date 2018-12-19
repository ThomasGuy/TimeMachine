from timeMachine.server import create_app
from timeMachine.crypto.initialize import main


if __name__ == '__main__':
    app = create_app()
    main()
    app.run(host='localhost', port=8080, debug=True)

    # app.debug = True
    # run_simple(
    #     'localhost',
    #     9090,
    #     app,
    #     use_reloader=True,
    #     use_debugger=True,
    #     use_evalex=True,
    #     static_files={'timeMachine/server': ('static/css/**/*.sass')},
    #     reloader_type="watchdog")
