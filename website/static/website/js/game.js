// Objects and general constants
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const fps = 60;
const frameMinTime = (1000 / 60) * (60 / fps) - (1000 / 60) * 0.5;
const backgroundSpeed = 3;
const biomeTime = 3;
const transitionSpeed = 1;
const skyBackground = document.getElementById('skyBackground');
const desertBackground = document.getElementById('desertBackground');
// Changing variables
let backgroundMovePos = 0;
let backgroundIterations = 0;
let currentBackground = skyBackground;
let opacity = 100;
let transition = false;
let returnTransition = false;
// Calculate the ground height and player position
let groundHeight;
let widthPosition;
let playerHeight;
let enemyHeight;
let jumpHeight;
// Create a new player object
const player = new Player();
const enemies = [];
let lastFrameTime = 0;
function update(time) {
    if (time - lastFrameTime < frameMinTime) {
        requestAnimationFrame(update);
        return;
    }
    lastFrameTime = time;
    requestAnimationFrame(update);
    draw(Math.floor(time / 1000));
}
requestAnimationFrame(update);
function draw(secondsPassed) {
    ctx.canvas.height = window.innerHeight - 64;
    ctx.canvas.width = window.innerWidth;
    drawBackground();
    drawPlayer();
    drawEnemies(secondsPassed);
}
// Add key press event listeners
document.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
        event.preventDefault();
        clickAction();
    }
});
canvas.addEventListener('click', (event) => {
    clickAction();
});