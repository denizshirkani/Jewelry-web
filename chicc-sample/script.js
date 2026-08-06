const header = document.getElementById('siteHeader');
const menuButton = document.getElementById('menuButton');
const drawer = document.getElementById('mobileDrawer');
const drawerClose = document.getElementById('drawerClose');
const overlay = document.getElementById('drawerOverlay');

window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 40));

function toggleDrawer(open) {
  drawer.classList.toggle('open', open);
  overlay.classList.toggle('open', open);
  drawer.setAttribute('aria-hidden', String(!open));
  document.body.style.overflow = open ? 'hidden' : '';
}
menuButton.addEventListener('click', () => toggleDrawer(true));
drawerClose.addEventListener('click', () => toggleDrawer(false));
overlay.addEventListener('click', () => toggleDrawer(false));
drawer.querySelectorAll('a').forEach(link => link.addEventListener('click', () => toggleDrawer(false)));

document.querySelectorAll('.wishlist').forEach(button => {
  button.addEventListener('click', () => {
    button.classList.toggle('active');
    button.textContent = button.classList.contains('active') ? '♥' : '♡';
  });
});

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

document.getElementById('newsletterForm').addEventListener('submit', event => {
  event.preventDefault();
  document.getElementById('formMessage').textContent = 'Welcome to the world of CHICC.';
  event.target.reset();
});
