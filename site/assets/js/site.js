/* Review Recess — tiny site script: applies links from config.js and runs the mobile menu.
   Without JavaScript every placeholder button simply reads "Coming soon". */
(function () {
  var d = document, cfg = window.RR_CONFIG || {};
  d.documentElement.className += ' js';
  var EMAIL = /^[^\s@<>"']+@[^\s@<>"']+\.[a-z]{2,}$/i;
  function raw(key) {
    // "TPT_GAME_URLS.answer-armada" reads one entry of a per-game map in config.js
    var dot = key.indexOf('.');
    if (dot > 0) { var map = cfg[key.slice(0, dot)] || {}; return map[key.slice(dot + 1)]; }
    return cfg[key];
  }
  function value(key) {
    var v = String(raw(key) || '').trim();
    if (!v) return '';
    if (key === 'CONTACT_EMAIL') return EMAIL.test(v) ? v : '';
    return /^https:\/\/[^\s"'<>]+$/i.test(v) ? v : '';
  }
  function ready(fn) { if (d.readyState !== 'loading') fn(); else d.addEventListener('DOMContentLoaded', fn); }
  ready(function () {
    // Buttons/links: <a data-link="KEY" aria-disabled="true">Label<span class="soon">Coming soon</span></a>
    //   data-fallback="KEY2": used when KEY is blank (per-game TpT page -> store page)
    //   data-optional: the element starts hidden and is only shown when its link is set
    Array.prototype.forEach.call(d.querySelectorAll('[data-link]'), function (el) {
      var key = el.getAttribute('data-link'), v = value(key);
      if (!v && el.getAttribute('data-fallback')) v = value(el.getAttribute('data-fallback'));
      if (!v) { el.removeAttribute('href'); el.setAttribute('aria-disabled', 'true'); return; }
      if (el.hasAttribute('data-optional')) el.hidden = false;
      var soon = el.querySelector('.soon'); if (soon) soon.parentNode.removeChild(soon);
      el.removeAttribute('aria-disabled');
      if (key === 'CONTACT_EMAIL') { el.href = 'mailto:' + v; }
      else { el.href = v; el.target = '_blank'; el.rel = 'noopener noreferrer'; }
    });
    // "Free version coming soon" notes disappear once that game's free link is set
    Array.prototype.forEach.call(d.querySelectorAll('[data-free-note]'), function (el) {
      var link = el.parentNode.querySelector('[data-optional]'); if (link && !link.hidden) el.hidden = true;
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
