'use strict';

function ready() {
  form_feedback()
}

function form_feedback() {
  var params = new URLSearchParams(location.search)
  var success = params.get('success')
  if (!success)
    return
  var form = document.querySelector('form[data-type="'+success+'"]')
  var msg_div = document.createElement('div')
  msg_div.textContent = form.dataset.success
  msg_div.classList = 'success hidden'
  form.appendChild(msg_div)
  requestAnimationFrame(function() { msg_div.classList.remove('hidden') })
  form.onclick = function() { msg_div.remove() }
  params.delete('success')
  history.replaceState(null, '', '?' + params + location.hash)
}

if (['interactive', 'complete'].includes(document.readyState))
  ready()
else
  document.addEventListener('DOMContentLoaded', ready)
