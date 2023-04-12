class player {
    moveX;
    moveY;
    frame;
    images;
    image;
    constructor() {
        this.moveX = 0;
        this.moveY = 0;
        this.frame = 0;
        this.images = [];
        this.loadImages();
        this.image = this.images[0];
    }
    loadImages() {
        for (let i = 1; i <= 16; i++) {
            this.images.push(document.getElementById("player" + String(i)));
        }
    }
    control(x, y) {
        this.moveX += x;
        this.moveY += y;
    }
    update() {
        if (this.moveX != 0) {
            this.frame += 1;
            if (this.frame > 7 * 4) {
                this.frame = 0;
            }
            this.image = this.images[this.frame / 4 + 8];
        }
    }
}
