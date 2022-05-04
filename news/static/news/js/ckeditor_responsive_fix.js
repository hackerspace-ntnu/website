// Prevent ckeditor hard fields to allow responsive images
window.addEventListener('DOMContentLoaded', () => {
    const images = document.getElementsByClassName('card-panel')[0].getElementsByTagName("img");
    for (const image of images) {
        image.className = "responsive-img";
        image.style.height = "";
    }
});
