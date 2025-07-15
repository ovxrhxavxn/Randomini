window.rouletteValues ||= [];
window.initialRoulette ||= [];

function renderRoulette(arr) {
    const rouletteDiv = document.getElementById("roulette-scroll");
    if (!rouletteDiv) return;
    rouletteDiv.innerHTML = '';
    arr.forEach(x => {
        const el = document.createElement("div");
        el.className = "roulette-item";
        el.textContent = x;
        rouletteDiv.appendChild(el);
    });
    // сброс скролла в начало
    const parent = rouletteDiv.parentElement;
    parent.scrollTop = 0;
}

function startRoulette() {
    const arr = window.rouletteValues;
    if (!arr.length) return;

    // Блокируем кнопки
    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    startBtn.disabled = true;
    resetBtn.disabled = true;

    const container = document.getElementById("roulette-scroll");
    const parent = container.parentElement;
    const items = container.children;
    const itemHeight = items[0].offsetHeight;

    // winner
    let winnerIdx = Math.floor(Math.random() * arr.length);

    // расстояние: несколько кругов + нужный индекс
    const spinRounds = 3;
    const targetIdx = spinRounds * arr.length + winnerIdx;
    const totalHeight = itemHeight * arr.length;

    // анимация
    let duration = 4500; // в мс, например 4 секунды
    let start = null;
    let startScroll = 0;
    let destScroll = targetIdx * itemHeight;

    // убрать подсветки/прошлый выигрыш
    for (let el of items) el.classList.remove('selected');
    document.getElementById('winner').innerText = "";

    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }

    function animateScroll(timestamp) {
        if (!start) start = timestamp;
        let elapsed = timestamp - start;
        let progress = Math.min(elapsed / duration, 1);
        let easedProgress = easeOutCubic(progress);
        let currentScroll = startScroll + (destScroll - startScroll) * easedProgress;

        parent.scrollTop = currentScroll % totalHeight;

        if (progress < 1) {
            requestAnimationFrame(animateScroll);
        } else {
            parent.scrollTop = winnerIdx * itemHeight;
            for (let el of items) el.classList.remove('selected');
            items[winnerIdx].classList.add('selected');
            setTimeout(() => {
                document.getElementById('winner').innerHTML =
                  `<div class="alert alert-primary fs-4">Выпало: <b>${arr[winnerIdx]}</b></div>`;
                arr.splice(winnerIdx, 1);
                renderRoulette(arr);
                // Разблокируем кнопки
                startBtn.disabled = false;
                resetBtn.disabled = false;
            }, 400);
        }
    }
    requestAnimationFrame(animateScroll);
}

function resetRoulette() {
    window.rouletteValues = [...window.initialRoulette];
    document.getElementById('winner').innerHTML = "";
    renderRoulette(window.rouletteValues);

    // Разблокировать кнопки
    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    if(startBtn) startBtn.disabled = false;
    if(resetBtn) resetBtn.disabled = false;
}