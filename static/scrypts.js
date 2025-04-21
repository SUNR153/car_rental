document.addEventListener("DOMContentLoaded", () => {
    const themeBtn = document.getElementById("theme-toggle");
    const body = document.body;
  
    themeBtn.addEventListener("click", () => {
      body.classList.toggle("dark");
      themeBtn.textContent = body.classList.contains("dark") ? "☀ Светлая тема" : "🌙 Тёмная тема";
    });
  
    // Анимации при прокрутке
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
        }
      });
    }, { threshold: 0.2 });
  
    cards.forEach(card => {
      card.classList.add('hidden');
      observer.observe(card);
    });
  });
  