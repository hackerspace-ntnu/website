class Platform {
    nextX: number;
    aspectRatio: number;
    x: number;
    y: number;
    width: number;
    height: number;
    image: HTMLImageElement;
    size: number;
    heightPositon: number;

    constructor(heightPosition: number, size: number, biome: string) {
        this.nextX = canvas.width;
        this.size = size;
        this.image = document.getElementById('platform' + this.size + biome) as HTMLImageElement;
        this.heightPositon = heightPosition;
    }

    draw(ctx: CanvasRenderingContext2D) {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }

    update(platformHeight: number) {
        this.height = platformHeight;
        this.width = this.height * this.size;
        this.y = platformHeight * (1.5 * this.heightPositon) + this.height;
        this.x = this.nextX;
        this.nextX = this.nextX - backgroundSpeed;
    }

    getBoundingBox(): { left: number; top: number; right: number; bottom: number } {
        return {
            left: this.x,
            top: this.y,
            right: this.x + this.width,
            bottom: this.y + this.height,
        };
    }
}
