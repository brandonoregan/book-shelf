"use strict";

const bookCards = document.querySelectorAll(".bookCard");
const bookCardTitle = document.querySelectorAll(".bookCardTitle");
const bookCardText = document.querySelectorAll(".bookCardText");
const tiles = document.querySelectorAll(".projects--tile");
const btnRight = document.querySelector(".right--arrow");
const btnLeft = document.querySelector(".left--arrow");

// const editForm = function (title, thoughts) {
//   bookCardTitle.textContent = title;
//   bookCardText.textContent = thoughts;
// };

// bookCards.forEach((card) => {
//   card.addEventListener("click", function () {
//     // card.classList.toggle('bg-dark')})
//     card.setAttribute("data-bs-toggle", "modal");
//   });
// });

let currentTile = 0;
const maxTile = 4;

const translateLeft = function () {
  currentTile = (currentTile + 1) % maxTile;
  tiles.forEach((tile) => {
    tile.style.transform = `translateX(-${currentTile * 100}%)`;
  });
};

const translateRight = function () {
  currentTile = (currentTile - 1 + maxTile) % maxTile;
  const translation = `-${currentTile * 100}%`;
  tiles.forEach((tile) => {
    tile.style.transform = `translateX(${translation})`;
  });
};

btnRight.addEventListener("click", function () {
  translateLeft();
  console.log("CLicked");
});

btnLeft.addEventListener("click", function () {
  translateRight();
  console.log("CLicked");
});
