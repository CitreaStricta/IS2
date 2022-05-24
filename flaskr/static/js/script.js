//let XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest; //same as import
var numberOfQuestion = 0;

function addTitle(){
    var container = document.getElementById("containerTitle") // la div class
    // generacion de un campo input (la pregunta en si) 
	var title = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    title.id = "titleId"
    title.placeholder = "Add Title here" // place holder
    
    container.appendChild(title)
    container.appendChild(document.createElement("br")) // br es un salto de linea
    container.appendChild(document.createElement("br")) // br es un salto de linea
}

function addAlternativa(contenedor){
    var containerAlternativa = contenedor // la div class en donde va
    var input = contenedor.getElementsByTagName("input") //pregunta
    //containerAlternativa.appendChild(document.createElement("&nbsp"))
    // generacion de un campo input (la pregunta en si) 
	var alternativa = document.createElement("input") // se refiere a un h1, un div, un boton, un elemento HTML
    alternativa.id = "alternativaId" + input.numberOfAlternativas;
    alternativa.placeholder = "Add Alternativa here" // place holder
    alternativa.name = "input" + input.numberOfAlternativas;

    containerAlternativa.appendChild(alternativa)
}

// genera nuevo campo dinamico al apretar "mas" o "agrega otro campo de pregunta"
function addQuestion(){
	var container = document.getElementById("containerQuestions")
    container.appendChild(document.createElement("br"))
    // generacion de un campo input (la pregunta en si) 
	var input = document.createElement("input")
    input.name = "input" + numberOfQuestion;
    input.id = "inputId" + numberOfQuestion
    input.numberOfAlternativas = 0

    
    var inputElement = document.createElement('button');
    inputElement.innerHTML = "+ alternativa"
    //inputElement.type = "button"
    inputElement.addEventListener('click', function(){
        addAlternativa(container);
        input.numberOfAlternativas++;
    });

    input.placeholder = "Add question here" // place holder
    //addAlternativa(input.number)
    //addAlternativa()

    numberOfQuestion++

    container.appendChild(input)
    container.appendChild(inputElement)
    container.appendChild(document.createElement("br"))

    addAlternativa(container)
    addAlternativa(container)
}

/*function removeQuestion(index){
    var container = document.getElementById("containerQuestions")
    container.remove()
}*/


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





