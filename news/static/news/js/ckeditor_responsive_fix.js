// Prevent ckeditor hard fields to allow responsive images
window.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementsByClassName('card-panel')[0];
    for (const image of container.getElementsByTagName("img")) {
        image.className = "responsive-img";
        image.style.height = "";
    }
});
