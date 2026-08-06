// 확인 다이얼로그

function showConfirmDialog(title, message) {
  const box = document.createElement('div');
  box.className = 'dialog';
  box.innerHTML = `<h3>${title}</h3><p>${message}</p><button>확인</button>`;
  box.querySelector('button').addEventListener('click', () => box.remove());
  document.body.appendChild(box);
  return box;
}
