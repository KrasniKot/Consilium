document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitButton').addEventListener('click', async function() {
        const questionInput = document.getElementById('question');
        const resultDiv     = document.getElementById('result');

        // Log to check if the button click is being detected
        console.log('Button clicked');

        // Show a loading message while fetching the answer
        resultDiv.style.display = 'none';
        resultDiv.textContent   = 'Fetching answer...';
        resultDiv.style.display = 'block';

        try {
            const response = await fetch('http://localhost:8085/ask', {
                method: 'POST', // Use POST method
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify({ question: questionInput.value }), // Send the question as JSON
            });

            if (!response.ok) {throw new Error('Network response was not ok');}

            const data   = await response.json(); // Parse JSON response
            const answer = data.answer || 'No answer available'; // Handle missing answers
            resultDiv.textContent = answer;

        } catch (error) {resultDiv.textContent = 'Error fetching answer: ' + error.message;}
    });
});
