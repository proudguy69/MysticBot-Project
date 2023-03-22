document.querySelector("#dashboard-module-container").addEventListener("click", e => {
    const enableBtn = e.target.closest("button.enable-button");
    if(!enableBtn) return;
    const container = enableBtn.closest(".dashboard-module");
    container.classList.toggle('module-enabled')
    container.firstElementChild.firstElementChild.firstElementChild.classList.toggle('switcher-enabled')
  }, {passive: true});


//add a dm message for the welcome module

function removedm(e) {
  const label = e.target.parentElement
  const textarea = label.nextElementSibling
  textarea.remove()
  label.remove()
  //rename all the other elements
  const form = document.querySelector('#welcome-form')
  let num = 0
  for (i=0; i < form.children.length; i++) {
    if (form.children[i].nodeName == 'LABEL') {
      num++
      form.children[i].innerText = `Dm Message #${num} | `
      const span = document.createElement('span')
      span.innerHTML = '- Remove'
      span.id = "WelcomeDmRemove"
      span.classList.add('module-button-red')
      form.children[i].insertAdjacentElement('beforeend', span)
      span.addEventListener('click', removedm)
    }
    if (form.children[i].nodeName == 'BR') {
      break
    }
  }
}

document.querySelector('#WelcomeDmRemove').addEventListener('click', removedm)


function WelcomeDmAdd() {
  //first, get the number of dm messages there is
  const form = document.querySelector('#welcome-form')
  let amt = 0
  let last;
  for (i=0; i < form.children.length; i++) {
    if (form.children[i].nodeName == 'BR') {
      amt = amt/2
      last = form.children[i-1]
      break
    }
    amt++
  }
  let num = amt+1
  //create label
  const label = document.createElement('label')
  label.for = `dmmsg${num}`
  label.innerHTML = `Dm Message #${num} | `
  const span = document.createElement('span')
  span.innerHTML = '- Remove'
  span.id = "WelcomeDmRemove"
  span.classList.add('module-button-red')
  const textarea = document.createElement('textarea')
  textarea.name = `dmmsg${num}`
  textarea.rows = 2
  textarea.classList.add('form-textarea')
  if (!last) {
    last = form
    console.log("YES")
    last.insertAdjacentElement('afterbegin', label)
  } else {
    last.insertAdjacentElement('afterend', label)
  }
  label.insertAdjacentElement('beforeend', span)
  label.insertAdjacentElement('afterend', textarea)

  span.addEventListener('click', removedm)
}

