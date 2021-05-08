const refreshBtn = document.getElementsByClassName('refresh-btn')[0];

refreshBtn.addEventListener('click', refreshPage);

function refreshPage(){
    location.reload();
}