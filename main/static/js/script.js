document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.querySelector('.dark_mode'); 
    const body = document.body;

    const currentTheme = localStorage.getItem('theme');
    body.classList.add(currentTheme ? currentTheme : 'light-mode');

    function updateDarkModeIcon() {
        if (darkModeToggle) {
            darkModeToggle.classList.toggle(
                'dark-mode-icon-active',
                body.classList.contains('dark-mode')
            );
        }
    }

    function updateVideos() {
        document.querySelectorAll('video[data-light][data-dark]').forEach(video => {
            const source = video.querySelector('source');
            if (!source) return;
            source.src = body.classList.contains('dark-mode') ? video.dataset.dark : video.dataset.light;
            video.load();
        });
    }

    updateDarkModeIcon();
    updateVideos();

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            if (body.classList.contains('dark-mode')) {
                body.classList.replace('dark-mode', 'light-mode');
                localStorage.setItem('theme', 'light-mode');
            } else {
                body.classList.replace('light-mode', 'dark-mode');
                localStorage.setItem('theme', 'dark-mode');
            }
            updateDarkModeIcon();
            updateVideos();
        });
    }

    const modal = document.getElementById("profileModal");
    const openBtn = document.getElementById("openProfileModal");

    if (openBtn) {
        openBtn.addEventListener("click", function (e) {
            e.preventDefault();
            if (modal.style.display === "block") {
                modal.style.display = "none";
            } else {
                modal.style.display = "block";
            }
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
    /* выбор аватара*/
    const avatarInput = document.getElementById("id_avatar");
    const avatarFileNameSpan = document.querySelector('.profile-edit-form .file-name');
    const avatarFileButton = document.querySelector('.profile-edit-form .file-button');
    
    if (avatarInput && avatarFileButton) {
        avatarFileButton.addEventListener('click', () => {
            avatarInput.click();
        });
    
        avatarInput.addEventListener('change', () => {
            if (avatarInput.files.length > 0) {
                avatarFileNameSpan.textContent = avatarInput.files[0].name;
            } else {
                avatarFileNameSpan.textContent = 'Файл не выбран';
            }
        });
    }
});

(function () {
  console.log("script.js загружен");

  function initShowMore() {
    const cards = document.querySelectorAll(".card");
    const showMoreBtn = document.getElementById("showMoreBtn");

    if (!cards.length || !showMoreBtn) return;

    let itemsToShow;
    let step;

    function setConfig() {
      if (window.innerWidth >= 1024) {
        itemsToShow = 10;
        step = 10;
      } else if (window.innerWidth >= 768) {
        itemsToShow = 6;
        step = 6;
      } else {
        itemsToShow = 4;
        step = 4;
      }
    }

    setConfig();

    function updateCards() {
      cards.forEach((card, index) => {
        if (index < itemsToShow) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });

      if (itemsToShow >= cards.length) {
        showMoreBtn.style.display = "none";
      } else {
        showMoreBtn.style.display = "block";
      }
    }

    showMoreBtn.addEventListener("click", () => {
      itemsToShow += step;
      updateCards();
    });

    window.addEventListener("resize", () => {
      const prevItemsToShow = itemsToShow;
      setConfig();
      if (itemsToShow !== prevItemsToShow) {
        updateCards();
      }
    });

    updateCards();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initShowMore);
  } else {
    initShowMore();
  }
})();


document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.getElementById("menu-button");
  const menuModal = document.getElementById("mobileMenuModal");
  const closeMenuBtn = document.getElementById("closeMobileMenu");

  function openMenu() {
    menuModal.style.display = "block";
    setTimeout(() => menuModal.classList.add("active"), 10);
  }

  function closeMenu() {
    menuModal.classList.remove("active");
    setTimeout(() => menuModal.style.display = "none", 300);
  }

  menuButton.addEventListener("click", openMenu);
  closeMenuBtn.addEventListener("click", closeMenu);
});


