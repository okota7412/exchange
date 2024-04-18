let i = 1 ;

function addForm() {
    i++ ;
    // 複製するHTML要素を取得 
    let content_area = document.getElementById("form_area1");

    // 複製
    let clone_element = content_area.cloneNode(true);

    // 複製した要素の属性を編集
    clone_element.id = "form_area" + i;
    
    // 複製したHTML要素をページに挿入
    let x = "form_area" + (i-1);
    let insert_area = document.getElementById(x);
    insert_area.after(clone_element);
    
    let div_data = document.createElement("div");
    let p_data = document.createElement("p");
    let button_data = document.createElement('input');
    div_data.setAttribute("class", "col-md-2");
    button_data.id = i;
    button_data.type = "button";
    button_data.value = "フォームを削除";
    button_data.onclick = function(){deleteBtn(this);}
    clone_element.appendChild(div_data);
    div_data.appendChild(p_data);
    div_data.appendChild(button_data);
    // console.log(i)
}

function deleteBtn(target) {
    let target_id = target.id;
    let parent = document.getElementById('form_area'+ target_id);
    parent.remove();
    // console.log(target)
    i--;
}