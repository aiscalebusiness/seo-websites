// Mobile menu, dropdowns, scroll reveal, contact form
(function () {
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  document.querySelectorAll('.has-drop > button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.has-drop.open').forEach(function (li) {
      if (!li.contains(e.target) && window.innerWidth > 960) {
        li.classList.remove('open');
        li.querySelector('button').setAttribute('aria-expanded', 'false');
      }
    });
  });

  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -60px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // Contact form: posts to the form's action if one is set, otherwise opens the visitor's mail client.
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      var msg = form.querySelector('.form-msg');
      if (form.getAttribute('action')) return;
      e.preventDefault();
      var d = new FormData(form);
      var body = 'Name: ' + d.get('first') + ' ' + d.get('last') + '\nEmail: ' + d.get('email') +
        '\nWebsite: ' + (d.get('website') || '-') + '\n\n' + d.get('message');
      window.location.href = 'mailto:info@seowebsites.co.nz?subject=' +
        encodeURIComponent('Website enquiry from ' + d.get('first')) + '&body=' + encodeURIComponent(body);
      msg.textContent = 'Opening your email app to send the message…';
    });
  }
})();
