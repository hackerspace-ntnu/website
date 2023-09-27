function drawPlayer() {
    player.update(widthPosition, platforms);
    player.draw(ctx);
}
function clickAction() {
    player.jump();
}
class Player {
    aspectRatio;
    x;
    y;
    width;
    height;
    currentFrame;
    images;
    updateCounter;
    initialY = 0;
    isJumping = false;
    hasDoubleJumped = false;
    walkHeight;
    constructor(walkHeight) {
        this.currentFrame = 0;
        this.images = [];
        this.loadImages();
        this.updateCounter = 0;
        this.walkHeight = walkHeight;
    }
    loadImages() {
        for (let i = 1; i <= 8; i++) {
            this.images.push(document.getElementById('player' + String(i)));
        }
        this.aspectRatio = this.images[0].width / this.images[0].height;
    }
    draw(ctx) {
        ctx.drawImage(this.images[this.currentFrame], this.x, this.y, this.width, this.height);
    }
    update(widthPosition, platforms) {
        // Update the frame every second time
        this.updateCounter++;
        if (this.updateCounter % 2 == 0) {
            this.currentFrame = (this.currentFrame + 1) % this.images.length;
        }
        console.log(this.walkHeight);
        this.x = widthPosition - this.width / 2;
        this.height = playerHeight;
        this.width = this.height * this.aspectRatio;
        // Jumping
        if (this.isJumping) {
            console.log('jumping');
            const gravity = 75 * this.height;
            const initialVelocity = (this.hasDoubleJumped ? 12 : 16) * this.height; // change initial velocity for double jump
            const time = this.updateCounter / 60;
            const displacement = -initialVelocity * time + 0.5 * gravity * time ** 2;
            const newY = this.initialY + displacement;
            if (newY > this.walkHeight) {
                this.y = this.walkHeight;
                this.isJumping = false;
                this.hasDoubleJumped = false; // reset double jump
                this.initialY = 0;
            }
            else {
                this.y = newY;
            }
        }
        else {
            this.y = this.walkHeight;
        }
        for (const platform of platforms) {
            const playerBox = {
                left: this.x,
                top: this.y + this.height - 2,
                right: this.x + this.width,
                bottom: this.y + this.height,
            };
            const platformBox = platform.getBoundingBox();
            if (playerBox.right > platformBox.left && playerBox.left < platformBox.right && playerBox.bottom > platformBox.top) {
                console.log('on platform');
                // Collision detected with the platform
                this.walkHeight = platformBox.top; // Snap player to platform top
                this.isJumping = false;
                this.hasDoubleJumped = false; // Reset double jump
                this.initialY = this.y;
            }
        }
    }
    jump() {
        if (!this.isJumping) {
            this.isJumping = true;
            this.initialY = this.y;
            this.hasDoubleJumped = false; // reset double jump
            this.updateCounter = 0;
        }
        else if (!this.hasDoubleJumped) {
            this.hasDoubleJumped = true;
            this.initialY = this.y;
            this.updateCounter = 0;
        }
    }
}
