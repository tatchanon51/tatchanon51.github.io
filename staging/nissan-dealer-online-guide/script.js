function scrollToHash() {
    const hash = window.location.hash;
    if (hash && hash.startsWith('#slide-')) {
      const el = document.querySelector(hash);
      if (el) {
        // Scroll so slide TOP is just below sticky toolbar
        const toolbar = document.querySelector('.toolbar');
        const toolbarH = toolbar ? toolbar.offsetHeight : 56;
        const y = el.getBoundingClientRect().top + window.pageYOffset - toolbarH;
        window.scrollTo({top: y, behavior: 'instant'});
      }
    }
  }
  window.addEventListener('load', scrollToHash);
  document.addEventListener('DOMContentLoaded', scrollToHash);
  setTimeout(scrollToHash, 100);
  setTimeout(scrollToHash, 300);
  setTimeout(scrollToHash, 800);
  setTimeout(scrollToHash, 1500);
  
  document.querySelectorAll('.toolbar-nav a').forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        const toolbar = document.querySelector('.toolbar');
        const toolbarH = toolbar ? toolbar.offsetHeight : 56;
        const y = target.getBoundingClientRect().top + window.pageYOffset - toolbarH;
        window.scrollTo({top: y, behavior: 'smooth'});
      }
    });
  });