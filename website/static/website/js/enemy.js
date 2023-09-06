function drawEnemies(secondsPassed) {
    enemies.push(new Enemy());
    enemies.forEach((enemy, index) => {
        enemy.update(groundHeight, enemyHeight, true);
        if (enemy.x > canvas.width + enemy.width || enemy.x < -enemy.width) {
            enemies.splice(index, 1);
        }
        enemy.draw(ctx);
    });
}
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
    initialX;
    constructor() {
        this.initialX = canvas.width;
        this.currentFrame = 0;
        this.images = [];
        this.flipped = true;
        this.loadImages();
        this.updateCounter = 0;
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
    update(walkHeight, enemyHeight, flipped) {
        // Update the frame every second time
        this.updateCounter++;
        if (this.updateCounter % 2 == 0) {
            this.currentFrame = (this.currentFrame + 1) % this.images.length;
        }
        this.flipped = flipped;
        this.x = this.initialX;
        this.initialX -= backgroundSpeed;
        this.height = enemyHeight;
        this.width = this.height * this.aspectRatio;
        this.y = walkHeight - this.height;
    }
}
