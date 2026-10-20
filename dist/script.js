const toast = document.getElementById('toast');
let toastTimer;
async function shareProfile() {
  const url = window.location.href.split('#')[0];
  try {
    if (navigator.share) {
      await navigator.share({ title: document.title, url });
      return;
    }
    await navigator.clipboard.writeText(url);
    toast.textContent = '프로필 링크를 복사했습니다.';
  } catch (error) {
    if (error.name === 'AbortError') return;
    toast.textContent = '주소창에서 링크를 복사해 주세요.';
  }
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}
document.getElementById('share-button').addEventListener('click', shareProfile);
document.getElementById('closing-share').addEventListener('click', shareProfile);
