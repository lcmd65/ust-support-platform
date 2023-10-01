setInterval(highlightAll, 1000);
// Function to highlight code using highlight.js library
function highlightAll() {
    document.querySelectorAll("pre code").forEach(block => {
        hljs.highlightBlock(block);
    });
}
const treeview = document.querySelector(".tree-view")
const chatBox = document.querySelector(".chat-box");
const messageInput = document.querySelector("#message-input");
const sendBtn = document.querySelector("#send-btn");

function addMessage(message, isUserMessage) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("mt-3", "p-3", "rounded");
    const treeItem = document.createElement("li");
    treeItem.addEventListener("click", function viewItem(event) {
        // Get the clicked `li` tag.
        const li = event.target;
        const item_view = li.getElementsByTagName('p')[0].innerHTML;
        const chatBoxElements = document.getElementById(".chat-box");
        for (const chatBoxElement of chatBoxElements) {
            const pElement = chatBoxElement.querySelector('p');
            if (pElement.textContent === item_view) {
                chatBoxElement.scrollIntoView(true);
                chatBoxElement.scrollIntoView({ smooth: true });
            }
        }
    });
    const messageInput = document.querySelector("tree-view");

    if (isUserMessage) {
        messageDiv.classList.add("user-message");
        treeItem.classList.add("tree-item")
    } else {
        messageDiv.classList.add("bot-message");
    }

    messageDiv.innerHTML = `<img src="" class="user-icon"><p>${message}</p>`;
    treeItem.innerHTML = `<imge src=""><p class="tree-item-click">${message}</p>`;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    treeview.appendChild(treeItem)
    treeview.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = messageInput.value.trim();

    if (message !== "") {
        addMessage(message, true);
        fetch("/api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                messageInput.value = "";
                const messageDiv = document.createElement("div");
                messageDiv.classList.add("mt-3", "p-3", "rounded");
                messageDiv.classList.add("bot-message");
                const content = data.content;
                // Check if the content has code block
                const hasCodeBlock = content.includes("```");
                if (hasCodeBlock) {
                    // If the content has code block, wrap it in a <pre><code> element
                    const codeContent = content.replace(/```([\s\S]+?)```/g, '</p><pre><code>$1</code></pre><p>');
                    messageDiv.innerHTML = `<img src="" class="bot-icon"><p>${codeContent}</p>`
                } else {
                    messageDiv.innerHTML = `<img src="" class="bot-icon"><p>${content}</p>`
                }
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => console.error(error));
    }
}
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", event => {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});