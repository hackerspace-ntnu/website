
function loop(){
    requestAnimationFrame(loop)
    c.save()
    //translate camera
    if(player.pos.y < 0){
        c.translate(0, -player.pos.y + 30)
    }
    else if(player.pos.y > h){
        c.translate(0, h-player.pos.y - 30)
    }
    if(player.pos.x < 0){
        c.translate(-player.pos.x + 30, 0)
    }
    else if(player.pos.x > w){
        c.translate(0, w-player.pos.x - 30)
    }

    // c.clearRect(0, 0, w, h)
    c.fillStyle = "beige"
    c.rect(0, 0, w, h)
    c.fill()
    update()
    draw()

    let closest = undefined
    let smallestdist = Infinity
    for(let i = 0; i < hooks.length; i++){
        hooks[i].pos.x -= gameSpeed
        const dist = hooks[i].pos.subtract(player.pos).mag()
        if(dist < hookDistance && dist < smallestdist){
            smallestdist = dist
            closest = hooks[i]
        }
        if(hooks[i].pos.x < 0){
            hooks[i].pos.x = w
        }
        hooks[i].draw()
    }
    if(closest){
        //tegn linje til nærmeste path
        c.beginPath()
        c.save()
        c.globalAlpha = 0.9
        c.strokeStyle = "red"
        c.moveTo(player.pos.x, player.pos.y)
        c.lineTo(closest.pos.x, closest.pos.y)
        c.stroke()
        c.restore()
        c.closePath()
    }
    c.restore()
    
}
loop()