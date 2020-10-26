function loop(){
    requestAnimationFrame(loop)
    c.clearRect(0, 0, w, h)
    update()
    draw()

    for(let i = 0; i < hooks.length; i++){
        hooks[i].draw()
    }
}
loop()