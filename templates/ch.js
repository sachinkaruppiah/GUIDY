const API_KEY = "GOOGLE_API_KEY";

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (!userInput) return;
    
    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    document.getElementById("userInput").value = "";

    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${API_KEY}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ contents: [{ parts: [{ text: userInput }] }] })
    });

    const data = await response.json();
    const botReply = data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I didn't understand that.";
    messagesDiv.innerHTML += `<p><strong>Bot:</strong> ${botReply}</p>`;
}
