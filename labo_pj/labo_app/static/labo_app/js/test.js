function hamburger(){
    const hamburger = document.querySelector('.hamburger');
    const icon = document.querySelector('.icon');
    const sm = document.querySelector('.sm');
  
    hamburger.addEventListener('click',function(){
        icon.classList.toggle('active');
        sm.classList.toggle('open');
    });
  }
  
hamburger();