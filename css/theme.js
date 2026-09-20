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

  function updateToggleButtons(theme) {
    const buttons = document.querySelectorAll('.theme-toggle-btn');
    const effective = getEffectiveTheme();
    const isAuto = (theme === 'auto');

    buttons.forEach(btn => {
      if (isAuto) {
        btn.innerHTML = effective === 'dark' ? '💻 <span>Téma: Auto (Tmavá)</span>' : '💻 <span>Téma: Auto (Svetlá)</span>';
        btn.title = 'Téma podľa prehliadača (kliknite pre zmenu)';
      } else if (theme === 'dark') {
        btn.innerHTML = '🌙 <span>Téma: Tmavá</span>';
        btn.title = 'Tmavá téma nastavená (kliknite pre zmenu)';
      } else {
        btn.innerHTML = '☀️ <span>Téma: Svetlá</span>';
        btn.title = 'Svetlá téma nastavená (kliknite pre zmenu)';
      }
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
    getEffectiveTheme: getEffectiveTheme
  };
})();
