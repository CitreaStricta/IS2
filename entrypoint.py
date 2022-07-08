from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port = 5004, debug = False,threaded=True,use_reloader=False)
