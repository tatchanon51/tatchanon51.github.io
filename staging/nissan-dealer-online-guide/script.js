// ===== Smooth Scroll to Slide Hash =====
function scrollToHash() {
  const hash = window.location.hash;
  if (hash && hash.startsWith('#slide-')) {
    const el = document.querySelector(hash);
    if (el) {
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

// ===== Toolbar Smooth Scroll =====
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

// ===== Keyboard Navigation =====
let currentSlide = 1;
const totalSlides = 40;

document.addEventListener('keydown', (e) => {
  const toolbar = document.querySelector('.toolbar');
  const toolbarH = toolbar ? toolbar.offsetHeight : 56;
  
  // Find current slide based on scroll position
  for (let i = 1; i <= totalSlides; i++) {
    const slide = document.querySelector('#slide-' + i);
    if (slide) {
      const rect = slide.getBoundingClientRect();
      if (rect.top <= toolbarH + 50 && rect.bottom > toolbarH + 100) {
        currentSlide = i;
        break;
      }
    }
  }
  
  if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
    e.preventDefault();
    if (currentSlide < totalSlides) {
      currentSlide++;
      navigateToSlide(currentSlide);
    }
  } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
    e.preventDefault();
    if (currentSlide > 1) {
      currentSlide--;
      navigateToSlide(currentSlide);
    }
  } else if (e.key === 'Home') {
    e.preventDefault();
    navigateToSlide(1);
  } else if (e.key === 'End') {
    e.preventDefault();
    navigateToSlide(totalSlides);
  }
});

function navigateToSlide(num) {
  const target = document.querySelector('#slide-' + num);
  if (target) {
    const toolbar = document.querySelector('.toolbar');
    const toolbarH = toolbar ? toolbar.offsetHeight : 56;
    const y = target.getBoundingClientRect().top + window.pageYOffset - toolbarH;
    window.scrollTo({top: y, behavior: 'smooth'});
    history.replaceState(null, null, '#slide-' + num);
  }
}

// ===== Progress Bar =====
function updateProgressBar() {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  
  let progressBar = document.querySelector('.scroll-progress');
  if (!progressBar) {
    progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = 'position: fixed; top: 56px; left: 0; height: 3px; background: linear-gradient(90deg, var(--nissan-red), #FFD54F); z-index: 99; transition: width 0.1s ease;';
    document.body.appendChild(progressBar);
  }
  progressBar.style.width = progress + '%';
}

window.addEventListener('scroll', updateProgressBar);
window.addEventListener('load', updateProgressBar);

// ===== Intersection Observer for Slide Fade-in =====
const slideObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('slide-visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.slide').forEach(slide => {
  slide.classList.add('slide-animated');
  slideObserver.observe(slide);
});