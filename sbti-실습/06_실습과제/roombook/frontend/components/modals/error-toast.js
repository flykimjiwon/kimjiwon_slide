// 오류 토스트

function showErrorToast(message, ms = 3000) {
  const el = document.createElement('div');
  el.className = 'toast toast-error';
  el.textContent = message;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), ms);
}

// 구버전 호환용으로 남겨둔 함수 — 현재 아무 데서도 호출하지 않는다
function showLegacyToast(message) {
  window.alert('[roombook] ' + message);
}
