// menu-btn sınıfına sahip butona tıklandığında
document.querySelectorAll('.menu-btn').forEach(function(button) {
    button.addEventListener('click', function() {
      // butona tıklanınca, bir sonraki sub-menu öğesini kaydırarak açın/kapatın
      var subMenu = this.nextElementSibling;
      if (subMenu.style.display === 'block') {
        subMenu.style.display = 'none';
      } else {
        subMenu.style.display = 'block';
      }
      // butona tıklanınca, icon sınıfını ekleyin veya kaldırın
      var icon = this.querySelector('.icon');
      icon.classList.toggle('rotate');
    });
  });
  
  // nav ul içindeki her bir li öğesi tıklandığında
  document.querySelectorAll('nav ul li').forEach(function(li) {
    li.addEventListener('click', function() {
      // tıklanan öğeye active sınıfını ekleyin ve diğer kardeş öğelerden active sınıfını kaldırın
      this.classList.add('active');
      Array.from(this.parentNode.children).forEach(function(child) {
        if (child !== li) {
          child.classList.remove('active');
        }
      });
    });
  });
  