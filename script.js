const menuButton=document.getElementById('menuButton'),drawer=document.getElementById('mobileDrawer'),drawerClose=document.getElementById('drawerClose'),overlay=document.getElementById('drawerOverlay'),modal=document.getElementById('enquiryModal'),pieceField=document.getElementById('pieceField');
function toggleDrawer(open){drawer.classList.toggle('open',open);overlay.classList.toggle('open',open);document.body.style.overflow=open?'hidden':''}
if(menuButton){menuButton.onclick=()=>toggleDrawer(true);drawerClose.onclick=()=>toggleDrawer(false);overlay.onclick=()=>toggleDrawer(false);drawer.querySelectorAll('a').forEach(a=>a.onclick=()=>toggleDrawer(false))}
document.querySelectorAll('.wishlist').forEach(b=>b.onclick=()=>{b.classList.toggle('active');b.textContent=b.classList.contains('active')?'♥':'♡'});
function openEnquiry(product='General CHICC enquiry'){pieceField.value=product;modal.classList.add('open');document.body.classList.add('modal-open')}
function closeEnquiry(){modal.classList.remove('open');document.body.classList.remove('modal-open')}
document.querySelectorAll('[data-open-enquiry]').forEach(b=>b.onclick=e=>openEnquiry(e.target.closest('.product-card')?.dataset.product||'General CHICC enquiry'));
document.querySelectorAll('[data-close-enquiry]').forEach(b=>b.onclick=closeEnquiry);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeEnquiry();toggleDrawer(false)}});
document.getElementById('enquiryForm').onsubmit=e=>{e.preventDefault();document.getElementById('formMessage').textContent='Thank you. Our client service will contact you shortly.'};