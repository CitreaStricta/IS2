function DesplegarEncuestas(btn) {
    var x = document.getElementById("contenido_"+btn.id);
    //alert(btn.id );
    if (x.style.display === "none" || x.style.display === "") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
      //alert(btn.id);
    }
  }
function DesplegarRespuestas(btn){
  var element = document.getElementById(btn.id)
  element.classList.add("active");
  var id_encuesta = btn.id;
  $.ajax({
    url: "/get_word",
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
