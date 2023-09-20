function drawEntities(time) {
    const seconds = Math.floor(time / 1000);
    if (seconds !== lastSecond) {
        lastSecond = seconds;
        if (lastSecond % 5 == 0) {
            enemies.push(new Enemy());
        }
        platforms.push(new Platform(Math.floor(Math.random() * 4), Math.floor(Math.random() * 4) + 1, biome));
    }
    platforms.forEach((platform, index) => {
        platform.update(platformHeight);
        removeOutOfBoundsEntity(platform, platforms, index);
        platform.draw(ctx);
    });
    enemies.forEach((enemy, index) => {
        enemy.moveBetween(6);
        removeOutOfBoundsEntity(enemy, enemies, index);
        enemy.draw(ctx);
    });
}
function removeOutOfBoundsEntity(entity, entitylist, index) {
    if (entity.x <= -canvas.width - entity.width) {
        entitylist.splice(index, 1);
    }
}
