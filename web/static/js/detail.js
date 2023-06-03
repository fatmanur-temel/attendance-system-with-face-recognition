//////////////////////
// table iconlarının renk değişimleri
//////////////////////
document.querySelectorAll('.table-head').forEach(function (tableHead) {
    tableHead.addEventListener('click', function () {
      // butona tıklanınca
      var upIcon = this.querySelector('.bi-caret-up-fill');
      var downIcon = this.querySelector('.bi-caret-down-fill');
      if (upIcon.style.color === 'rgb(0, 0, 0)') {
        upIcon.style.color = '#5c5c5c';
        downIcon.style.color = '#000';
      }
      else {
        upIcon.style.color = '#000';
        downIcon.style.color = '#5c5c5c';
      }
    });
  });
  
  
////////////////////////
// filtreleme işlemi
///////////////////////

// Add active class to the current button (highlight it)
const btnContainer = document.getElementById("BtnContainer");
const btns = btnContainer.getElementsByClassName("filter-btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function () {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}

filterSelection("all")
function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("item");
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) AddClass(x[i], "show");
  }
}

function AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) { element.className += " " + arr2[i]; }
  }
}

function RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}