// Objects and general constants
const canvas: HTMLCanvasElement = document.getElementById("gameCanvas") as HTMLCanvasElement;
const ctx: CanvasRenderingContext2D = canvas.getContext("2d")!;
const fps = 60;
const frameMinTime = (1000 / 60) * (60 / fps) - (1000 / 60) * 0.5;
const backgroundSpeed = 3;
const biomeTime = 3;
const skyBackground = document.getElementById("skyBackground") as HTMLCanvasElement;
const desertBackground = document.getElementById("desertBackground") as HTMLCanvasElement;

// Changing variables
let backgroundMovePos = 0;
let backgroundIterations = 0;
let currentBackground = skyBackground;
let opacity = 1.0;
let transition = false;

// Calculate the ground height and player position
let groundHeight: number;
let widthPosition: number;
let playerHeight: number;

// Create a new player object
const player = new Player(groundHeight, widthPosition, playerHeight);

// Add event listener to handle user input for moving the player
const keyPressed: { [key: string]: boolean } = {};
document.addEventListener("keydown", event => {
    keyPressed[event.code] = true;
});
document.addEventListener("keyup", event => {
    keyPressed[event.code] = false;
});

let lastFrameTime = 0;
function update(time) {
    if (time - lastFrameTime < frameMinTime) {
        requestAnimationFrame(update);
        return;
    }
    lastFrameTime = time;
    requestAnimationFrame(update);
    draw()
}
requestAnimationFrame(update);

function draw() {
    ctx.canvas.height = window.innerHeight - 64;
    ctx.canvas.width = window.innerWidth;
    drawBackground();
    drawPlayer();
}

function drawPlayer() {
    player.update(groundHeight, widthPosition, playerHeight);
    player.draw(ctx);
}

function drawBackground() {
    // Calculate the background positions and sizes
    const backgroundAspectRatio = currentBackground.width / currentBackground.height;
    const canvasAspectRatio = canvas.width / canvas.height;
    const calculatedBackgroundWidth = backgroundAspectRatio / canvasAspectRatio * canvas.width;
    const startBackgroundPos = (canvas.width - calculatedBackgroundWidth) / 2;
    const secondBackgroundPos = startBackgroundPos + calculatedBackgroundWidth - 0.75; // 0.75 Removes white line between images
    const thirdBackgroundPos = startBackgroundPos + 2 * (calculatedBackgroundWidth - 0.75);
    const preBackgroundPos = startBackgroundPos - calculatedBackgroundWidth + 0.75;

    // Calculate the ground height and player position
    groundHeight = canvas.height - calculatedBackgroundWidth / backgroundAspectRatio * 0.25;
    widthPosition = canvas.width / 3;
    playerHeight = calculatedBackgroundWidth / backgroundAspectRatio * 0.2;

    backgroundMovePos += backgroundSpeed;
    if (backgroundMovePos >= calculatedBackgroundWidth) {
        backgroundMovePos = 0;
        backgroundIterations++;
    }

    if (backgroundIterations == biomeTime) {
        if (currentBackground == skyBackground) {
            currentBackground = desertBackground;
        } else {
            currentBackground = skyBackground;
        }
        backgroundIterations = 0;
        transition = true;
    }

    if (transition) {
        if (opacity > 0) {
            opacity -= 0.1;
        } else {
            transition = false;
            opacity = 1.0;
        }
    }

    ctx.globalAlpha = opacity;
    ctx.drawImage(currentBackground, startBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(currentBackground, secondBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(currentBackground, thirdBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(currentBackground, preBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
}