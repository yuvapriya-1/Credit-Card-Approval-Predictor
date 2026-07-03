document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    console.log("Analyze button clicked!"); // Check console for this

    const resultBox = document.getElementById('result');
    const formData = new FormData(this);
    const formObject = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject)
        });

        const result = await response.json();
        console.log("Server response:", result);

        resultBox.classList.remove('hidden');
        
        if (result.approved) {
            resultBox.innerHTML = `🎉 Application Approved!<br>Status: <b>${result.risk_level}</b>`;
            resultBox.className = 'result-box success-box';
        } else {
            resultBox.innerHTML = `❌ Application Rejected.<br>Status: <b>${result.risk_level}</b>`;
            resultBox.className = 'result-box danger-box';
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});