function DesplegarEncuestas(btn) {
    var x = document.getElementById(btn.id + "_");
    //alert(btn.id );
    if (x.style.display === "none" || x.style.display === "") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
      //alert(btn.id);
    }
  }
function DesplegarRespuestas(btn){
  //alert(document.getElementById("text"));
  var id_encuesta = btn.id;
  $.ajax({
    url: "/get_word",
    type: "get",
    data: {id_encuesta: id_encuesta},
    success: function(response) {
      if($.type(response.porcentajes) === "string"){
        $("#"+id_encuesta).html(response.porcentajes);
        console.log("#"+id_encuesta);
      }
      else{
        for (var i = 0; i < response.porcentajes.length; i++) {
          for (var j = 0; j < response.porcentajes[0].length; j++) {
            $("#"+id_encuesta+"_"+i+"_"+j).append(" ("+response.porcentajes[i][j]+"%)");
            //document.getElementById(id_encuesta+"_"+i+"_"+j).innerHTML = " ("+response.porcentajes[i][j]+"%)";
            console.log("#"+id_encuesta+"_"+i+"_"+j);
          }
        }
      }
  },
  error: function(xhr) {
    //Do Something to handle error
  }
  });
  //document.getElementById("text").innerHTML="My First JavaScript Function";
}