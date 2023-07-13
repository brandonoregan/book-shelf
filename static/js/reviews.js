'use strict';

const bookCards = document.querySelectorAll('.bookCard');
const bookCardTitle = document.querySelectorAll('.bookCardTitle');
const bookCardText = document.querySelectorAll('.bookCardText');


const editForm = function(title, thoughts) {
    bookCardTitle.textContent = title
    bookCardText.textContent = thoughts
}

bookCards.forEach(card => {
    card.addEventListener('click', function(){
        // card.classList.toggle('bg-dark')})
        card.setAttribute('data-bs-toggle', 'modal')})
    })
    
