// カテゴリ追加
function addCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var file = "./PDF_list_column.txt";
  var request = new XMLHttpRequest();
  request.open('GET', 'http://192.168.60.62:5000/?title=' + title + '&column=' + add_val);
  // request.open('GET', 'http://192.168.1.210:5000/?title=' + title + '&column=' + add_val);
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
  document.getElementById('sss3' + tmp).value = '';
  readTextFile2();
  var request1 = new XMLHttpRequest();
  request1.open('GET', 'http://192.168.60.62:5000/update/');
  // request.open('GET', 'http://192.168.1.210:5000/update/');
  request1.onreadystatechange = function() {
    if (request1.readyState != 4) {
      document.write("OK");
    } else if (request1.status != 0) {
      document.write(request1.status);
      document.write('失敗');
    } else {
      var result = request.responseText;
    }
  }
  request1.send(null);
}

//カテゴリ削除
function deleteCategory(a) {
  tmp = String(a)
  var add_val = document.getElementById('sss3' + tmp).value;
  var title = document.getElementById('s31' + tmp).value;
  var file = "./PDF_list_column.txt";
  var request = new XMLHttpRequest();
  request.open('GET', 'http://192.168.60.62:5000/delete/?title=' + title + '&column=' + add_val);
  // request.open('GET', 'http://192.168.1.210:5000/delete/?title=' + title + '&column=' + add_val);
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
  document.getElementById('sss3' + tmp).value = '';
  readTextFile2();
  var request1 = new XMLHttpRequest();
  request1.open('GET', 'http://192.168.60.62:5000/update/');
  // request1.open('GET', 'http://192.168.1.210:5000/update/');
  request1.onreadystatechange = function() {
    if (request1.readyState != 4) {
      document.write('OK')
    } else if (request1.status != 0) {
      document.write(request1.status);
      document.write('失敗');
    } else {
      var result = request.responseText;
    }
  }
  request1.send(null);
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
function cateSearch(a) {
  var file2 = "./PDF_list_column.txt";
  var rawFile2 = new XMLHttpRequest();
  var dic = {};
  rawFile2.open("GET", file2, false);
  rawFile2.onreadystatechange = function() {
    if (rawFile2.readyState == 4) {
      if (rawFile2.status === 200 || rawFile2.status == 0) {
        var allText2 = rawFile2.responseText;
        file_names2 = allText2.split("\n");
        for (var i = 0; i < file_names2.length; i++) {
          columns = file_names2[i].split(",");
          dic[columns[0]] = new Array();
          for (var ii = 1; ii < columns.length; ii++) {
            dic[columns[0]].push(columns[ii]);
          }
        }
      }
    }
  }
  rawFile2.send(null);
  var tmp = String(a)
  var file5 = "./cate_search.txt";
  var rawFile5 = new XMLHttpRequest();
  var category = document.getElementById('cate' + tmp).value;
  var target = document.getElementById('output4');
  var url = "<br>";
  rawFile5.open("GET", file5, false);
  rawFile5.onreadystatechange = function() {
    if (rawFile5.readyState == 4) {
      if (rawFile5.status === 200 || rawFile5.status == 0) {
        var allText5 = rawFile5.responseText;
        file_names5 = allText5.split("\n");
        for (var i = 0; i < file_names5.length; i++) {
          var title_list = file_names5[i].split(",");
          if (category == title_list[0]) {
            var file0 = "./PDF_list_column.txt";
            var rawFile0 = new XMLHttpRequest();
            rawFile0.open("GET", file0, false);
            rawFile0.onreadystatechange = function() {
              if (rawFile0.readyState == 4) {
                if (rawFile0.status === 200 || rawFile0.status == 0) {
                  var allText0 = rawFile0.responseText;
                  file_names0 = allText0.split("\n");
                  for (var ei = 0; ei < file_names0.length; ei++) {
                    if (title_list.indexOf(file_names0[ei].split(',')[0]) != -1) {
                      title0 = file_names[ei].split(',')[0]
                      url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + ei + "' value='" + title0 + "'>" + title0 + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + ei + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + ei + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + ei + ");'></input><input type='button'  value='更新' onclick='koshin();'><a href='dlPDF/" + title0 + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='dlPDF/" + title0 + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
                      if (title0 in dic) {
                        for (n = 0; n < dic[title0].length; n++) {
                          url += "<input type='button' style='font:200pt MS ゴシック; WIDTH:150px; HEIGHT:150px' value='" + dic[title0][n] + "' onclick='pushingButton(" + n + ", " + ei + ", " + file_names0.length + ");'>";
                        }
                      }
                      url += "</h4><br>";
                    }
                  }
                }
              }
            }
            rawFile0.send(null);
          }
        }
      }
    }
  }
  rawFile5.send(null);
  target.innerHTML = url;
}

// 一覧表示
function dispButton() {
  var file2 = "./PDF_list_column.txt";
  var rawFile2 = new XMLHttpRequest();
  var dic = {};
  rawFile2.open("GET", file2, false);
  rawFile2.onreadystatechange = function() {
    if (rawFile2.readyState == 4) {
      if (rawFile2.status === 200 || rawFile2.status == 0) {
        var allText2 = rawFile2.responseText;
        file_names2 = allText2.split("\n");
        for (var i = 0; i < file_names2.length; i++) {
          columns = file_names2[i].split(",");
          dic[columns[0]] = new Array();
          for (var ii = 1; ii < columns.length; ii++) {
            dic[columns[0]].push(columns[ii]);
          }
        }
      }
    }
  }
  rawFile2.send(null);
  var val = document.getElementById('s1').value;
  var target = document.getElementById("output2");
  var url = "<br>";
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if(req.readyState == 4 && req.status == 200){
      var file_names = JSON.parse(req.response)['pdfs'];
      for (var i = 0; i < file_names.length; i++) {
        if (file_names[i].indexOf(val) != -1) {
          url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + i + "' value='" + file_names[i] + "'>" + file_names[i] + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + i + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + i + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + i + ");'></input><input type='button' value='更新' onclick='koshin();'></input><a href='dlPDF/" + file_names[i] + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='dlPDF/" + file_names[i] + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
          if (file_names[i] in dic) {
            for (n = 0; n < dic[file_names[i]].length; n++) {
              url += "<input type='button' id='" + file_names[i] + "s2" + n + "' style='font:200pt MS ゴシック; WIDTH:150px; HEIGHT:150px' value='" + dic[file_names[i]][n] + "' onclick='pushingButton(" + n + "," + i + "," + file_names.length + ");'>";
            }
          }
          url += "</h4><br>";
        }
        target.innerHTML = url;
      }
    }
  }
  // req.open("GET", "http://192.168.1.210:5000/getlist/", true);
  req.open("GET", "http://192.168.60.62:5000/getlist/", true);
  req.send(null);
}

// テキストボックスクリア
function clearText() {
  document.getElementById('s1').value = '';
}

// 一覧表示
function readTextFile2() {
  var file = "./PDF_list.txt";
  var file2 = "./PDF_list_column.txt";
  var url = "";
  var target2 = document.getElementById("output");
  var rawFile = new XMLHttpRequest();
  var rawFile2 = new XMLHttpRequest();
  var dic = {};
  rawFile2.open("GET", file2, false);
  rawFile2.onreadystatechange = function() {
    if (rawFile2.readyState == 4) {
      if (rawFile2.status === 200 || rawFile2.status == 0) {
        var allText2 = rawFile2.responseText;
        file_names2 = allText2.split("\n");
        for (var i = 0; i < file_names2.length; i++) {
          columns = file_names2[i].split(",");
          dic[columns[0]] = new Array();
          for (var ii = 1; ii < columns.length; ii++) {
            dic[columns[0]].push(columns[ii]);
          }
        }
      }
    }
  }
  rawFile2.send(null);
  var target = document.getElementById("output");
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if(req.readyState == 4 && req.status == 200){
      var file_names = JSON.parse(req.response)['pdfs'];
      for (var i = 0; i < file_names.length; i++) {
        url += "<h3><div style='text-align:right;'><div style='text-align:left;float:left;'><input type='hidden' id='s31" + i + "' value='" + file_names[i] + "'>" + file_names[i] + "</input></div>カテゴリ：<input type='text' name='word' id='sss3" + i + "' value=''></input><input type='button' value='追加' onclick='addCategory(" + i + ");'></input><input type='button' value='削除' onclick='deleteCategory(" + i + ");'></input><input type='button' value='更新' onclick='koshin();'></input><a href='dlPDF/" + file_names[i] + ".pdf#page=1 target='_blank''><img src='images/pdf-hiraku.png' alt='イラスト２' width=100 height=100></a><a href='dlPDF/" + file_names[i] + ".pdf.zip#page=1 target='_blank''><img src='images/pdf-DL.png' alt='イラスト3' width=100 height=100></a></div></h3><h4>カテゴリ<br>";
        if (file_names[i] in dic) {
          for (n = 0; n < dic[file_names[i]].length; n++) {
            url += "<input type='button' id='" + file_names[i] + "s2" + n + "' style='font:200pt MS ゴシック; WIDTH:150px; HEIGHT:150px' value='" + dic[file_names[i]][n] + "' onclick='pushingButton(" + n + "," + i + "," + file_names.length + ");'>";
          }
        }
        url += "</h4><br>";
      }
      target.innerHTML = url;
    }
  };
  // req.open("GET", "http://192.168.1.210:5000/getlist/", true);
  req.open("GET", "http://192.168.60.62:5000/getlist/", true);
  req.send(null);
  var file3 = "./column_list.txt";
  var url3 = "";
  var target3 = document.getElementById("output3");
  var rawFile3 = new XMLHttpRequest();
  rawFile3.open("GET", file3, false);
  rawFile3.onreadystatechange = function() {
    if (rawFile3.readyState == 4) {
      if (rawFile3.status === 200 || rawFile3.status == 0) {
        var allText3 = rawFile3.responseText;
        file_names3 = allText3.split("\n");
        for (var ii = 0; ii < file_names3.length - 1; ii++) {
          url3 += "<input type='button' id='cate" + ii + "' style='font:200pt MS ゴシック; WIDTH:150px; HEIGHT:150px' value='" + file_names3[ii] + "' onclick='cateSearch(" + ii + ");'>";
        }
      }
      target3.innerHTML = url3;
    }
  }
  rawFile3.send(null);
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
