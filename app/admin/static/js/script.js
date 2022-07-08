//let XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest; //same as import
var numberOfQuestion = 0;

// FALTA IMPLEMENTAR BOTON PARA ELIMINAR PREGUNTAS Y BOTON PARA ELIMINAR ALTERNATIVAS
// FALTA INDICAR EL NUMERO DE LA PREGUNTA
function addTitulo(){
    var container = document.getElementById("containerTitulo") // la div class
    // generacion de un campo input (Para asignar titulo) 
	container.titulo = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    container.titulo.id = "titleId"
    container.titulo.placeholder = "Agregue el Título aquí" // place holder
    container.titulo.className = "form-control form-control-lg"
    
    container.descripcion = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    container.descripcion.id = "descripcionId"
    container.descripcion.placeholder = "Agregue una Descripción aquí" // place holder
    container.descripcion.className = "form-control"

    container.fechaComienzo = document.createElement("input")
    container.fechaComienzo.id= "fechaComienzoId"
    container.fechaComienzo.type= "date"
    container.fechaComienzo.className = "me-5"
    container.fechaTermino = document.createElement("input")
    container.fechaTermino.id= "fechaTerminoId"
    container.fechaTermino.type= "date"

    const titulo = document.createElement("h1");
    titulo.textContent = "Título";
    const descripcion = document.createElement("h3");
    descripcion.textContent = "Descripción";
    container.appendChild(titulo/*document.createTextNode("Titulo:")*/)
    container.appendChild(container.titulo)
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(descripcion)
    container.appendChild(container.descripcion)
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(document.createTextNode("Fecha Comienzo:"))
    container.appendChild(container.fechaComienzo)
    container.appendChild(document.createTextNode("   Fecha Termino:"))
    container.appendChild(container.fechaTermino)
}

function addAlternativa(pregunta){
    //containerAlternativa.appendChild(document.createElement("&nbsp"))
    // generacion de un campo input (la pregunta en si) 

    var alternativa = document.createElement("div")

	alternativa.contenido = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    alternativa.contenido.id = "alternativaId" + pregunta.numAlternativas;
    alternativa.contenido.placeholder = "Agregue una Alternativa aquí" // place holder
    alternativa.contenido.name = "input" + pregunta.numAlternativas;
    alternativa.contenido.className="form-control form-control-sm col-6"

    alternativa.boton = document.createElement('button');
    alternativa.boton.className = "btn btn-outline-dark m-2"
    alternativa.boton.innerHTML = "- alternativa"
    alternativa.boton.addEventListener('click', function(){
        // funcion que elimina la alternativa
        if(pregunta.numAlternativas<=2){
            alert("Se tiene que tener un minimo de dos alternativas por pregunta")
        }
        else{
            pregunta.alternativas.removeChild(alternativa)
            pregunta.numAlternativas--    
        }
        
    });

    alternativa.appendChild(alternativa.contenido)
    alternativa.appendChild(alternativa.boton)
    alternativa.appendChild(document.createElement("br"))

    pregunta.numAlternativas++
    pregunta.alternativas.appendChild(alternativa)
}

// genera nuevo campo dinamico al apretar "mas" o "agrega otro campo de pregunta"
function addEncuesta(){
    var encuesta = document.getElementById("containerEncuesta")
    var listPregunta = document.createElement("ul")
    listPregunta.style = "padding-left: 0!important;"
    encuesta.listPreguntas = listPregunta
    encuesta.numPreguntas=0

    encuesta.appendChild(encuesta.listPreguntas)
}

function addQuestion(){
    var encuesta = document.getElementById("containerEncuesta")
    encuesta.numPreguntas++
    
    var pregunta = document.createElement("div")

    pregunta.contenidoPregunta = document.createElement("input")
    pregunta.contenidoPregunta.name = "input" + numberOfQuestion
    pregunta.contenidoPregunta.id = "inputId" + numberOfQuestion
    pregunta.contenidoPregunta.placeholder = "Agregue una Pregunta aquí"
    pregunta.contenidoPregunta.className = "form-control"
    //pregunta.revisarContenidoPregunta = document.createElement("div")
    //pregunta.revisarContenidoPregunta.appendChild(document.createTextNode("Vacio"))
    //if(!pregunta.contenidoPregunta){
    //    pregunta.revisarContenidoPregunta.style.display="block";
    //}

    pregunta.alternativas = document.createElement("ul")
    pregunta.alternativas.style = "padding: 0px 50px!important;"
    pregunta.numAlternativas = 0

    pregunta.botonAlternativas = document.createElement('button');
    pregunta.botonAlternativas.innerHTML = "+ alternativa"
    pregunta.botonAlternativas.className = "btn btn-outline-dark m-2"
    pregunta.botonAlternativas.addEventListener('click', function(){
        addAlternativa(pregunta);
    });

    pregunta.botonPregunta = document.createElement('button');
    pregunta.botonPregunta.innerHTML = "- pregunta"
    pregunta.botonPregunta.className = "btn btn-outline-dark m-2"
    pregunta.botonPregunta.addEventListener('click', function(){
        // funcion que elimina la pregunta
        encuesta.numPreguntas--
        encuesta.listPreguntas.removeChild(pregunta)
    });

    pregunta.appendChild(document.createElement("br"))
    pregunta.appendChild(pregunta.contenidoPregunta)
    pregunta.appendChild(pregunta.botonPregunta)
    pregunta.appendChild(pregunta.botonAlternativas)
    //pregunta.appendChild(pregunta.revisarContenidoPregunta)
    pregunta.appendChild(pregunta.alternativas)

    encuesta.listPreguntas.appendChild(pregunta)

    addAlternativa(pregunta)
    addAlternativa(pregunta)

    numberOfQuestion++;
}

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
        alert("Encuesta " + datosEncuesta[0] +" enviada con exito")
        window.location.replace("http://152.74.52.191:5004/");
    } catch (error) {
        console.error(error.message);
        alert("Ocurrio un error, vuelva a intentarlo mas tarde")
    }
}

function saveQuestions(){
    var container = document.getElementById("containerTitulo")
    var encuesta = document.getElementById("containerEncuesta")

    var datosEncuesta = []
    var jsonEncuesta = []

    var titulo = container.titulo.value
    var descripcion = container.descripcion.value
    var fechaComienzo = container.fechaComienzo.value
    var fechaTermino = container.fechaTermino.value

    if(!titulo){
        alert("Inserte un Titulo a la encuesta")
        return
    }
    datosEncuesta.push(titulo)
    if(!descripcion){
        alert("Inserte una Descripción a la encuesta")
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
    let today = new Date().toISOString().slice(0, 10)
    //console.log(today);
    //console.log(fechaComienzo);
    if(fechaComienzo < today){
        alert("Inserte una fecha de Comienzo desde hoy")
        return
    }
    if(fechaComienzo>fechaTermino){
        alert("La fecha de termino tiene que ser el mismo dia que la fecha de comienzo o posterior")
        return
    }
    datosEncuesta.push(fechaTermino)
    

    //console.log(datosEncuesta);

    // Falta ingresar formato para tener en JSON la encuesta
    var listaPreguntas = encuesta.listPreguntas
    if(encuesta.numPreguntas==0){
        alert("Agregue al menos una pregunta a la encuesta")
        return
    }
    var preguntaActual = 0
    var contadorDivs = 0 // este es el contador que iterara por listaPreguntas
    while(preguntaActual<encuesta.numPreguntas){
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs])
        //console.log(preguntaActual);
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs].contenidoPregunta.value)
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas)
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

    console.log(datosEncuesta);
    
    var url_api = "http://152.74.52.191:5004/guardarEncuesta"
    fetchDataAsync(url_api, datosEncuesta);
}