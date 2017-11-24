// api_url = "172.16.67.210"
// api_url = "192.168.62.24"
api_url = "192.168.60.62"
// api_url = "192.168.1.210"

// カテゴリ追加
function addCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var request = new XMLHttpRequest();
  request.open('GET', 'http://'+api_url+':5000/addcate/?title=' + title + '&column=' + add_val);
  request.onreadystatechange = function() {
    if (request.readyState != 4) {
      document.write("OK");
    } else if (request.status != 0) {
      document.write(request.status);
      document.write('失敗');
    } else {
      var result = request.responseText;
    }
  }
  request.send(null);
  readTextFile2();
}

//カテゴリ削除
function deleteCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var request = new XMLHttpRequest();
  request.open('GET', 'http://'+api_url+':5000/deletecate/?title=' + title + '&column=' + add_val);
  request.onreadystatechange = function() {
    if (request.readyState != 4) {
      document.write('OK');
    } else if (request.status != 0) {
      document.write(request.status);
      document.write('失敗');
    } else {
      var result = request.responseText;
    }
  }
  request.send(null);
  location.reload();
}

// 更新
function koshin() {
  location.reload();
}

// エンターキーイベント発火
function enterEvent(code) {
  if (13 === code) {
    dispButton();
  }
}

// カテゴリ検索, 表示
function cateSearch(cate_num) {
  var category = document.getElementById('cate' + String(cate_num)).value;
  var request = new XMLHttpRequest();
  var target = document.getElementById('output4');
  request.open('GET', 'http://'+api_url+':5000/searchcate/?column=' + category);
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200){
      var file_names = JSON.parse(request.response)['titles'];
      url = show(file_names);
    }
    target.innerHTML = url;
  }
  request.send(null);
}

// キーワード検索一覧表示
function dispButton() {
  var word = document.getElementById('s1').value;
  var request = new XMLHttpRequest();
  var target = document.getElementById('output2');
  var url = "<br>";
  request.open("GET", "http://"+api_url+":5000/searchword/?keyword=" + word, true);
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200){
      var file_names = JSON.parse(request.response)['titles'];
      url += show(file_names);
    }
    target.innerHTML = url;
  }
  request.send(null);
}

function categoryButton() {
  var request = new XMLHttpRequest();
  var target = document.getElementById('output3');
  var url = "";
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200){
      var file_names = JSON.parse(request.response)['categories'];
      for (var ii = 0; ii < file_names.length; ii++){
        url += "<input type='button' id='cate" + ii + "' style='font:10pt MS ゴシック; WIDTH:150px; HEIGHT:70px' value='" + file_names[ii] + "' onclick='cateSearch(" + ii + ");'>";
      }
    }
    target.innerHTML = url + "<br>";
  }
  request.open("GET", "http://"+api_url+":5000/getlist_cate/", true);
  request.send(null);
}

function show(file_names){
  var url = "<br>";
  var ei = 0
  for (key in file_names) {
    url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + ei + "' value='" + key + "'>" + key + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + ei + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + ei + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + ei + ");'></input><input type='button'  value='更新' onclick='koshin();'><a href='./test_dlPDF/" + key + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='./test_dlPDF/" + key + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
    for (n = 0; n < file_names[key].length; n++) {
      url += "<input type='button' id='" + key + "s2" + n + "' style='font:10pt MS ゴシック; WIDTH:150px; HEIGHT:70px' value='" + file_names[key][n] + "' onclick='pushingButton(" + n + ", " + ei + ", " + file_names[key].length + ");'>";
    }
    url += "</h4><br>";
    ei += 1;
  }
  return url;
}

function show_test(file_names, category_names){
  var url = "<br>";
  var ei = 0
  for (key in file_names) {
    url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + ei + "' value='" + file_names[key] + "'>" + file_names[key] + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + ei + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + ei + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + ei + ");'></input><input type='button'  value='更新' onclick='koshin();'><a href='./test_dlPDF/" + file_names[key] + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='./test_dlPDF/" + file_names[key] + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
    for (n = 0; n < category_names[ei].length; n++) {
      url += "<input type='button' id='" + file_names[key] + "s2" + n + "' style='font:10pt MS ゴシック; WIDTH:150px; HEIGHT:70px' value='" +  category_names[ei][n] + "' onclick='pushingButton(" + n + ", " + ei + ", " +  file_names.length + ");'>";
    }
    url += "</h4><br>";
    ei += 1;
  }
  return url;
}

// テキストボックスクリア
function clearText() {
  document.getElementById('s1').value = '';
}

// 一覧表示
function readTextFile2() {
  var target = document.getElementById("output");
  var req = new XMLHttpRequest();
  var url = "";
  req.onreadystatechange = function() {
    if(req.readyState == 4 && req.status == 200){
      var file_names = JSON.parse(req.response)['titles'];
      var category_names = JSON.parse(req.response)['category'];
      url += show_test(file_names, category_names);
    }
    target.innerHTML = url;
  };
  req.open("GET", "http://192.168.1.210:5000/getlist/", true);
  req.send(null);
  categoryButton();
}

// カテゴリ -> テキストボックス入力
function pushingButton(a, b, c) {
  tmp = String(a);
  tmp1 = String(b);
  var title = document.getElementById('s31' + tmp1).value;
  var val1 = document.getElementById(title + 's2' + tmp).value;
  for (n = 0; n < c; n++) {
    tmp2 = String(n);
    document.getElementById('sss3' + tmp2).value = '';
  }
  document.getElementById('sss3' + tmp1).value = val1;
}
