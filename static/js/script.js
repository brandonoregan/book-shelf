"use strict";

const pageTitle = document.querySelector(".pageTitle");
const bookCards = document.querySelectorAll(".bookCard");
const bookCardTitle = document.querySelectorAll(".bookCardTitle");
const bookCardText = document.querySelectorAll(".bookCardText");
const tiles = document.querySelectorAll(".projects--tile");
const btnRight = document.querySelector(".right--arrow");
const btnLeft = document.querySelector(".left--arrow");
const footerLogo = document.querySelector(".footerLogo");
const arrowContainer = document.querySelector(".arrowContainer");
const sliderSubmitButton = document.getElementById("submitButton");
const removeCardButton = document.getElementById("removeCardButton");

// This function will display or hide the associated classes depending on associated screen size.
const handleScreenResize = function () {
  const screenWidth = window.innerWidth;
  if (screenWidth < 786) {
    arrowContainer.classList.add("hidden");
    btnLeft.classList.add("hidden");
    btnRight.classList.add("hidden");
  }

  if (screenWidth > 786) {
    arrowContainer.classList.remove("hidden");
    btnLeft.classList.remove("hidden");
    btnRight.classList.remove("hidden");
  }
};

// adds animated affect to associated class
gsap.from(".pageTitle", { opacity: 0, duration: 1.3, y: -30, ease: "slow" });

footerLogo.addEventListener("click", function () {
  document.documentElement.scrollIntoView({
    top: 0,
    behavior: "smooth",
  });
});

handleScreenResize();

window.addEventListener("resize", handleScreenResize);

let currentTile = 0;
const maxTile = 4;

// Adjust associated classes x position to the left
const translateLeft = function () {
  currentTile = (currentTile + 1) % maxTile;
  tiles.forEach((tile) => {
    tile.style.transform = `translateX(-${currentTile * 100}%)`;
  });
};

// Adjust associated classes x position to the right
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
