
const P=window.CHICC_PRODUCTS||{};
const qs=s=>document.querySelector(s), qsa=s=>[...document.querySelectorAll(s)];
const modal=qs('#enquiryModal'), pieceField=qs('#pieceField');
function openEnquiry(name='General CHICC enquiry'){if(pieceField)pieceField.value=name;modal?.classList.add('open');document.body.classList.add('locked')}
function closeEnquiry(){modal?.classList.remove('open');document.body.classList.remove('locked')}
qsa('[data-enquire]').forEach(b=>b.onclick=()=>openEnquiry());
qsa('[data-close]').forEach(b=>b.onclick=closeEnquiry);
qs('#enquiryForm')?.addEventListener('submit',e=>{e.preventDefault();qs('#success').textContent='Thank you. CHICC client service will contact you shortly.'});
qsa('.wish').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();b.classList.toggle('on');b.textContent=b.classList.contains('on')?'♥':'♡'});
const menu=qs('#menuBtn'),drawer=qs('#drawer'),overlay=qs('#overlay'); if(menu){menu.onclick=()=>{drawer.classList.add('open');overlay.classList.add('open')};overlay.onclick=()=>{drawer.classList.remove('open');overlay.classList.remove('open')}}

function card(p){
return `<article class="product-card" data-id="${p.id}"><button class="wish">♡</button><a href="product.html?id=${p.id}"><div class="product-image"><img src="assets/${p.image}" alt="${p.name}"></div><div class="meta"><span class="collection">${p.collection}</span><h3>${p.name}</h3><p>${p.material}</p><span class="enquire-link">Discover piece</span></div></a></article>`
}
function bindWishes(){qsa('.wish').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();b.classList.toggle('on');b.textContent=b.classList.contains('on')?'♥':'♡'})}
const grid=qs('#categoryGrid');
if(grid){
 const params=new URLSearchParams(location.search), cat=params.get('c')||'Rings';
 qs('#categoryTitle').textContent=cat; document.title=`CHICC — ${cat}`;
 const intros={Rings:'Symbols of love, strength and timeless elegance.',Necklaces:'Precious stones designed to shine close to your heart.',Earrings:'From delicate diamonds to statement creations.',Bracelets:'Refined lines of diamonds, gemstones and polished gold.'};
 qs('#categoryIntro').textContent=intros[cat]||'Discover exceptional creations.';
 const items=Object.values(P).filter(p=>p.category===cat);
 grid.innerHTML=items.map(card).join(''); bindWishes();
 qsa('.category-nav a').forEach(a=>{if(a.textContent===cat)a.classList.add('active')});
}
const detailName=qs('#detailName');
if(detailName){
 const id=new URLSearchParams(location.search).get('id'), p=P[id]||Object.values(P)[0];
 detailName.textContent=p.name; qs('#detailCollection').textContent=p.collection; qs('#detailMaterial').textContent=p.material; qs('#detailDescription').textContent=p.description; qs('#detailImage').src=`assets/${p.image}`; qs('#detailImage').alt=p.name; document.title=`CHICC — ${p.name}`;
 qs('#detailEnquire').onclick=()=>openEnquiry(p.name);
 const related=Object.values(P).filter(x=>x.category===p.category&&x.id!==p.id).slice(0,4);
 qs('#relatedGrid').innerHTML=related.map(card).join(''); bindWishes();
}
