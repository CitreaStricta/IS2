from app import create_app

app = create_app()

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(port = 5000, debug = True)
=======
    app.run(port = 5000, debug = True,threaded=True)
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
