function loop(){
    requestAnimationFrame(loop)
    c.clearRect(0, 0, w, h)
    update()
    draw()

    for(let i = 0; i < hooks.length; i++){
        hooks[i].pos.x -= gameSpeed
        if(hooks[i].pos.x < 0){
            hooks[i].pos.x = w
        }
        hooks[i].draw()
    }
}
loop()