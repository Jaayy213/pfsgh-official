/*
  PASTE THIS AT THE TOP OF YOUR ./js/about.js FILE
*/

// --- Video Modal Code ---

// This maps your click IDs to the video files
const videoMap = {
    'video1': './images/pronto.mp4',
    'video2': './images/docVid.mp4',
    'video3': './images/pronto.mp4'  // Using the same video as video1
};

// Get the modal elements
const modal = document.getElementById("videoModal");
const videoPlayer = document.getElementById("modalVideoPlayer");
// Note: We need to get the close button *after* the DOM is loaded.
// Let's move this inside the DOMContentLoaded listener.
let closeBtn; 

/**
 * This function is called when you click a video card.
 */
function playVideo(videoId) {
    const videoSrc = videoMap[videoId];
    
    if (videoSrc) {
        videoPlayer.src = videoSrc;
        modal.style.display = "block";
        videoPlayer.play();
    } else {
        console.error("Video source not found for ID:", videoId);
    }
}

/**
 * This function closes the modal.
 */
function closeModal() {
    modal.style.display = "none";
    videoPlayer.pause();
    videoPlayer.src = ""; 
}

// When the user clicks anywhere *outside* of the modal content
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// --- End of Video Modal Code ---


/* YOUR EXISTING IntersectionObserver CODE 
  (with one small addition to hook up the close button)
*/
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};
// ... (rest of your observer code) ...
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const delay = entry.target.dataset.delay || 0;
            setTimeout(() => {
                entry.target.classList.add('animate-in');
            }, delay);
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    // Your existing code
    const cards = document.querySelectorAll('.card-custom');
    const values = document.querySelectorAll('.value-item');
    cards.forEach(card => observer.observe(card));
    values.forEach(value => observer.observe(value));

    // --- ADD THIS PART ---
    // This finds the close button and makes it work.
    // We put it here to make sure the modal HTML is loaded.
    closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.onclick = closeModal;
    }
    // --- End of new part ---
});



// Intersection Observer for scroll animations
// const observerOptions = {
//     threshold: 0.1,
//     rootMargin: '0px 0px -50px 0px'
// };


// Observe all animated elements
// document.addEventListener('DOMContentLoaded', () => {
//     const cards = document.querySelectorAll('.card-custom');
//     const values = document.querySelectorAll('.value-item');

//     cards.forEach(card => observer.observe(card));
//     values.forEach(value => observer.observe(value));
// });
