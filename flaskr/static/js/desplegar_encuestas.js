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