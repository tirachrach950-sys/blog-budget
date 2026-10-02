(function() {
  // Smooth scroll for every in-page link (nav + TOC)
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }
    });
  });

  // Signup form: submit via fetch so the page never navigates to a broken URL,
  // and the person always sees a clear result.
  var form = document.getElementById('signupForm');
  var note = document.getElementById('signup-note');
  if (!form) return;
  var defaultNote = note ? note.textContent : '';

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var btn = form.querySelector('button');
    var action = form.getAttribute('action') || '';

    if (action.indexOf('YOUR_FORM_ID') !== -1) {
      if (note) {
        note.textContent = 'Signup isn\'t connected yet — add your Formspree form ID in the code to activate it.';
        note.style.color = 'var(--rust)';
      }
      return;
    }

    btn.disabled = true;
    var originalLabel = btn.textContent;
    btn.textContent = 'Sending...';

    fetch(action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function(res) {
      if (res.ok) {
        if (note) { note.textContent = 'You\'re in — check your inbox for the template.'; note.style.color = 'var(--teal-deep)'; }
        form.reset();
      } else {
        if (note) { note.textContent = 'Something went wrong — please try again.'; note.style.color = 'var(--rust)'; }
      }
    }).catch(function() {
      if (note) { note.textContent = 'Network error — please try again.'; note.style.color = 'var(--rust)'; }
    }).finally(function() {
      btn.disabled = false;
      btn.textContent = originalLabel;
    });
  });
})();
(function() {
  var stage = document.querySelector('.tilt-stage');
  var obj = document.getElementById('tiltObject');
  if (!stage || !obj) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isTouch = window.matchMedia('(hover: none)').matches;
  if (reduce || isTouch) return;

  stage.addEventListener('mousemove', function(e) {
    var r = stage.getBoundingClientRect();
    var px = (e.clientX - r.left) / r.width;
    var py = (e.clientY - r.top) / r.height;
    var rotY = (px - 0.5) * 20;
    var rotX = (0.5 - py) * 14 + 6;
    obj.style.transform = 'rotateX(' + rotX + 'deg) rotateY(' + rotY + 'deg)';
  });
  stage.addEventListener('mouseleave', function() {
    obj.style.transform = 'rotateX(10deg) rotateY(-8deg)';
  });
})();
(function () {
  var b = document.getElementById('motionToggle');
  if (!b) return;
  b.addEventListener('click', function () {
    var on = document.body.classList.toggle('motion-on');
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.querySelector('span').textContent = on ? 'Lire / Read' : 'Motion';
  });
})();
