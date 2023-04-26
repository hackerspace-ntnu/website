class Player {
    aspectRatio;
    x;
    y;
    width;
    height;
    currentFrame;
    images;
    updateCounter;
    constructor(groundHeight, widthPosition, playerHeight) {
        this.x = widthPosition;
        this.y = groundHeight;
        this.currentFrame = 0;
        this.images = [];
        this.loadImages();
        this.height = playerHeight;
        this.width = this.height * this.aspectRatio;
        this.updateCounter = 0;
    }
    loadImages() {
        for (let i = 1; i <= 8; i++) {
            this.images.push(document.getElementById("player" + String(i)));
        }
        this.aspectRatio = this.images[0].width / this.images[0].height;
    }
    draw(ctx) {
        ctx.drawImage(this.images[this.currentFrame], this.x, this.y, this.width, this.height);
    }
    update(groundHeight, widthPosition, playerHeight) {
        // Update the frame every second time
        this.updateCounter++;
        if (this.updateCounter % 2 == 0) {
            this.currentFrame = (this.currentFrame + 1) % this.images.length;
        }
        this.y = groundHeight - this.height;
        this.x = widthPosition - this.width / 2;
        this.height = playerHeight;
        this.width = this.height * this.aspectRatio;
    }
}
