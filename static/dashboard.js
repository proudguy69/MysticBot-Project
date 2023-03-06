const servers = document.getElementsByClassName('server')


for (server in servers) {
    servers[server].addEventListener('mouseenter', (event) => {
        console.log(event)
    })
}