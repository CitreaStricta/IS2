function DesplegarEncuestas(btn) {
    var x = document.getElementById("contenido_"+btn.id);
<<<<<<< HEAD
    //alert(btn.id );
=======
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
    if (x.style.display === "none" || x.style.display === "") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
<<<<<<< HEAD
      //alert(btn.id);
=======
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
    }
  }

function DesplegarRespuestas(btn){
  var element = document.getElementById(btn.id)
  element.classList.add("active");
  var id_encuesta = btn.id;
  $.ajax({
<<<<<<< HEAD
    url: "/get_word",
=======
    url: "/obtener_respuestas",
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
    type: "get",
    data: {id_encuesta: id_encuesta},
    success: function(response) {
      if($.type(response.porcentajes) === "string"){
        element.classList.remove("active");
        $("#"+id_encuesta).html(response.porcentajes);
        
      }
      else{
        for (var i = 0; i < response.porcentajes.length; i++) {
          for (var j = 0; j < response.porcentajes[0].length; j++) {
            $("#"+id_encuesta+"_"+i+"_"+j).append(" ("+response.porcentajes[i][j]+"%)");
          }
        }
        setTimeout(function(){
          element.classList.add("success");
        },100)
      }
  },
  error: function(xhr) {
    //Do Something to handle error
    alert("Error al conectar con la base de datos");
  }
  });

  btn.disabled = true;
}
