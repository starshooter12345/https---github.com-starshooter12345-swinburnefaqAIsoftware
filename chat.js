document.getElementById('send-container').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('message-input');
    const userMessage = input.value.trim();

    if (userMessage !== '') {
        addMessage(userMessage, 'user');
        input.value = ''; // Clear input after sending

        // Send the message to the backend
        fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage("Sorry, I couldn't process your request at the moment.", 'bot');
        });
    }
});

function addMessage(text, sender) {
    const message = document.createElement('div');
    message.textContent = text;
    message.classList.add('message', sender);
    document.getElementById('chat-box').appendChild(message);
    document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
}

// Function to send a greeting message when the chatbox loads
function greetUser() {
    const greetingMessage = "Hello! How can I assist you today?";
    addMessage(greetingMessage, 'bot');
}

// Call greetUser when the window loads
window.onload = greetUser;