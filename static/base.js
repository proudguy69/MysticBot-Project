const dropdown = document.getElementById('dropdown')
const settings = document.getElementById('settings')

dropdown.addEventListener('mousedown', (e) => {
     if (dropdown.classList.contains('rotate')) {
        dropdown.classList.remove('rotate')
        settings.classList.remove('show')
        setTimeout(() => {
            settings.classList.add('hidden')
        }, 500)
        
     } else {
        dropdown.classList.add('rotate')
        settings.classList.remove('hidden')
        settings.classList.add('show')
     }
})