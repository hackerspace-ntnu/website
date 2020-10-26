class Hook{
    constructor(x, y){
        this.pos = new Vector2(x, y)
        this.size = 10
    }
    draw(){
        c.beginPath()
        c.fillStyle = "red"
        c.arc(this.pos.x, this.pos.y, this.size, 0, Math.PI*2)
        c.fill()
        c.closePath()
    }
}

window.addEventListener("keydown", keyDownHandler)
window.addEventListener("keyup", keyUpHandler)



function keyUpHandler(e){
    //space
    if(e.keyCode == 32){
        player.attachedHook = undefined
    }
}

function keyDownHandler(e){
    //space
    if(e.keyCode == 32 && !player.attachedHook){
        player.grounded = false
        player.vel = new Vector2(0, 0)
        player.attachedHook = findClosestHook()
    }
}
let hooks = [new Hook(300, h/2), new Hook(1200, h/2)]

function findClosestHook(){
    let closestHook;
    let smallestDistance = Infinity
    for(let i = 0; i < hooks.length; i++){
        let deltaVec = hooks[i].pos.subtract(player.pos)
        let distance = deltaVec.mag()
        if (distance < smallestDistance){
            smallestDistance = distance
            closestHook = hooks[i]
        }
    }
    return closestHook
}

