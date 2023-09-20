class Enemy {
    aspectRatio;
    x;
    y;
    width;
    height;
    currentFrame;
    images;
    flipped;
    updateCounter;
    nextX;
    target;
    x1;
    x2;
    constructor() {
        this.nextX = canvas.width;
        this.currentFrame = 0;
        this.images = [];
        this.flipped = true;
        this.loadImages();
        this.updateCounter = 0;
        this.target = true;
        this.x1 = canvas.width - 800;
        this.x2 = canvas.width - 500;
    }
    loadImages() {
        for (let i = 1; i <= 8; i++) {
            this.images.push(document.getElementById('enemy' + String(i)));
        }
        this.aspectRatio = this.images[0].width / this.images[0].height;
    }
    draw(ctx) {
        if (this.flipped) {
            ctx.save();
            ctx.scale(-1, 1); // Flips horizontally
            ctx.drawImage(this.images[this.currentFrame], -this.x - this.width, this.y, this.width, this.height);
            ctx.restore();
        }
        else {
            ctx.drawImage(this.images[this.currentFrame], this.x, this.y, this.width, this.height);
        }
    }
    moveBetween(movementSpeed) {
        if (this.nextX < this.x1) {
            this.target = false;
        }
        else if (this.nextX > this.x2) {
            this.target = true;
        }
        if (this.target == true) {
            this.update(groundHeight, true, -movementSpeed);
        }
        else {
            this.update(groundHeight, false, movementSpeed);
        }
    }
    update(walkHeight, flipped, movementSpeed) {
        // Update the frame every second time
        this.updateCounter++;
        if (this.updateCounter % 2 == 0) {
            this.currentFrame = (this.currentFrame + 1) % this.images.length;
        }
        this.flipped = flipped;
        this.x = this.nextX;
        this.nextX = this.nextX - backgroundSpeed + movementSpeed;
        this.height = enemyHeight;
        this.width = this.height * this.aspectRatio;
        this.y = walkHeight - this.height;
        this.x1 -= 1;
        this.x2 -= 1;
    }
}
