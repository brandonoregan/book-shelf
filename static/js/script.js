"use strict";

const pageTitle = document.querySelector(".pageTitle");
const bookCards = document.querySelectorAll(".bookCard");
const bookCardTitle = document.querySelectorAll(".bookCardTitle");
const bookCardText = document.querySelectorAll(".bookCardText");
const tiles = document.querySelectorAll(".projects--tile");
const btnRight = document.querySelector(".right--arrow");
const btnLeft = document.querySelector(".left--arrow");
const footerLogo = document.querySelector(".footerLogo");

footerLogo.addEventListener("click", function () {
  document.documentElement.scrollIntoView({
    top: 0,
    behavior: "smooth",
  });
});

gsap.from(".pageTitle", { opacity: 0, duration: 1.3, y: -30, ease: "slow" });

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
});

btnLeft.addEventListener("click", function () {
  translateRight();
});
