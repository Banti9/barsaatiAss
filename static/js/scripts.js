// static/js/script.js

async function fetchTrends() {
    const response = await fetch('/fetch_trends');
    const data = await response.json();

    const trendsList = document.getElementById('trends');
    const timestamp = new Date(data.timestamp).toLocaleString();
    const proxy = data.proxy;
    const mongodbData = JSON.stringify(data.mongodb_data, null, 2);

    trendsList.innerHTML = `
        <h3>These are the most happening topics as on ${timestamp}</h3>
        <ul>
            ${data.trends.map(trend => `<li>${trend}</li>`).join('')}
        </ul>
        <p>The IP address used for this query was ${proxy}.</p>
        <h3>Here’s a JSON extract of this record from the MongoDB:</h3>
        <pre>${mongodbData}</pre>
    `;
}

document.getElementById('fetch-button').addEventListener('click', fetchTrends);
