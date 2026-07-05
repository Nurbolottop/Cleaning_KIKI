// Конфиг PurgeCSS для bundle.css (используется scripts/build_css_bundle.py / вручную)
// npx purgecss --config scripts/purgecss.config.js
module.exports = {
  content: [
    'app/templates/**/*.html',
    'app/core/static/assets/js/**/*.js',
  ],
  css: ['app/core/static/assets/css/bundle.css'],
  output: 'app/core/static/assets/css/',
  // Динамические классы, которые добавляются JS-плагинами на лету
  safelist: {
    standard: ['active', 'active-tab', 'open', 'show', 'hide', 'visible', 'expanded',
               'isActive', 'loaded', 'checked', 'disabled', 'selected', 'current',
               'stricked-menu', 'stricky-fixed', 'main-menu', 'scroll-to-top'],
    greedy: [
      /^swiper/, /^owl/, /^mfp/, /^nice-select/, /^odometer/, /^aos/, /^animated/,
      /^fade/, /^slideIn/, /^slideOut/, /^zoomIn/, /^bounce/, /^wow/, /^twentytwenty/,
      /^marquee/, /^float-bob/, /^img-bounce/, /^tabs?-/, /^dropdown/, /^mobile-nav/,
      /^xs-/, /^js-/, /^icon-/, /^fa/, /^flaticon/, /^sub-menu/, /^menu-/, /^list-/,
      /^close-/, /^section-title/, /^custom-cursor/, /^loader/, /^slider/, /^select2/,
      /^ui-/, /^tns-/, /^lg-/, /^error/, /^alert/, /^was-validated/, /^invalid/, /^valid/,
    ],
  },
  fontFace: false,
  keyframes: false,
  variables: false,
};
