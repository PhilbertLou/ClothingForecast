function show(){
    let div1 = document.getElementById("more");
    //let div2 = document.getElementById("breaks");

    if (div1.style.display === "none") {
        div1.style.display = "block";
        //div2.style.display = "none";
    }
    else {
        div1.style.display = "none";
        //div2.style.display = "block";
  }
}

function load(){
    let div1 = document.getElementById("main");
    let div2 = document.getElementById("loading");

    div1.style.display = "none";
    div2.style.display = "block";
}

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("morebutton").onclick = show;
})

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("dash").onclick = load;
})

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("logo").onclick = load;
})

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("train").onclick = load;
})

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("trainnew").onclick = load;
})

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("getrec").onclick = load;
})
