// var csrftoken = '{{ csrf_token }}';

// // フォーム送信時の処理
// $('#parameter_form').submit(function(event) {
//     event.preventDefault();
    
//     var molecular_name = getValues("molecular_name");
//     var molecular_number = getValues("molecular_number");
//     var box_size = getValues("box_size");
//     var pressure = getValues("pressure");
//     var ensemble = getValues("ensemble");
//     var temperature = getValues("temperature");
//     var exe_time = getValues("exe_time");
//     var exe_step = getValues("exe_step");
//     var parameter = {"molecular_name": molecular_name,
//                      "molecular_number": molecular_number,
//                      "box_size": box_size,
//                      "pressure": pressure,
//                      "ensemble": ensemble,
//                      "temperature": temperature,
//                      "exe_time": exe_time,
//                      "exe_step": exe_step,
//                     };
//     var intervalID = setInterval(fetchData, 5000);

//     console.log(JSON.stringify(parameter));
    
//     // $.ajax({
//     //     url: '{% url "ajax_exe_gmx_com" %}',  // コマンドを実行するエンドポイントのURL
//     //     type: 'POST',
//     //     data: JSON.stringify({ command: command}), // 多分parameter
//     //     dataType: 'json',
//     //     contentType: 'application/json',
//     //     headers: {
//     //         'X-CSRFToken': csrftoken
//     //     }
//     // }).done(function(data) {
//     //     console.log('done   リクエストが成功しました。');
//     // }).always(function() { 
//     //     console.log('always リクエストが完了しました。');
//     //     fetchData();
//     //     clearInterval(intervalID);
//     //     console.log('setInterval()をクリアしました')
//     // });
// });

// // 5秒ごとに実行結果を取得する関数
// function fetchData() {
//     $.ajax({
//         url: '{% url "get_output" %}',  // コマンドの実行結果を取得するエンドポイントのURL(user_idを定義する必要がある)
//         type: 'POST',
//         dataType: 'json',
//         contentType: 'application/json',
//         headers: {
//             'X-CSRFToken': csrftoken
//         }
//     }).done(function(data) {
//         console.log("feachData success\n");
//         console.log(data.content);
//         console.log(data.error);
//         // 受信したデータを表示
//         var content = convertNewlineToBr(data.content);
//         //$('#output').text(content);
//         output.innerHTML = content;
//         // スクロール位置を一番下に設定
//         output.scrollTop = output.scrollHeight;
//     }).fail(function() {
//         alert('エラーが起きました');
//     });
// }

// // CSRFトークンを取得する関数
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // クッキー名が一致する場合、値を取得
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// // 改行コードを改行タグに置き換える関数
// function convertNewlineToBr(text) {
//     return text.replace(/\n/g, '<br>');
// }

// // リストの形で要素の値を取得する関数
// function getValues(name) {
//     // 同じ名前の要素を取得
//     var elements = document.getElementsByName(name);
//     var len = elements.length;

//     // 要素の数に応じて処理を分岐
//     if (len === 0) {
//         return -1;
//     } else if(len === 1){
//         // 要素が一つだけの場合、その要素の値を返す
//         var value = elements[0].value;
//         return value;
//     } else {
//         // 複数の要素がある場合、それぞれの要素の値を配列に格納して返す
//         var values = [];
//         for (var i = 0; i < elements.length; i++) {
//             values.push(elements[i].value);
//         }
//         return values;
//     }
// }
