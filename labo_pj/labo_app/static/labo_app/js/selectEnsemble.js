function nptPressure(){
    let pressure_area = document.getElementById("pressure_area");
    let box_area = document.getElementById("box_area");
    let box_size_form = document.getElementsByName("box_size");
    let pressure_form = document.getElementsByName("pressure");
    Array.prototype.forEach.call(box_size_form, function (element) {
        element.classList.remove("required");
        element.required = false;
    });
    pressure_form[0].classList.add("required");
    pressure_form[0].required = true;
    pressure_area.style.visibility="visible";
    box_area.style.display="none";
}

function nvtBox(){
    let pressure_area = document.getElementById("pressure_area");
    let box_area = document.getElementById("box_area");
    let box_size_form = document.getElementsByName("box_size");
    let pressure_form = document.getElementsByName("pressure");
    Array.prototype.forEach.call(box_size_form, function (element) {
        element.classList.add("required");
        element.required = true;
    });
    pressure_form[0].classList.remove("required");
    pressure_form[0].required = false;
    pressure_area.style.visibility="hidden";
    box_area.style.display="";
}