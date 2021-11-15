let track = document.querySelector(".slider-track")


let x = 1100
function position() {
    if (x === 3300) {
        track.style.transform = `translateX(0px)`
        x = 1100
    } else {
        track.style.transform = `translateX(-${x}px)`
    x += 1100
    }
}


setInterval(() => {
    position()
}, 8000)
