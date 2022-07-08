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
        alert("Encuesta " + datosEncuesta[0] +" editada con exito")
        window.location.replace("http://127.0.0.1:5004/");
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

    datosEncuesta.push(idEncuesta)

    console.log(datosEncuesta);
    
    var url_api = "http://127.0.0.1:5004/guardarEditEncuesta"
    fetchDataAsync(url_api, datosEncuesta);
}