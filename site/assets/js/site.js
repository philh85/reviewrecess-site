/* Review Recess — tiny site script: applies links from config.js and runs the mobile menu.
   Without JavaScript every placeholder button simply reads "Coming soon". */
(function () {
  var d = document, cfg = window.RR_CONFIG || {};
  d.documentElement.className += ' js';
  var EMAIL = /^[^\s@<>"']+@[^\s@<>"']+\.[a-z]{2,}$/i;
  function value(key) {
    var v = String(cfg[key] || '').trim();
    if (!v) return '';
    if (key === 'CONTACT_EMAIL') return EMAIL.test(v) ? v : '';
    return /^https:\/\/[^\s"'<>]+$/i.test(v) ? v : '';
  }
  function ready(fn) { if (d.readyState !== 'loading') fn(); else d.addEventListener('DOMContentLoaded', fn); }
  ready(function () {
    // Buttons/links: <a data-link="KEY" aria-disabled="true">Label<span class="soon">Coming soon</span></a>
    Array.prototype.forEach.call(d.querySelectorAll('[data-link]'), function (el) {
      var key = el.getAttribute('data-link'), v = value(key);
      if (!v) { el.removeAttribute('href'); el.setAttribute('aria-disabled', 'true'); return; }
      var soon = el.querySelector('.soon'); if (soon) soon.parentNode.removeChild(soon);
      el.removeAttribute('aria-disabled');
      if (key === 'CONTACT_EMAIL') { el.href = 'mailto:' + v; }
      else { el.href = v; el.target = '_blank'; el.rel = 'noopener noreferrer'; }
    });
    // Plain text slots: <span data-text="CONTACT_EMAIL">fallback text</span>
    Array.prototype.forEach.call(d.querySelectorAll('[data-text]'), function (el) {
      var v = value(el.getAttribute('data-text')); if (v) el.textContent = v;
    });
    // Mobile menu
    var btn = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
    if (btn && nav) btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
})();
