const canvas = document.querySelector("canvas")
const c = canvas.getContext("2d")
let w, h
function resize(e){
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    w = canvas.width
    h = canvas.height
}


//konstanter
const pull = 0.5
const g = 0.2
const gameSpeed = 3
const hookDistance = 800
resize()
window.addEventListener("resize", resize)

class Vector2{
    constructor(x, y){
        this.x = x
        this.y = y
    }

    normalized(newMag){
        let angle = Math.atan2(this.y, this.x)
        const newVector = new Vector2(Math.cos(angle), Math.sin(angle))
        if (newMag){
            newVector.scale(newMag)
        }
        return newVector
    }
    add(vec){
        this.x += vec.x
        this.y += vec.y
    }
    mag(){
        return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2))
    }
    subtract(vec){
        return new Vector2(this.x-vec.x, this.y-vec.y)
    }
    scale(skalar){
        this.x *= skalar
        this.y *= skalar
    }
}

let player = {
    grounded: true,
    pos: new Vector2(0, h-15),
    vel: new Vector2(0, 0),
    groundedVel: new Vector2(0, 0),
    attachedHook: undefined,
    closestHook: undefined

}

function update(){
    if(player.attachedHook){
        if(player.attachedHook.pos.subtract(player.pos).mag() > hookDistance) player.attachedHook = undefined
        else{
            const deltaVector = player.attachedHook.pos.subtract(player.pos)
            player.acc = deltaVector.normalized(pull) 
            player.vel.add(player.acc)
            player.vel.y += g
            player.pos.add(player.vel)
        }
    }
    else{
        if(player.grounded){
            player.pos.add(player.groundedVel)
        }
        else{
            player.vel.y += g
            player.vel.x *= 0.995
            
            player.pos.add(player.vel)

            if(player.pos.y > h-15){
                player.pos.y = h-15
                player.grounded = true
            }
        }

    }
}

function draw(){
    c.fillStyle = "black"
    c.beginPath()
    c.fillRect(player.pos.x-15, player.pos.y-15, 30, 30)
    c.closePath()

    if(player.attachedHook){
        c.beginPath()
        c.strokeStyle = "black"
        c.moveTo(player.pos.x, player.pos.y)
        c.lineTo(player.attachedHook.pos.x, player.attachedHook.pos.y)
        c.stroke()
        c.closePath()
    }
}




