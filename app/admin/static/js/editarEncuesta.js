const fetchData = (url_api,datosEncuesta) => {
    
    return new Promise((resolve, reject) => { // resolve se ejecuta cuando la peticion fue exitosa (reject cuando no)

        const xhttp = new XMLHttpRequest(); // instanciacion

        xhttp.open('POST', url_api , true); // "vamos al url de tipo post para ejecutar de forma asincrona"

        xhttp.onreadystatechange = () => {
            if(xhttp.readyState === 4){
                if(xhttp.status === 200){
                    resolve(JSON.parse(xhttp.responseText));
                }else{
                    reject(new Error('Error : ' + url_api));
                }
            }
        }

        xhttp.send(JSON.stringify(datosEncuesta));
    });
}

const fetchDataAsync = async(url_api,datosEncuesta) => {
    try {
        const response = await fetchData(url_api,datosEncuesta);
        
        console.log(response)
<<<<<<< HEAD
        alert("Encuesta " + datosEncuesta[0] +" editada con exito")
        window.location.replace("http://127.0.0.1:5000/");
=======
        alert("¿Encuesta enviada con exito?")
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
    } catch (error) {
        console.error(error.message);
    }
}

function saveEdit(idEncuesta){
    var container = document.getElementById("containerTitulo")
    var encuesta = document.getElementById("containerEncuesta")

    var datosEncuesta = []
    var jsonEncuesta = []

    var titulo = container.getElementsByClassName("titulo")[0].value
    var descripcion = container.getElementsByClassName("descripcion")[0].value
    var fechaComienzo =container.getElementsByClassName("fechaComienzo")[0].value
    var fechaTermino = container.getElementsByClassName("fechaTermino")[0].value

    if(!titulo){
        alert("No puede dejar a la encuesta sin un Titulo")
        return
    }
    datosEncuesta.push(titulo)
    if(!descripcion){
        alert("No puede dejar a la encuesta sin una Descripción")
        return
    }
    datosEncuesta.push(descripcion)
    if(!fechaComienzo){
        alert("Designe una fecha de comienzo a la encuesta")
        return
    }
    datosEncuesta.push(fechaComienzo)
    if(!fechaTermino){
        alert("Designe una fecha de termino a la encuesta")
        return
    }
    datosEncuesta.push(fechaTermino)

    datosEncuesta.push(idEncuesta)

    console.log(datosEncuesta);
    /*
    // Falta ingresar formato para tener en JSON la encuesta
    var listaPreguntas = encuesta.listPreguntas
    if(encuesta.numPreguntas==0){
        alert("Agregue al menos una pregunta a la encuesta")
        return
    }
    var preguntaActual = 0
    var contadorDivs = 0 // este es el contador que iterara por listaPreguntas
    while(preguntaActual<encuesta.numPreguntas){
        var json = {}
        var alternativasDePregunta = []
        var contenidoDePregunta = listaPreguntas.getElementsByTagName("div")[contadorDivs].contenidoPregunta.value
        if(!contenidoDePregunta){
            alert("inserte el enunciado de la pregunta " + (preguntaActual+1))
            return;
        }
        json['Pregunta'] = contenidoDePregunta
        var alternativaActual = 1
        var numAlternativasActual = listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas
        if(numAlternativasActual==0){
            alert("La pregunta " + (preguntaActual+1) + " no tiene alternativas")
            return
        }
        while(alternativaActual <= numAlternativasActual){
            contenidoAlternativa = listaPreguntas.getElementsByTagName("div")[contadorDivs+alternativaActual].contenido.value
            if(!contenidoAlternativa){
                alert("La pregunta " + (preguntaActual+1) + " no tiene contenido en la alternativa " + alternativaActual)
                return
            }
            alternativasDePregunta.push(contenidoAlternativa)
            alternativaActual++
        }
        json['Alternativas'] = alternativasDePregunta
        jsonEncuesta.push(json)
        contadorDivs += listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas
        contadorDivs++
        preguntaActual++
    }
    //console.log(jsonEncuesta);
    datosEncuesta.push(jsonEncuesta)
    */
    var url_api = "http://127.0.0.1:5000/guardarEditEncuesta"
    fetchDataAsync(url_api, datosEncuesta);
}