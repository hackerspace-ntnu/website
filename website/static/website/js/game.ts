const canvas: HTMLCanvasElement = document.getElementById("gameCanvas") as HTMLCanvasElement;;
const ctx: CanvasRenderingContext2D = canvas.getContext("2d")!;
const fps = 60;
const frameMinTime = (1000 / 60) * (60 / fps) - (1000 / 60) * 0.5;
const skyBackground = document.getElementById("skyBackground") as HTMLCanvasElement;;
const desertBackground = document.getElementById("desertBackground");
const backgroundAspectRatio = skyBackground.width / skyBackground.height;
let backgroundMovePos = 0;

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
    //drawPlayer();
}

function drawBackground() {
    const canvasAspectRatio = canvas.width / canvas.height;
    const calculatedBackgroundWidth = backgroundAspectRatio / canvasAspectRatio * canvas.width;
    const startBackgroundPos = (canvas.width - calculatedBackgroundWidth) / 2;
    const secondBackgroundPos = startBackgroundPos +  calculatedBackgroundWidth - 0.75; // 0.75 Removes white line between images
    const thirdBackgroundPos = startBackgroundPos +  2 * (calculatedBackgroundWidth - 0.75);
    const preBackgroundPos = startBackgroundPos -  calculatedBackgroundWidth + 0.75;

    backgroundMovePos += 3;
    if (backgroundMovePos >= calculatedBackgroundWidth) {
        backgroundMovePos = 0;
    }

    ctx.drawImage(skyBackground, startBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(skyBackground, secondBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(skyBackground, thirdBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
    ctx.drawImage(skyBackground, preBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height)
}