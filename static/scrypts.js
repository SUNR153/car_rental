
// const posts = document.querySelectorAll(".post");

// posts.forEach((post) => {
//     const img = post.querySelector(".post-image");
//     const prevBtn = post.querySelector(".prev-btn");
//     const nextBtn = post.querySelector(".next-btn");
//     const imageData = post.querySelector(".image-data");

//     if (!img || !prevBtn || !nextBtn || !imageData) return;

//     let images = JSON.parse(imageData.dataset.images);

//     if (images.length <= 1) {
//         prevBtn.style.display = 'none'; 
//         nextBtn.style.display = 'none';
//         return;
//     }

//     let currentIndex = 0;

//     function updateImage() {
//         img.src = images[currentIndex];
//     }

//     prevBtn.addEventListener("click", function () {
//         currentIndex = (currentIndex - 1 + images.length) % images.length;
//         updateImage();
//     });

//     nextBtn.addEventListener("click", function () {
//         currentIndex = (currentIndex + 1) % images.length;
//         updateImage();
//     });
// });


// function show_files(target){
//     const selectedFiles = document.getElementById('selected-files');
//     const files = target.files;
//     selectedFiles.innerHTML = '';

//     for(const file of files){
//         const fileName = file.name;
//         const fileItem = document.createElement('p');
//         fileItem.textContent = fileName;
//         selectedFiles.appendChild(fileItem);
//     }
// }

// document.querySelector("form").addEventListener("submit", function (e) {
//     e.preventDefault();
//     alert("Спасибо! Ваша заявка отправлена 🚗");
//   });
  
  