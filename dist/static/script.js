'use strict';

function ready() {
  deploy_button()
  form_feedback()
}

function deploy_button() {
  if (!/test/.test(location.hostname))
    return
  var deploy_div = document.createElement('div')
  deploy_div.classList.add('deploy')
  deploy_div.innerHTML = '<button>Publiser!</button>'
  var pub = deploy_div.firstElementChild
  pub.onclick = function() {
    fetch('/cgi-bin/staging-to-prod.py', {method: 'POST'}).then(function(r) {
      if (r.ok)
        pub.remove()
    })
  }
  document.body.appendChild(deploy_div)
}

function form_feedback() {
  var p = take_param('success')
  if (!p.value)
    return
  var form = document.querySelector('form[data-type="'+p.value+'"]')
  if (!form)
    return
  var msg_div = document.createElement('div')
  msg_div.textContent = form.dataset.success
  msg_div.classList = 'success hidden'
  form.appendChild(msg_div)
  requestAnimationFrame(function() { msg_div.classList.remove('hidden') })
  setTimeout(function() {
    form.scrollIntoView({
      behaviour: 'smooth',
      block: 'center',
      inline: 'center',
    })
  }, 500)
  form.onclick = function() { msg_div.remove() }
  history.replaceState(null, '', p.search + location.hash)
}

function take_param(key) {
  var params = new Map(location.search.slice(1).split('&')
      .map(function(p) { return p.split(/=(.*)/) }))
  var value = params.get(key)
  params.delete(key)
  var search = Array.from(params.entries()).map(
      function(v){ return v[0]+'='+v[1] }).join('&')
  return {search: search ? '?' + search : '', value: value}
}


if (['interactive', 'complete'].includes(document.readyState))
  ready()
else
  document.addEventListener('DOMContentLoaded', ready)
