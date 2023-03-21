document.querySelector("#dashboard-module-container").addEventListener("click", e => {
    const enableBtn = e.target.closest("button.enable-button");
    if(!enableBtn) return;
    const container = enableBtn.closest(".dashboard-module");
    container.classList.toggle('module-enabled')
    container.firstElementChild.firstElementChild.firstElementChild.classList.toggle('switcher-enabled')
  }, {passive: true});


function welcomeSave() {
  const switcher = document.querySelector('div.button-switcher')
  let enabled = false
  let dmMsg;
  let channelMsg;
  let channel;

  if (switcher.classList.contains('switcher-enabled')) {
    enabled = true
  } else {
    enabled = false
  }

  dmMsg = document.querySelector('#dmmsg').value
  channel = document.querySelector('#welcchanneldropdown').value
  channelMsg = document.querySelector('.channelinput').value
  if (!dmMsg) {dmMsg = null}
  if (!channel) {channel = null}
  if (!channelMsg) {channelMsg = null}
  const form = {
    "enabled": enabled,
    "dmMessage": dmMsg,
    "channel": channel,
    "channelMsg": channelMsg
  }
  const data = JSON.stringify(form)
  fetch(window.location.href, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
  },
    body: data
  })
}