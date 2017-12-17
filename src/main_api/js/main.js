// カテゴリ追加
function addCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var huga = 0;
  var request = new XMLHttpRequest();
  request.open('GET', getAPI() + '/addcate/?title=' + title + '&column=' + add_val);
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
}

//カテゴリ削除
function deleteCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var request = new XMLHttpRequest();
  var huga = 0;
  var hoge = setInterval(function() {
    request.open('GET', getAPI() + '/deletecate/?title=' + title + '&column=' + add_val);
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
    huga++;
    if (huga == 1) {
      location.reload();
    }
  }, 2000);
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
  request.open('GET', getAPI() +'/searchcate/?column=' + category);
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200){
      var file_names = JSON.parse(request.response)['titles'];
      url = show(file_names);
    }
    target.innerHTML = url;
  }
  request.send(null);
}

function uploadDateSearch(num) {
  var upload = document.getElementById('date' + String(num)).value;
  var request = new XMLHttpRequest();
  var target = document.getElementById('output6');
  request.open('GET', getAPI() +'/searchdate/?date=' + upload);
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
  request.open("GET", getAPI() + "/searchword/?keyword=" + word, true);
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
  request.open("GET", getAPI() + "/getlist_cate/", true);
  request.send(null);
}

function uploaddateButton(uploadDates) {
  var out = document.getElementById("output5");
  var elementInp = document.createElement('input');
  for(key in uploadDates){
    elementInp = document.createElement('input');
    elementInp.id = 'date' + String(key);
    elementInp.type = 'button';
    elementInp.value = uploadDates[key];
    elementInp.setAttribute("onclick", "uploadDateSearch("+key+");");
    out.appendChild(elementInp);
  }
}

function show(file_names){
  var url = "<br>";
  var ei = 0
  for (key in file_names) {
    url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + ei + "' value='" + key + "'>" + key + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + ei + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + ei + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + ei + ");'></input><input type='button'  value='更新' onclick='koshin();'><a href='../test_dlPDF/" + key + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='../test_dlPDF/" + key + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
    for (n = 0; n < file_names[key].length; n++) {
      url += "<input type='button' id='" + key + "s2" + n + "' style='font:10pt MS ゴシック; WIDTH:150px; HEIGHT:70px' value='" + file_names[key][n] + "' onclick='pushingButton(" + n + ", " + ei + ", " + file_names[key].length + ");'>";
    }
    url += "</h4><div align='center'><img　data-echo='../test_dlPDF/pdfFront/"+key+".jpg' width='256' height='256'></div><br>";
    ei += 1;
  }
  return url;
}

function generateElement(file_names, category_names){
  var elementCh = document.createElement('h3');
  var elementDiv = document.createElement('div');
  var element = document.createElement('div');
  var out = document.getElementById("output");
  var elementCa = document.createElement('h4');
  var elementIn = document.createElement('input');
  var elementIm = document.createElement('img');
  var elementDi = document.createElement('div');
  var elementA = document.createElement('a');

  for (key in file_names) {
    elementCh = document.createElement('h3');

    elementDiv = document.createElement('div');
    elementDiv.style = 'text-align:right;';
    elementDiv.innerHTML = 'カテゴリ：';
    elementCh.appendChild(elementDiv);

    element = document.createElement('div');
    element.style = 'text-align:left;float:left;';
    element.innerHTML = file_names[key];
    elementDiv.appendChild(element);

    element.appendChild(addInputHidden(file_names[key], key));
    elementDiv.appendChild(addInputText(key));

    elementDiv.appendChild(addInputButtonAdd(key, '追加'));
    elementDiv.appendChild(addInputButtonDel(key, '削除'));
    elementDiv.appendChild(addInputButtonKousin(key, '更新'));

    elementA = document.createElement('a');
    elementA.href = '../test_dlPDF/' + file_names[key] + '.pdf#page=1 target="_blank"';
    elementDiv.appendChild(elementA);

    elementA.appendChild(addImageSRC('images/pdf-hiraku.png', 100, 100));

    elementA = document.createElement('a');
    elementA.href = '../test_dlPDF/' + file_names[key] + '.pdf.zip#page=1 target="_blank"';
    elementDiv.appendChild(elementA);

    elementA.appendChild(addImageSRC('images/pdf-DL.png', 100, 100));
    out.appendChild(elementCh);

    elementCa = document.createElement('h4');
    elementCa.innerHTML = 'カテゴリ<br>';

    for (n = 0; n < category_names[key].length; n++) {
      elementIn = document.createElement('input');
      elementIn.type = 'button';
      elementIn.id = file_names[key] + 's2' + String(n);
      elementIn.style='font:10pt MS ゴシック; WIDTH:150px; HEIGHT:70px';
      elementIn.setAttribute('value', category_names[key][n]);
      elementIn.innerHTML = category_names[key][n];
      elementIn.setAttribute('onclick', 'pushingButton('+n+','+key+','+file_names.length+');');
      elementCa.appendChild(elementIn);
    }
    elementDi = document.createElement('div');
    elementDi.align = 'center';

    elementDi.appendChild(addImage(take_image(file_names[key]), 256, 256));
    out.appendChild(elementCa);
    out.appendChild(elementDi);
  }
}

function addInputHidden(file_name, key){
  elementInp = document.createElement('input');
  elementInp.type = 'hidden';
  elementInp.id = 's31' + String(key);
  elementInp.value = file_name;
  return elementInp;
}

function addInputText(key){
  elementInp = document.createElement('input');
  elementInp.type = 'text';
  elementInp.id = 'sss3' + String(key);
  elementInp.value = '';
  return elementInp;
}

function addImage(path, wid, hei){
  elementImg = document.createElement('img');
  elementImg.setAttribute('data-echo', path);
  elementImg.width = wid;
  elementImg.height = hei;
  return elementImg;
}

function addImageSRC(path, wid, hei){
  elementImg = document.createElement('img');
  elementImg.setAttribute('src', path);
  elementImg.width = wid;
  elementImg.height = hei;
  return elementImg;
}

function addInputButtonAdd(key, val){
  elementInp = document.createElement('input');
  elementInp.type = 'button';
  elementInp.value = val;
  elementInp.setAttribute("onclick", "addCategory("+key+");");
  return elementInp;
}

function addInputButtonDel(key, val){
  elementInp = document.createElement('input');
  elementInp.type = 'button';
  elementInp.value = val;
  elementInp.setAttribute('onclick', 'deleteWrap('+key+');');
  return elementInp;
}

function addInputButtonKousin(key, val){
  elementInp = document.createElement('input');
  elementInp.type = 'button';
  elementInp.value = val;
  elementInp.setAttribute('onclick', 'reloadWrap();');
  return elementInp;
}

function pushingWrap(n, key, fileNamesLength){
  return function(){
    pushingButton(n, key, fileNamesLength);
  };
}

function addWrap(key){
  return addCategory(key);
}

function deleteWrap(key){
  return function(){
    deleteCategory(key);
  };
}

function reloadWrap(){
  return function(){
    koshin();
  };
}

function take_image(file_name){
  var img = new Image();
  img.src = '../test_dlPDF/pdfFront/'+file_name+'.jpg';
  if(img.width == 0){
    return '../test_dlPDF/pdfFront/'+file_name+'.jpg';
  }
  return '../test_dlPDF/pdfFront/'+file_name+'.jpg';
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
  req.open("GET", getAPI() + "/getlist/", true);
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
