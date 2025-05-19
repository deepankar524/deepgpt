document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat-form');
    const userInput = document.getElementById('user_input');
    const chatBox = document.getElementById('chat-box');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message === '') return;

        // Display user's message
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user');
        userMessageDiv.innerHTML = `<strong>User:</strong> ${message}`;
        chatBox.appendChild(userMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear input
        userInput.value = '';

        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'user_input': message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                const botMessageDiv = document.createElement('div');
                botMessageDiv.classList.add('message', 'bot');
                botMessageDiv.innerHTML = `<strong>Bot:</strong> ${data.response}`;
                chatBox.appendChild(botMessageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
