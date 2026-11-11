/* Cleaning KIKI — интерактив сайта. Чистый JS, без зависимостей. */
(function () {
  'use strict';
  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (sel, ctx) { return (ctx || doc).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); };

  /* ---------- Шапка: тень при прокрутке + плавающая кнопка звонка ---------- */
  var header = $('.site-header');
  var fab = $('.fab-call');
  var onScroll = function () {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (fab) fab.classList.toggle('is-visible', y > 500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Оверлеи: мобильное меню и окно заказа ---------- */
  var lastFocus = null;
  function openLayer(el) {
    if (!el) return;
    lastFocus = doc.activeElement;
    el.classList.add('is-open');
    el.setAttribute('aria-hidden', 'false');
    doc.body.classList.add('is-locked');
    var focusable = el.querySelector('input, button, a');
    if (focusable) setTimeout(function () { focusable.focus({ preventScroll: true }); }, 350);
  }
  function closeLayer(el) {
    if (!el || !el.classList.contains('is-open')) return;
    el.classList.remove('is-open');
    el.setAttribute('aria-hidden', 'true');
    if (!$('.mnav.is-open, .drawer.is-open')) doc.body.classList.remove('is-locked');
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  var mnav = $('#mnav');
  var drawer = $('#booking');

  doc.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('[data-mnav-open]')) { e.preventDefault(); openLayer(mnav); return; }
    if (t.closest('[data-mnav-close]')) { e.preventDefault(); closeLayer(mnav); return; }
    var opener = t.closest('[data-booking-open]');
    if (opener && drawer) {
      e.preventDefault();
      closeLayer(mnav);
      var sid = opener.getAttribute('data-service');
      if (sid) {
        var radio = drawer.querySelector('input[name="service"][value="' + sid + '"]');
        if (radio) radio.checked = true;
      }
      openLayer(drawer);
      return;
    }
    if (t.closest('[data-booking-close]')) { e.preventDefault(); closeLayer(drawer); }
  });
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeLayer(drawer); closeLayer(mnav); }
  });

  /* ---------- Ползунок количества комнат ---------- */
  $$('.range input[type="range"]').forEach(function (input) {
    var out = input.closest('.range').querySelector('output');
    var update = function () {
      var min = +input.min || 0, max = +input.max || 10;
      input.style.setProperty('--fill', ((input.value - min) / (max - min) * 100) + '%');
      if (out) out.textContent = input.value;
    };
    input.addEventListener('input', update);
    update();
  });

  /* ---------- Hero-слайдер ---------- */
  var hero = $('[data-hero]');
  if (hero) {
    var slides = $$('.hero__slide', hero);
    var dots = $$('.hero__dot', hero);
    var idx = 0, timer = null;
    var loadSlide = function (s) {
      $$('source[data-srcset]', s).forEach(function (src) { src.srcset = src.getAttribute('data-srcset'); src.removeAttribute('data-srcset'); });
      $$('img[data-src]', s).forEach(function (img) { img.src = img.getAttribute('data-src'); img.removeAttribute('data-src'); });
    };
    var go = function (n) {
      if (!slides.length) return;
      idx = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) {
        var on = i === idx;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
        // догружаем фон следующего слайда только когда он нужен
        if (on) loadSlide(s);
      });
      dots.forEach(function (d, i) { d.classList.toggle('is-active', i === idx); d.setAttribute('aria-current', i === idx ? 'true' : 'false'); });
    };
    var play = function () { if (reduceMotion || slides.length < 2) return; stop(); timer = setInterval(function () { go(idx + 1); }, 6500); };
    var stop = function () { if (timer) clearInterval(timer); timer = null; };
    var prev = $('[data-hero-prev]', hero), next = $('[data-hero-next]', hero);
    if (prev) prev.addEventListener('click', function () { go(idx - 1); play(); });
    if (next) next.addEventListener('click', function () { go(idx + 1); play(); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); play(); }); });
    hero.addEventListener('mouseenter', stop);
    hero.addEventListener('mouseleave', play);
    // свайп
    var sx = null;
    hero.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) { go(idx + (dx < 0 ? 1 : -1)); play(); }
      sx = null;
    }, { passive: true });
    // предзагрузка остальных фонов после полной загрузки страницы
    window.addEventListener('load', function () {
      setTimeout(function () { slides.forEach(loadSlide); }, 1500);
    });
    play();
  }

  /* ---------- До / После ---------- */
  $$('.ba__frame').forEach(function (frame) {
    var range = $('.ba__range', frame);
    if (!range) return;
    var set = function () { frame.style.setProperty('--pos', range.value + '%'); };
    range.addEventListener('input', set);
    set();
  });

  /* ---------- Карусель отзывов ---------- */
  $$('[data-carousel]').forEach(function (wrap) {
    var track = $('.carousel__track', wrap);
    var prev = $('[data-carousel-prev]', wrap), next = $('[data-carousel-next]', wrap);
    if (!track) return;
    var step = function () { var c = track.firstElementChild; return c ? c.getBoundingClientRect().width + 24 : track.clientWidth; };
    var sync = function () {
      if (prev) prev.disabled = track.scrollLeft <= 4;
      if (next) next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    };
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* ---------- Счётчики ---------- */
  var animateCount = function (el) {
    var raw = (el.getAttribute('data-count') || '').trim();
    var target = parseInt(raw.replace(/[^\d]/g, ''), 10);
    if (!target || reduceMotion) return;
    var dur = 1600, start = null;
    var tick = function (ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(target * eased).toLocaleString('ru-RU');
      if (p < 1) requestAnimationFrame(tick); else el.textContent = raw;
    };
    el.textContent = '0';
    requestAnimationFrame(tick);
  };

  /* ---------- Появление при прокрутке ---------- */
  var revealEls = $$('[data-reveal]');
  var countEls = $$('[data-count]');
  if ('IntersectionObserver' in window) {
    // то, что уже на экране, показываем сразу — без мигания
    var vh = window.innerHeight;
    revealEls.forEach(function (el) { if (el.getBoundingClientRect().top < vh * 0.92) el.classList.add('is-in'); });
    root.classList.add('fx-ready');

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { if (!el.classList.contains('is-in')) io.observe(el); });

    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        animateCount(en.target);
        cio.unobserve(en.target);
      });
    }, { threshold: 0.6 });
    countEls.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- Тосты ---------- */
  $$('.toast').forEach(function (t, i) {
    var hide = function () { t.classList.add('is-hiding'); setTimeout(function () { t.remove(); }, 420); };
    var btn = $('button', t);
    if (btn) btn.addEventListener('click', hide);
    setTimeout(hide, 5000 + i * 600);
  });
})();
