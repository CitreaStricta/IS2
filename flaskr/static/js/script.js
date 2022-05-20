//let XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest; //same as import
var numberOfQuestion = 0;

// FALTA IMPLEMENTAR BOTON PARA ELIMINAR PREGUNTAS Y BOTON PARA ELIMINAR ALTERNATIVAS
// FALTA INDICAR EL NUMERO DE LA PREGUNTA
function addTitulo(){
    var container = document.getElementById("containerTitulo") // la div class
    // generacion de un campo input (Para asignar titulo) 
	container.titulo = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    container.titulo.id = "titleId"
    container.titulo.placeholder = "Add Title here" // place holder
    
    container.descripcion = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    container.descripcion.id = "descripcionId"
    container.descripcion.placeholder = "Add Descripción here" // place holder

    container.fechaComienzo = document.createElement("input")
    container.fechaComienzo.id= "fechaComienzoId"
    container.fechaComienzo.type= "date"
    container.fechaTermino = document.createElement("input")
    container.fechaTermino.id= "fechaTerminoId"
    container.fechaTermino.type= "date"

    container.appendChild(document.createTextNode("Titulo:"))
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(container.titulo)
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(document.createTextNode("Descripcion:"))
    container.appendChild(document.createElement("br")) // br es un salto de linea
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
    alternativa.contenido.placeholder = "Add Alternativa here" // place holder
    alternativa.contenido.name = "input" + pregunta.numAlternativas;

    alternativa.boton = document.createElement('button');
    alternativa.boton.innerHTML = "- alternativa"
    alternativa.boton.addEventListener('click', function(){
        // funcion que elimina la alternativa
        pregunta.alternativas.removeChild(alternativa)
        pregunta.numAlternativas--
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
    pregunta.contenidoPregunta.placeholder = "Add Pregunta here"

    pregunta.alternativas = document.createElement("ul")
    pregunta.numAlternativas = 0

    pregunta.botonAlternativas = document.createElement('button');
    pregunta.botonAlternativas.innerHTML = "+ alternativa"
    pregunta.botonAlternativas.addEventListener('click', function(){
        addAlternativa(pregunta);
    });

    pregunta.botonPregunta = document.createElement('button');
    pregunta.botonPregunta.innerHTML = "- pregunta"
    pregunta.botonPregunta.addEventListener('click', function(){
        // funcion que elimina la pregunta
        encuesta.numPreguntas--
        encuesta.listPreguntas.removeChild(pregunta)
    });

    pregunta.appendChild(document.createElement("br"))
    pregunta.appendChild(pregunta.contenidoPregunta)
    pregunta.appendChild(pregunta.botonPregunta)
    pregunta.appendChild(pregunta.botonAlternativas)
    pregunta.appendChild(pregunta.alternativas)

    encuesta.listPreguntas.appendChild(pregunta)

    addAlternativa(pregunta)

    numberOfQuestion++;
}

const fetchData = (url_api,listOfQuestions) => {
    
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

        xhttp.send(JSON.stringify(listOfQuestions));
    });
}

const fetchDataAsync = async(url_api,listOfQuestions) => {
    try {
        const response = await fetchData(url_api,listOfQuestions);
        
        console.log(response)
    } catch (error) {
        console.error(error.message);
    }
}

function saveQuestions(){
    var container = document.getElementById("containerTitulo")
    var encuesta = document.getElementById("containerEncuesta")
    var titulo = container.titulo
    var descripcion = container.descripcion
    var fechaComienzo = container.fechaComienzo
    var fechaTermino = container.fechaTermino

    //console.log(container);
    //console.log(encuesta);

    // Falta ingresar formato para tener en JSON la encuesta
    var listaPreguntas = encuesta.listPreguntas
    var preguntas = listaPreguntas.getElementsByTagName("input")
    //console.log(listaPreguntas);
    //console.log(preguntas);
    var preguntaActual = 0
    var contadorDivs = 0 // este es el contador que iterara por listaPreguntas
    var jsonTotal = []
    while(preguntaActual<encuesta.numPreguntas){
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs])
        //console.log(preguntaActual);
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs].contenidoPregunta.value)
        //console.log(listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas)
        var json = []
        json.push(listaPreguntas.getElementsByTagName("div")[contadorDivs].contenidoPregunta.value)
        var alternativaActual = 1
        while(alternativaActual <= listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas){
            json.push(listaPreguntas.getElementsByTagName("div")[contadorDivs+alternativaActual].contenido.value)
            alternativaActual++
        }
        jsonTotal.push(json)
        contadorDivs += listaPreguntas.getElementsByTagName("div")[contadorDivs].numAlternativas
        contadorDivs++
        preguntaActual++
    }
    console.log(jsonTotal);

    /*
    for(var i=0; i<encuesta.numPreguntas;i++){
        console.log(listaPreguntas.getElementsByTagName("div"))
        console.log(i)
    }
    */
}

/*
function saveQuestions(){
    // estructurador de la encuesta (aun no se estan guardando en ninguna parte)
	var container = document.getElementById("containerQuestions") // donde se encuentran todas las preguntas
	var title = document.getElementById("containerTitle").getElementsByTagName("input") // obtiene el elemento de la div class con nombre containerTitle
    var questions = container.getElementsByTagName("input") //pregunta
	var select = container.getElementsByTagName("select") //tipo de respuesta

	var totalQuestions = questions.length // cantidad de preguntas (?)

    // le entrega sus valores a cada pregunta (?)
    listOfQuestions = []
	for(let i=0 ; i<totalQuestions ; i++){
		var questionObject = {}
		var numberOfCurrentquestion = i + 1
		var currentQuestion = questions[i].value
		var typeValue = select[i].value

		questionObject['questionNumber'] = numberOfCurrentquestion
		questionObject['questionText'] = currentQuestion
		questionObject['typeValue'] = typeValue

		listOfQuestions.push(questionObject)
	}
    console.log(title[0].value)
    listOfQuestions.push(title[0].value)

    var url_api = "http://127.0.0.1:5000/guardarEncuesta"
    fetchDataAsync(url_api, listOfQuestions);



	console.log(listOfQuestions)

    

    // aqui debe ir la coneccion con la bd
    // asegurarse de que no se ingresen multiples encuestas iguales cada vez que se precione Guardar


}
*/



/*
// genera nuevo campo dinamico al apretar "mas" o "agrega otro campo de pregunta"
function addQuestion(){
	var container = document.getElementById("containerQuestions")
    // generacion de un campo input (la pregunta en si) 
	var input = document.createElement("input")
    input.name = "input" + numberOfQuestion;
    input.id = "inputId" + numberOfQuestion
    input.contenedor = document.createElement("div")
    input.contenedor.id="contenedorAlternativas"
    input.numberOfAlternativas = 0

    
    var button = document.createElement("button")
    button.innerHTML = '+ alternativa';
    button.value = numberOfAlternativas
    button.onclick = function(){
        console.log("se apreto el boton")
        
        // generacion de un campo input (la pregunta en si) 
        var alternativa = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
        alternativa.id = "alternativaId" + input.numberOfAlternativas;
        alternativa.placeholder = "Add Alternativa here" // place holder
        alternativa.name = "input" + input.numberOfAlternativas;
        input.numberOfAlternativas++;

        input.contenedor.appendChild(alternativa)
        input.contenedor.appendChild(document.createElement("br")) // br es un salto de linea
    };

    input.placeholder = "Add question here" // place holder
    //addAlternativa(input.number)
    //addAlternativa()

    numberOfQuestion++

    container.appendChild(input)
    container.appendChild(button)
    container.appendChild(document.createElement("br"))
}
*/





