async function fetchTopCoins() {
    try {
        const response = await fetch('backend/update.json');
        const data = await response.json();

        const list = document.getElementById('coin-list');
        list.innerHTML = '';

        data.top5.forEach(coin => {
            const li = document.createElement('li');
            li.textContent = `${coin.rank}. ${coin.name} (${coin.symbol}) - Score: ${coin.score}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading coins:", error);
    }
}

fetchTopCoins();
setInterval(fetchTopCoins, 60 * 60 * 1000); // Refresh hourly
