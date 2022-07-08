from app import create_app

app = create_app()

if __name__ == '__main__':
    #ACORDARSE DE SETEAR DEBUG EN FALSE PARA EL ENVIO DE CORREOS
    app.run(port = 5004, debug = True,threaded=True,use_reloader=False)
