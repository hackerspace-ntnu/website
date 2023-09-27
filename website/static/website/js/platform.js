class Platform {
    nextX;
    aspectRatio;
    x;
    y;
    width;
    height;
    image;
    size;
    heightPositon;
    constructor(heightPosition, size, biome) {
        this.nextX = canvas.width;
        this.size = size;
        this.image = document.getElementById('platform' + this.size + biome);
        this.heightPositon = heightPosition;
    }
    draw(ctx) {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }
    update(platformHeight) {
        this.height = platformHeight;
        this.width = this.height * this.size;
        this.y = platformHeight * (1.5 * this.heightPositon) + this.height;
        this.x = this.nextX;
        this.nextX = this.nextX - backgroundSpeed;
    }
    getBoundingBox() {
        return {
            left: this.x,
            top: this.y,
            right: this.x + this.width,
            bottom: this.y + this.height,
        };
    }
}
