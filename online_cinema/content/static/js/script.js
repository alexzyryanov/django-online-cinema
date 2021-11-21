let trackDistance = 1100
function position() {
    let track = document.querySelector(".slider-track")
    if (trackDistance === 3300) {
        track.style.transform = `translateX(0px)`
        trackDistance = 1100
    } else {
        track.style.transform = `translateX(-${trackDistance}px)`
        trackDistance += 1100
    }
}


let timerId = setInterval(() => {
    try {
        position()
    } catch (err) {
        clearInterval(timerId)
    }
}, 8000)


function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie != "") {
        let cookies = document.cookie.split(";")
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) == (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}


async function like(id) {
    let response = await fetch("/api/", {
      method: "POST",
      headers: {"X-CSRFToken": getCookie("csrftoken")},
      body: JSON.stringify({"type": "like", "id": id})
    })
    let data = await response.text()
    console.log(data)
    let butLike = document.querySelectorAll(".but-like")
    for (i of butLike) {
        if ((i.outerHTML).includes(`like(${id})`)) {
            i.style.width = "25px"
            i.style.background = "lime"
            i.style.transform = "rotate(180deg)"
            i.innerText = ""
        }
    }
}


async function likeDel(id) {
    let response = await fetch("/api/", {
      method: "POST",
      headers: {"X-CSRFToken": getCookie("csrftoken")},
      body: JSON.stringify({"type": "like_del", "id": id})
    })
    let data = await response.text()
    console.log(data)
    let divItem = document.querySelectorAll(".item")
    for (i of divItem) {
        if ((i.outerHTML).includes(`likeDel(${id})`)) {
            i.style.transition = "0.5s"
            i.style.transform = "scale(0)"
            setTimeout(() => {
                i.remove()
            }, 500);
            break
        }
    }
}
