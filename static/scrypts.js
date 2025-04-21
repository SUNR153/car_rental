document.addEventListener("DOMContentLoaded", () => {
  console.log("JS подключён и готов к работе!");

  const btns = document.querySelectorAll('.btn');
  btns.forEach(btn => {
      btn.addEventListener('click', () => {
          btn.classList.add('clicked');
          setTimeout(() => {
              btn.classList.remove('clicked');
          }, 200);
      });
  });
});
