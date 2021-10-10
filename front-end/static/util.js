VALHEIM_PORT = "2456"
VALHEIM_APP_ID = "892970"
async function sha512(str) {
  const buf = await crypto.subtle.digest("SHA-512", new TextEncoder("utf-8").encode(str));
  return Array.prototype.map.call(new Uint8Array(buf), x=>(('00'+x.toString(16)).slice(-2))).join('');
}

function makeJsonBody(body) {
    body = new Blob([JSON.stringify(body)], {type: "application/json"})
    return body
}

function getInfo() {
    let password = document.getElementById("password-text").value
    sha512(password).then((hash) => {
        let body = makeJsonBody({hash: hash})
        const url = "/get-info"
        const init = {method: "POST", mode: "same-origin", body: body}
        fetch(url, init).then((response) => {
            return response.json()
        }).then((payload) => {
            if (!payload["password_correct"]) {
                alert("Password is not correct!")
                return
            }
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
                // and link to open valheim client and connect to server via
                // steam protocol
                payload = payload["server_status"]
                if (payload["external_ip"]) {
                    // status page link
                    let a = document.createElement("a")
                    a.href = `http://${payload['external_ip']}:9000/status.json`
                    a.innerText = "status page"
                    let p2 = document.createElement("p")
                    p2.append("Detected external IP address on instance, check out the Valheim server's ")
                    p2.appendChild(a)
                    p2.append(".")
                    el.appendChild(p2)
                    // steam protocol link
                    let p3 = document.createElement("p")
                    p3.append("When server is ready, click ")
                    a = document.createElement("a")
                    a.href = `steam://run/${VALHEIM_APP_ID}/en/+connect ${payload['external_ip']}:${VALHEIM_PORT}`
                    a.innerText = "this link"
                    p3.appendChild(a)
                    p3.append(" to open Valheim and connect to the server. You may have to authorize steam to run Valheim with command line arguments.")
                    el.appendChild(p3)
                }
            }
            else
                el.innerText = "Something went wrong, could not get server status"
            el.style.visibility = "visible"
        })
    })
}

function turnOn() {
    let password = document.getElementById("password-text").value
    sha512(password).then((hash) => {
        let body = makeJsonBody({hash: hash})
        const url = "/turn-on"
        const init = {method: "POST", mode: "same-origin", body: body}
        fetch(url, init).then((response) => {
            return response.json()
        }).then((payload) => {
            if (!payload["password_correct"]) {
                alert("Password incorrect!")
                return
            }
            let el = document.getElementById("turn-on-output")
            if (payload["status"] === "ok")
                el.innerText = JSON.stringify(payload["response"])
            else
                el.innerText = "Something went wrong, could not get response"
            el.style.visibility = "visible"
        })
    })
}

function turnOff() {
    let password = document.getElementById("password-text").value
    sha512(password).then((hash) => {
        let body = makeJsonBody({hash: hash})
        const url = "/turn-off"
        const init = {method: "POST", mode: "same-origin", body: body}
        fetch(url, init).then((response) => {
            return response.json()
        }).then((payload) => {
            if (!payload["password_correct"]) {
                alert("Password incorrect!")
                return
            }
            let el = document.getElementById("turn-off-output")
            if (payload["status"] === "ok")
                el.innerText = JSON.stringify(payload["response"])
            else
                el.innerText = "Something went wrong, could not get response"
            el.style.visibility = "visible"
        })
    })
}
