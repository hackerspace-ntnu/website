// Objects and general constants
const canvas: HTMLCanvasElement = document.getElementById('gameCanvas') as HTMLCanvasElement;
const ctx: CanvasRenderingContext2D = canvas.getContext('2d')!;
const fps = 60;
const frameMinTime = (1000 / 60) * (60 / fps) - (1000 / 60) * 0.5;
const backgroundSpeed = 3;
const biomeTime = 3;
const transitionSpeed = 1;
const skyBackground = document.getElementById('skyBackground') as HTMLCanvasElement;
const desertBackground = document.getElementById('desertBackground') as HTMLCanvasElement;

// Changing variables
let backgroundMovePos = 0;
let backgroundIterations = 0;
let currentBackground = skyBackground;
let biome = 'sky';
let opacity = 100;
let transition = false;
let returnTransition = false;

// Calculate the ground height and player position
let generalHeight: number;
let groundHeight: number;
let widthPosition: number;
let platformHeight: number;
let playerHeight: number;
let enemyHeight: number;
let jumpHeight: number;

// Create a new player object
let player: Player;
const enemies: Enemy[] = [];
const platforms: Platform[] = [];
let lastSecond = -1;

let lastFrameTime = 0;
function update(time) {
    if (!player && groundHeight && playerHeight) {
        player = new Player(groundHeight - playerHeight);
    }
    if (time - lastFrameTime < frameMinTime) {
        requestAnimationFrame(update);
        return;
    }
    lastFrameTime = time;
    requestAnimationFrame(update);
    draw(time);
}
requestAnimationFrame(update);

function draw(time: number) {
    ctx.canvas.height = window.innerHeight - 64;
    ctx.canvas.width = window.innerWidth;
    drawBackground();
    drawEntities(time);
    drawPlayer();
}

// Add key press event listeners
document.addEventListener('keydown', (event: KeyboardEvent) => {
    if (event.code === 'Space') {
        event.preventDefault();
        clickAction();
    }
});

canvas.addEventListener('click', (event: MouseEvent) => {
    clickAction();
});
