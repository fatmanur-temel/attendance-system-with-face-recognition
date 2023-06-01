////////////////////////
// Pasta dilim graf
///////////////////////

//renkler, grafiğimiz 5 parçadan oluşacakı için 5 rengi myColor dizisinde saklıyoruz.
var myColor = ["#34a561", "#e54d42"];
var myData = [66, 36];
var myLabel = ["Gelenler", "Gelmeyenler"];

function getTotal() {
  var myTotal = 0;
  for (var j = 0; j < myData.length; j++) {
    myTotal += (typeof myData[j] == 'number') ? myData[j] : 0;
  }
  return myTotal;
}

function plotData() {
  var canvas;
  var ctx;
  var lastend = 0;
  var myTotal = getTotal();
  var doc;
  canvas = document.getElementById("canvas");
  var x = (canvas.width) / 2;
  var y = (canvas.height) / 2;
  var r = 150;

  ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (var i = 0; i < myData.length; i++) {
    ctx.fillStyle = myColor[i];
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.arc(x, y, r, lastend, lastend + (Math.PI * 2 * (myData[i] / myTotal)), false);
    ctx.lineTo(x, y);
    ctx.fill();

    // Grafik üzerindeki ifadeler bu kısımdan sonra yaptırılacak.
    ctx.beginPath();
    var start = [];
    var end = [];
    var last = 0;
    var flip = 0;
    var textOffset = 0;
    var precentage = (myData[i] / myTotal) * 100;
    start = getPoint(x, y, r - 20, (lastend + (Math.PI * 2 * (myData[i] / myTotal)) / 2));
    end = getPoint(x, y, r + 20, (lastend + (Math.PI * 2 * (myData[i] / myTotal)) / 2));
    if (start[0] <= x) {
      flip = -1;
      textOffset = -140;
    }
    else {
      flip = 1;
      textOffset = 0;
    }
    ctx.moveTo(start[0], start[1]);
    ctx.lineTo(end[0], end[1]);
    ctx.lineTo(end[0] + 150 * flip, end[1]);
    ctx.strokeStyle = "#9a9c9e";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Etiketler ayarlanıyor
    ctx.font = "18px Arial";
    ctx.fillText(myLabel[i] + " %" + precentage.toFixed(2), end[0] + textOffset, end[1] - 3);

    // Döngü artırılıyor
    lastend += Math.PI * 2 * (myData[i] / myTotal);

  }
}
// Sihirli nokta bulunuyor.
function getPoint(c1, c2, radius, angle) {
  return [c1 + Math.cos(angle) * radius, c2 + Math.sin(angle) * radius];
}
// Çizim fonksiyonu çalıştırılıyor.
plotData();


/////////////////
// Takvim
/////////////////

var monthEl = document.querySelector(".date h1");
var daysEl = document.querySelector(".days");

var monthInx = new Date().getMonth();
var lastDay = new Date(new Date().getFullYear(), monthInx + 1, 0).getDate();
var firstDay = new Date(new Date().getFullYear(), monthInx, 1).getDay() - 1;

const months = [
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
  ];

changeMonth('current')
function changeMonth(p) {
  
  console.log(p);
  if (p == 'current') {
    monthEl.innerText = months[monthInx];

    let days = "";
    
    for (let i = firstDay; i > 0; i--) {
      days += `<div class="empty"></div>`;
    }
    
    for (let i = 1; i <= lastDay; i++) {
      if (i === new Date().getDate()) {
        days += `<div class="today"><a href="#" onclick="goToCalendarDetail(${i}, ${monthInx + 1}, ${new Date().getFullYear()})">${i}</a></div>`;
      } else {
        days += `<div><a href="#" onclick="goToCalendarDetail(${i}, ${monthInx + 1}, ${new Date().getFullYear()})">${i}</a></div>`;
      }
    }
    daysEl.innerHTML = days;
  }else if (p == 'geri') {
    monthInx = monthInx - 1;
    lastDay = new Date(new Date().getFullYear(), monthInx + 1, 0).getDate();
    firstDay = new Date(new Date().getFullYear(), monthInx, 1).getDay() - 1;

    monthEl.innerText = months[monthInx];
    
    let days = "";
    console.log(new Date(new Date().getFullYear(), monthInx, 1));
    
    for (let i = firstDay; i > 0; i--) {
      days += `<div class="empty"></div>`;
    }
    console.log(new Date(new Date().getFullYear(), monthInx + 1, 0));
    
    for (let i = 1; i <= lastDay; i++) {
      days += `<div><a href="#" onclick="goToCalendarDetail(${i}, ${monthInx + 1}, ${new Date().getFullYear()})">${i}</a></div>`;
    }
    daysEl.innerHTML = days;
  }
  else {
    monthInx = monthInx + 1;
    lastDay = new Date(new Date().getFullYear(), monthInx + 1, 0).getDate();
    firstDay = new Date(new Date().getFullYear(), monthInx , 1).getDay() - 1;

    monthEl.innerText = months[monthInx];

    let days = "";
    console.log(new Date(new Date().getFullYear(), monthInx, 1));
    for (let i = firstDay; i > 0; i--) {
      days += `<div class="empty"></div>`;
    }
    console.log(new Date(new Date().getFullYear(), monthInx + 1, 0));
    for (let i = 1; i <= lastDay; i++) {
      days += `<div><a href="#" onclick="goToCalendarDetail(${i}, ${monthInx + 1}, ${new Date().getFullYear()})">${i}</a></div>`;
    }
    daysEl.innerHTML = days;

  }
}