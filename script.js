async function fetchTopCoins() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/neonorainc/cryptobuytoday/main/backend/update.json');
        const data = await response.json();

        const list = document.getElementById('coin-list');
        list.innerHTML = '';

        data.top5.forEach((coin, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. ${coin.name} (${coin.symbol}) - Score: ${coin.score}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading coins:", error);
    }
}

fetchTopCoins();
setInterval(fetchTopCoins, 60 * 60 * 1000);
