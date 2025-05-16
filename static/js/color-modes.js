/*!
 * Переключатель цветового режима для документации Bootstrap (https://getbootstrap.com/)
 * Авторские права 2011-2023 Авторы Bootstrap
 * Лицензия Creative Commons Attribution 3.0 Unported License.
 */

(() => {
  «использовать строго»

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  константа getPreferredTheme = () => {
    const сохраненнаяТема = getStoredTheme()
    если (хранимаяТема) {
      возврат сохраненногоТема
    }

    return window.matchMedia('(prefers-color-scheme: dark)').соответствует ? 'dark' : 'light'
  }

  константа setTheme = тема => {
    если (тема === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark')
    } еще {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  установитьТему(getPreferredTheme())

  const showActiveTheme = (тема, фокус = ложь) => {
    const themeSwitcher = document.querySelector('#bd-theme')

    если (!themeSwitcher) {
      возвращаться
    }

    const themeSwitcherText = document.querySelector('#bd-theme-text')
    const activeThemeIcon = document.querySelector('.theme-icon-active use')
    const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
    const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')

    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      элемент.classList.remove('активный')
      элемент.setAttribute('aria-pressed', 'false')
    })

    btnToActive.classList.add('активный')
    btnToActive.setAttribute('aria-pressed', 'true')
    activeThemeIcon.setAttribute('href', svgOfActiveBtn)
    const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`
    themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)

    если (фокус) {
      themeSwitcher.фокус()
    }
  }

  window.matchMedia('(предпочитает-цветовую-схему: темную)').addEventListener('изменение', () => {
    const сохраненнаяТема = getStoredTheme()
    если (storedTheme !== 'светлый' && storedTheme !== 'темный') {
      установитьТему(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    показатьАктивнуюТему(getPreferredTheme())

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(переключение => {
        toggle.addEventListener('click', () => {
          константа тема = toggle.getAttribute('data-bs-theme-value')
          setStoredTheme(тема)
          setTheme(тема)
          showActiveTheme(тема, правда)
        })
      })
  })
})()