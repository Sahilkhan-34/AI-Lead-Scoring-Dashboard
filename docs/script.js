// frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('lead-form');
    const tableBody = document.getElementById('leads-table-body');
    const submitBtn = document.getElementById('submit-btn');
    const errorMessage = document.getElementById('error-message');
    
    // IMPORTANT: Change this to your deployed backend URL
    const API_URL = 'https://ai-lead-scoring-dashboard-4.onrender.com';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable button to prevent multiple submissions
        submitBtn.disabled = true;
        submitBtn.textContent = 'Scoring...';
        errorMessage.textContent = '';

        const leadData = {
            Email: document.getElementById('email').value,
            CreditScore: parseInt(document.getElementById('credit-score').value, 10),
            AgeGroup: document.getElementById('age-group').value,
            FamilyBackground: document.getElementById('family-background').value,
            Income: parseInt(document.getElementById('income').value, 10),
            Comments: document.getElementById('comments').value
        };
        
        try {
            const response = await fetch(`${API_URL}/score`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(leadData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An unknown error occurred.');
            }

            const result = await response.json();
            addLeadToTable(result);
            form.reset();

        } catch (error) {
            errorMessage.textContent = `Error: ${error.message}`;
            console.error('Failed to score lead:', error);
        } finally {
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Get Score';
        }
    });

    function addLeadToTable(lead) {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${lead.Email}</td>
            <td>${lead.Comments || '-'}</td>
            <td>${lead.InitialScore}</td>
            <td>${lead.RerankedScore}</td>
        `;

        tableBody.prepend(row); // Add new leads to the top
    }
});