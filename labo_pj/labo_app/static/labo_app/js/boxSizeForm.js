function changeSizeByWidth(){
    let box_select = document.getElementById("box_select_0").checked;
    if(box_select){
        let box_width = document.getElementById("width");
        let box_depth = document.getElementById("depth");
        let box_height = document.getElementById("height");
        box_depth.value = box_width.value;
        box_height.value = box_width.value;
    }
}

function changeSizeByDepth(){
    let box_select = document.getElementById("box_select_0").checked;
    if(box_select){
        let box_width = document.getElementById("width");
        let box_depth = document.getElementById("depth");
        let box_height = document.getElementById("height");
        box_width.value = box_depth.value;
        box_height.value = box_depth.value;
    }
}

function changeSizeByHeight(){
    let box_select = document.getElementById("box_select_0").checked;
    if(box_select){
        let box_width = document.getElementById("width");
        let box_depth = document.getElementById("depth");
        let box_height = document.getElementById("height");
        box_width.value = box_height.value;
        box_depth.value = box_height.value;
    }
}

