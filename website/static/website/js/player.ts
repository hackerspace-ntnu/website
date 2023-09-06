function drawPlayer() {
    player.update(groundHeight, widthPosition, playerHeight);
    player.draw(ctx);
}

function clickAction() {
    player.jump();
}

class Player {
    aspectRatio: number;
    x: number;
    y: number;
    width: number;
    height: number;
    currentFrame: number;
    images: HTMLImageElement[];
    updateCounter: number;
    initialY: number = 0;
    isJumping: boolean = false;
    hasDoubleJumped: boolean = false;

    constructor() {
        this.currentFrame = 0;
        this.images = [];
        this.loadImages();
        this.updateCounter = 0;
    }

    loadImages() {
        for (let i = 1; i <= 8; i++) {
            this.images.push(document.getElementById('player' + String(i)) as HTMLImageElement);
        }
        this.aspectRatio = this.images[0].width / this.images[0].height;
    }

    draw(ctx: CanvasRenderingContext2D) {
        ctx.drawImage(this.images[this.currentFrame], this.x, this.y, this.width, this.height);
    }

    update(groundHeight: number, widthPosition: number, playerHeight: number) {
        // Update the frame every second time
        this.updateCounter++;
        if (this.updateCounter % 2 == 0) {
            this.currentFrame = (this.currentFrame + 1) % this.images.length;
        }

        this.x = widthPosition - this.width / 2;
        this.height = playerHeight;
        this.width = this.height * this.aspectRatio;

        // Jumping
        if (this.isJumping) {
            const gravity = 75 * this.height;
            const initialVelocity = (this.hasDoubleJumped ? 12 : 16) * this.height; // change initial velocity for double jump
            const time = this.updateCounter / 60;
            const displacement = -initialVelocity * time + 0.5 * gravity * time ** 2;
            const newY = this.initialY + displacement;
            if (newY > groundHeight - this.height) {
                this.y = groundHeight - this.height;
                this.isJumping = false;
                this.hasDoubleJumped = false; // reset double jump
                this.initialY = 0;
            } else {
                this.y = newY;
            }
        } else {
            this.y = groundHeight - this.height;
        }
    }

    jump() {
        if (!this.isJumping) {
            this.isJumping = true;
            this.initialY = this.y;
            this.hasDoubleJumped = false; // reset double jump
            this.updateCounter = 0;
        } else if (!this.hasDoubleJumped) {
            this.hasDoubleJumped = true;
            this.initialY = this.y;
            this.updateCounter = 0;
        }
    }
}
