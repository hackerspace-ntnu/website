function drawBackground() {
    // Calculate the background positions and sizes
    const backgroundAspectRatio = currentBackground.width / currentBackground.height;
    const canvasAspectRatio = canvas.width / canvas.height;
    const calculatedBackgroundWidth = (backgroundAspectRatio / canvasAspectRatio) * canvas.width;
    const startBackgroundPos = (canvas.width - calculatedBackgroundWidth) / 2;
    const secondBackgroundPos = startBackgroundPos + calculatedBackgroundWidth - 0.75; // 0.75 Removes white line between images
    const thirdBackgroundPos = startBackgroundPos + 2 * (calculatedBackgroundWidth - 0.75);
    const preBackgroundPos = startBackgroundPos - calculatedBackgroundWidth + 0.75;

    // Calculate the ground height and player position
    groundHeight = canvas.height - (calculatedBackgroundWidth / backgroundAspectRatio) * 0.25;
    widthPosition = canvas.width / 3;
    generalHeight = calculatedBackgroundWidth / backgroundAspectRatio;
    platformHeight = (calculatedBackgroundWidth / backgroundAspectRatio) * 0.1;
    playerHeight = (calculatedBackgroundWidth / backgroundAspectRatio) * 0.2;
    enemyHeight = (calculatedBackgroundWidth / backgroundAspectRatio) * 0.15;
    jumpHeight = (calculatedBackgroundWidth / backgroundAspectRatio) * 0.5;

    backgroundMovePos += backgroundSpeed;
    if (backgroundMovePos >= calculatedBackgroundWidth) {
        backgroundMovePos = 0;
        backgroundIterations++;
    }

    if (backgroundIterations == biomeTime) {
        backgroundIterations = 0;
        transition = true;
    }

    if (transition) {
        if (opacity > 0 && returnTransition == false) {
            opacity -= transitionSpeed;
        } else if (opacity < 100 && returnTransition == false) {
            if (currentBackground == skyBackground) {
                currentBackground = desertBackground;
                biome = 'desert';
            } else {
                currentBackground = skyBackground;
                biome = 'sky';
            }
            returnTransition = true;
        } else if (opacity < 100 && returnTransition == true) {
            opacity += transitionSpeed;
        } else if (opacity == 100 && returnTransition == true) {
            transition = false;
            returnTransition = false;
        }
    }

    ctx.globalAlpha = opacity / 100;
    ctx.drawImage(currentBackground, startBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height);
    ctx.drawImage(currentBackground, secondBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height);
    ctx.drawImage(currentBackground, thirdBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height);
    ctx.drawImage(currentBackground, preBackgroundPos - backgroundMovePos, 0, calculatedBackgroundWidth, canvas.height);
    ctx.globalAlpha = 1;
}
