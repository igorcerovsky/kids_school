/**
 * Kubi Theme Controller
 * Detects browser theme (prefers-color-scheme) with optional manual override
 */
(function() {
  const STORAGE_KEY = 'kubi-theme-pref';

  function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY) || 'auto';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    updateToggleButtons(theme);
  }

  function getEffectiveTheme() {
    const saved = getSavedTheme();
    if (saved === 'dark' || saved === 'light') return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function cycleTheme() {
    const current = getSavedTheme();
    let next;
    if (current === 'auto') {
      next = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
    } else if (current === 'dark') {
      next = 'light';
    } else {
      next = 'auto';
    }
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  }

  const THEME_I18N = {
    en: {
      autoDark: '💻 <span>Theme: Auto (Dark)</span>',
      autoLight: '💻 <span>Theme: Auto (Light)</span>',
      autoTitle: 'Theme based on browser preference (click to cycle)',
      dark: '🌙 <span>Theme: Dark</span>',
      darkTitle: 'Dark theme set (click to cycle)',
      light: '☀️ <span>Theme: Light</span>',
      lightTitle: 'Light theme set (click to cycle)',
      backLink: '← All Activities'
    },
    sk: {
      autoDark: '💻 <span>Téma: Auto (Tmavá)</span>',
      autoLight: '💻 <span>Téma: Auto (Svetlá)</span>',
      autoTitle: 'Téma podľa prehliadača (kliknite pre zmenu)',
      dark: '🌙 <span>Téma: Tmavá</span>',
      darkTitle: 'Tmavá téma nastavená (kliknite pre zmenu)',
      light: '☀️ <span>Téma: Svetlá</span>',
      lightTitle: 'Svetlá téma nastavená (kliknite pre zmenu)',
      backLink: '← Prehľad aktivít'
    },
    de: {
      autoDark: '💻 <span>Design: Auto (Dunkel)</span>',
      autoLight: '💻 <span>Design: Auto (Hell)</span>',
      autoTitle: 'Design nach Systemeinstellung (klicken zum Wechseln)',
      dark: '🌙 <span>Design: Dunkel</span>',
      darkTitle: 'Dunkles Design gewählt (klicken zum Wechseln)',
      light: '☀️ <span>Design: Hell</span>',
      lightTitle: 'Helles Design gewählt (klicken zum Wechseln)',
      backLink: '← Zur Übersicht'
    }
  };

  function getEffectiveLang() {
    return localStorage.getItem('kubi_lang') || document.documentElement.lang || 'en';
  }

  function updateToggleButtons(theme) {
    const buttons = document.querySelectorAll('.theme-toggle-btn');
    const effective = getEffectiveTheme();
    const isAuto = (theme === 'auto');
    const lang = getEffectiveLang();
    const t = THEME_I18N[lang] || THEME_I18N.en;

    buttons.forEach(btn => {
      if (isAuto) {
        btn.innerHTML = effective === 'dark' ? t.autoDark : t.autoLight;
        btn.title = t.autoTitle;
      } else if (theme === 'dark') {
        btn.innerHTML = t.dark;
        btn.title = t.darkTitle;
      } else {
        btn.innerHTML = t.light;
        btn.title = t.lightTitle;
      }
    });

    // Update standard back navigation links if present
    document.querySelectorAll('.kubi-back-link').forEach(link => {
      if (link.dataset.customI18n) return;
      link.textContent = t.backLink;
    });
  }

  // Initial apply
  applyTheme(getSavedTheme());

  // Listen for browser preference changes when in 'auto' mode
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (getSavedTheme() === 'auto') {
      applyTheme('auto');
    }
  });

  // Attach click handler once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    updateToggleButtons(getSavedTheme());
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.addEventListener('click', cycleTheme);
    });
  });

  // Export helper
  window.KubiTheme = {
    cycle: cycleTheme,
    apply: applyTheme,
    update: function() { updateToggleButtons(getSavedTheme()); },
    getEffectiveTheme: getEffectiveTheme
  };
})();
