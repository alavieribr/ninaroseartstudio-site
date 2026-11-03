(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
// reveal
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -40px 0px'});
$$('.rv').forEach(el=>io.observe(el));
// hero slideshow
const sl=$$('#slides img');if(sl.length>1){let i=0;setInterval(()=>{sl[i].classList.remove('on');i=(i+1)%sl.length;sl[i].classList.add('on')},4800)}
// nav, journey stitch, paintings parallax
const nav=$('#nav'),jp=$('#jpath'),jr=$('#journey'),vs=$('#villages'),ps=$$('#pstack img');
const onScroll=()=>{if(!document.body.classList.contains('p-home'))return;nav.classList.toggle('solid',scrollY>40);
 if(jp&&jr){const r=jr.getBoundingClientRect();const p=Math.min(1,Math.max(0,(innerHeight-r.top)/(r.height+innerHeight*.2)));jp.style.clipPath=`inset(0 ${100-p*100}% 0 0)`}
 if(vs&&ps.length){const t=vs.getBoundingClientRect().top;ps.forEach((im,i)=>im.style.transform=`translateY(${(t*(i+1)*.05).toFixed(1)}px)`)}};
addEventListener('scroll',onScroll,{passive:true});onScroll();
// counters
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target,to=+el.dataset.count;let t0;const st=t=>{t0??=t;const k=Math.min(1,(t-t0)/1600);el.textContent=Math.round(to*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(st)};requestAnimationFrame(st);cio.unobserve(el)}));
$$('[data-count]').forEach(el=>{el.textContent='0';cio.observe(el)});
// quotes
const qs=$$('#quotes blockquote');if(qs.length){let q=0;setInterval(()=>{qs[q].classList.remove('on');q=(q+1)%qs.length;qs[q].classList.add('on')},4400)}
// cards tap
$$('.card').forEach(c=>c.addEventListener('click',()=>c.classList.toggle('flip')));
// filters
const fl=$('#filters'),ms=$('#masonry');
if(fl&&ms)fl.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',fl).forEach(x=>x.classList.toggle('on',x===b));
 $$('figure',ms).forEach(f=>{const show=b.dataset.f==='all'||f.dataset.k===b.dataset.f;f.classList.toggle('hide',!show);if(show){f.classList.remove('in');requestAnimationFrame(()=>requestAnimationFrame(()=>f.classList.add('in')))}})});
// lightbox
const lb=$('#lb'),li=$('#lb img'),lc=$('#lb figcaption');let set=[],cur=0;
const show=i=>{cur=(i+set.length)%set.length;const a=set[cur];li.src=a.href;li.alt=a.dataset.cap||'';lc.textContent=a.dataset.cap||'';li.style.animation='none';li.offsetWidth;li.style.animation=''};
document.addEventListener('click',e=>{const a=e.target.closest('a[data-lb]');if(!a)return;e.preventDefault();set=$$('a[data-lb]').filter(x=>!x.closest('figure.hide'));show(set.indexOf(a));lb.classList.add('on');document.body.style.overflow='hidden'});
const close=()=>{lb.classList.remove('on');document.body.style.overflow=''};
$('.lb-x').onclick=close;$('.lb-p').onclick=()=>show(cur-1);$('.lb-n').onclick=()=>show(cur+1);
lb.addEventListener('click',e=>{if(e.target===lb)close()});
addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
let x0=null;lb.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)show(cur+(dx<0?1:-1));x0=null});
// close mobile menu on link
$$('.menu a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('menu-open')));
})();
