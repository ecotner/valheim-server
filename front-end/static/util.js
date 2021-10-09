async function sha512(str) {
  const buf = await crypto.subtle.digest("SHA-512", new TextEncoder("utf-8").encode(str));
  return Array.prototype.map.call(new Uint8Array(buf), x=>(('00'+x.toString(16)).slice(-2))).join('');
}

function getInfo() {
    const url = "/get-info"
    const init = {method: "GET", mode: "same-origin"}
    fetch(url, init).then((response) => {
        return response.json()
    }).then((payload) => {
        let el = document.getElementById("info-output")
        // remove all preexisting child nodes
        while (el.firstChild)
            el.removeChild(el.lastChild)
        if (payload["status"] === "ok") {
            // create paragraph node
            let p1 = document.createElement("p")
            p1.innerText = JSON.stringify(payload["server_status"])
            el.appendChild(p1)
            // if external IP address is present, create link to status page
            payload = payload["server_status"]
            if (payload["external_ip"]) {
                let a = document.createElement("a")
                a.href = `http://${payload['external_ip']}:9000/status.json`
                a.innerText = "status page"
                let p2 = document.createElement("p")
                p2.append("Detected external IP address on instance, check out the Valheim server's ")
                p2.appendChild(a)
                p2.append(".")
                el.appendChild(p2)
            }
        }
        else
            el.innerText = "Something went wrong, could not get server status"
        el.style.visibility = "visible"
    })
}

function turnOn() {
    const url = "/turn-on"
    const init = {method: "GET", mode: "same-origin"}
    fetch(url, init).then((response) => {
        return response.json()
    }).then((payload) => {
        let el = document.getElementById("turn-on-output")
        if (payload["status"] === "ok")
            el.innerText = JSON.stringify(payload["response"])
        else
            el.innerText = "Something went wrong, could not get response"
        el.style.visibility = "visible"
    })
}

function turnOff() {
    const url = "/turn-off"
    const init = {method: "GET", mode: "same-origin"}
    fetch(url, init).then((response) => {
        return response.json()
    }).then((payload) => {
        let el = document.getElementById("turn-off-output")
        if (payload["status"] === "ok")
            el.innerText = JSON.stringify(payload["response"])
        else
            el.innerText = "Something went wrong, could not get response"
        el.style.visibility = "visible"
    })
}

async function callServer() {
    let password = document.getElementById("password-text").value
    let hash = await sha512(password)
    console.log(hash)
    let body = {hash: hash}
    body = new Blob([JSON.stringify(body)], {type: "application/json"})
    const url = "/start"
    const init = {method: "POST", mode: "same-origin", body: body}
    fetch(url, init)//.then((response) => {
    // }).then((payload) =>{
    // })
}