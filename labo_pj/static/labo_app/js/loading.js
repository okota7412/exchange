let button = document.getElementById("simulation");
let first = true;
button.addEventListener("click", () => {
    let requiredElems = document.querySelectorAll(".required");
    if(checkAllForm(requiredElems)){
        if(!first){
            var result = window.confirm('再度シミュレーションを実行しますがよろしいですか？');
    
            if( result ) {
                button.innerHTML = `<div class="loading"></div>`;
            }
            else {
                console.log('キャンセルがクリックされました');
            }
        }else{
            button.innerHTML = `<div class="loading"></div>`;
            first = false;
        }
    }
});

function checkAllForm(list){
    let count = list.length;
    list.forEach(elem => {
        if(elem.value === "") {
            console.log("failure")
        }else{
            console.log("success")
            count = count - 1;
        }
    });
    if(count > 0){
        return false;
    }else{
        return true;
    }
}