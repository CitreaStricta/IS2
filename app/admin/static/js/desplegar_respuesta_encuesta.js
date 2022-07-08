function DesplegarEncuestas(btn) {
    var x = document.getElementById("contenido_"+btn.id);
    if (x.style.display === "none" || x.style.display === "") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

function DesplegarRespuestas(btn, db_data_pregunta){
  console.log(db_data_pregunta);

  var element = document.getElementById(btn.id)
  element.classList.add("active");
  var id_encuesta = btn.id;
  $.ajax({
    url: "/obtener_respuestas",
    type: "get",
    data: {id_encuesta: id_encuesta},
    success: function(response) { 
      if($.type(response.porcentajes) === "string"){
        element.classList.remove("active"); // si no hay respuestas
        $("#"+id_encuesta+"_encuesta").html(response.porcentajes);
        
      }
      else{ // si hay respuestas
        for (var i = 0; i < response.porcentajes.length; i++) {
          for (var j = 0; j < response.porcentajes[i].length; j++) {
            $("#"+id_encuesta+"_"+i+"_"+j).append(" ("+response.porcentajes[i][j]+"%)");
          }
        
          var ctx = document.getElementById(i).getContext('2d');
          var MyChart = new Chart(ctx, {
              type: 'doughnut',
              data: {
                  labels: db_data_pregunta[i]['Alternativas'],
                  datasets: [{
                      data: response.n_respuestas[i],
                      backgroundColor: [
                          'rgba(255, 99, 132)',
                          'rgba(54, 162, 235)',
                          'rgba(255, 206, 86)',
                          'rgba(75, 192, 192)',
                          'rgba(153, 102, 255)',
                          'rgba(255, 159, 64)'
                      ],
                      borderColor: [
                          'rgba(255, 99, 132, 1)',
                          'rgba(54, 162, 235, 1)',
                          'rgba(255, 206, 86, 1)',
                          'rgba(75, 192, 192, 1)',
                          'rgba(153, 102, 255, 1)',
                          'rgba(255, 159, 64, 1)'
                      ],
                      borderWidth: 1
                  }]
              },
              options: {
                title: {
                    display: true,
                    text: db_data_pregunta[i]['Pregunta']
                }
              }
          });
        }
      }
    },
    error: function(xhr) {
      //Do Something to handle error
      alert("Error al conectar con la base de datos");
    }
  });

  btn.disabled = true;
}
