
    var modal = document.getElementById("myModal");

    var mcontent = document.getElementsByClassName("modal-content")[0];

    var a = document.getElementsByClassName("redirect")[0];

    var btn = document.getElementById("myBtn");

    var span = document.getElementsByClassName("close")[0];

    var del = document.getElementsByClassName("delete")[0];

    var pmodal = document.getElementsByClassName("change")[0];

    btn.onclick = function() {
    modal.style.display = "block";
    }

    span.onclick = function() {
    modal.style.display = "none";
    }

    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        }
    }

    del.onclick = function(){
        mcontent.style.backgroundColor = "green";
        pmodal.innerHTML = "Cliente desvinculado";
        span.style.display = "none";
        del.style.display = "none";
    }