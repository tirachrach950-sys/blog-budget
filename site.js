/* ===== SITE SETTINGS ===== */
var CFG={
  ga4Id:'G-E9TWCC9638',      // Google Analytics (loads only after Accept)
  monetagSrc:''              // paste your Monetag script URL here (loads only after Accept)
};
(function(){
  var KEY='plainfolio-cookie-consent',d=document,loaded=false;
  function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function set(v){try{localStorage.setItem(KEY,v)}catch(e){}}
  function load(){
    if(loaded)return;loaded=true;
    if(CFG.ga4Id){window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',CFG.ga4Id);
      var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+CFG.ga4Id;d.head.appendChild(s)}
    if(CFG.monetagSrc){var m=d.createElement('script');m.async=true;m.src=CFG.monetagSrc;d.head.appendChild(m)}
  }
  function banner(){
    if(d.getElementById('cookie'))return;
    var b=d.createElement('div');b.id='cookie';b.setAttribute('role','dialog');b.setAttribute('aria-label','Cookie choice');
    b.innerHTML='<p>We use cookies for analytics and to show ads. They load only if you accept. <a href="/privacy-policy">Privacy Policy</a></p><button class="ok" type="button">Accept</button><button type="button">Decline</button>';
    var bt=b.querySelectorAll('button');
    bt[0].onclick=function(){set('accepted');b.remove();load()};
    bt[1].onclick=function(){set('declined');b.remove()};
    d.body.appendChild(b);
  }
  var c=get();if(c==='accepted')load();else if(!c)banner();
  var cs=d.getElementById('cookie-settings');if(cs)cs.onclick=banner;
  var chips=d.querySelectorAll('.chip');
  chips.forEach(function(ch){ch.onclick=function(){
    chips.forEach(function(x){x.classList.toggle('on',x===ch)});
    var f=ch.dataset.f;d.querySelectorAll('#guides .card').forEach(function(card){card.hidden=!(f==='all'||card.dataset.cat===f)})}});
})();
