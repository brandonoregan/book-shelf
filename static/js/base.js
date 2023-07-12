"use strict";

const pageTitle = document.querySelector('.pageTitle');

pageTitle.addEventListener('click', function() {
    pageTitle.classList.toggle('bg-dark')
})

gsap.from(".pageTitle", { opacity: 0, duration: 1.3, y: -30, ease: "slow" });


