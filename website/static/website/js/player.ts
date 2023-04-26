class Player {
    aspectRatio: number;
    x: number;
    y: number;
    width: number;
    height: number;
    currentFrame: number;
    images: HTMLImageElement[];
    updateCounter: number;

    constructor(groundHeight: number, widthPosition: number, playerHeight: number) {
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
            this.images.push(document.getElementById("player" + String(i)) as HTMLImageElement);
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
    this.y = groundHeight - this.height;
    this.x = widthPosition - this.width / 2;
    this.height = playerHeight;
    this.width = this.height * this.aspectRatio;
    }
}