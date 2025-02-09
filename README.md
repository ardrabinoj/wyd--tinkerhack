<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Home</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
        }
        header {
            display: flex;
            justify-content: space-between;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .profile-icon {
            cursor: pointer;
            position: relative;
        }
        .profile-menu {
            position: absolute;
            right: 10px;
            top: 50px;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            padding: 10px;
            display: none;
        }
        .profile-menu.show {
            display: block;
        }
        .profile-menu p {
            margin: 5px 0;
        }
        .profile-menu button {
            background-color: red;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
        }
        .post-box textarea, .chat-box textarea {
            width: 80%;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #ddd;
            resize: none;
        }
        .post-box button, .chat-box button {
            background-color: white;
            border: 2px solid #ddd;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .post-box button:active, .chat-box button:active {
            transform: scale(0.9);
        }
        .posts {
            margin-top: 20px;
            text-align: left;
            padding: 10px;
        }
        .post {
            background: white;
            padding: 10px;
            border-radius: 8px;
            margin: 10px auto;
            width: 60%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .chat-box {
            display: none;
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: white;
            width: 300px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 10px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Hi there..</h1>
        <div class="profile-icon" onclick="toggleProfileMenu()">👤</div>
        <div id="profile-menu" class="profile-menu">
            <p>Username: JohnDoe</p>
            <button onclick="logout()">Log Out</button>
        </div>
    </header>
    
    <main>
        <div class="post-box">
            <textarea id="post-text" placeholder="Share your thoughts..."></textarea>
            <button onclick="postMessage()">Send</button>
        </div>
        
        <div class="posts" id="posts"></div>
        
        <div class="contacts">
            <h2>Contacts</h2>
            <div class="contact-item">
                <span>Contact 1</span>
                <button onclick="openChat('Contact 1')">Chat</button>
            </div>
            <div class="contact-item">
                <span>Contact 2</span>
                <button onclick="openChat('Contact 2')">Chat</button>
            </div>
        </div>
    </main>
    
    <div id="chat-box" class="chat-box">
        <h3 id="chat-title">Chat</h3>
        <div id="chat-messages"></div>
        <textarea id="chat-input" placeholder="Type a message..."></textarea>
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        function toggleProfileMenu() {
            document.getElementById("profile-menu").classList.toggle("show");
        }
        function logout() {
            window.location.href = '/login';
        }
        function postMessage() {
            let text = document.getElementById("post-text").value;
            if (text.trim() !== "") {
                let postContainer = document.getElementById("posts");
                let newPost = document.createElement("div");
                newPost.className = "post";
                newPost.innerText = text;
                postContainer.prepend(newPost);
                document.getElementById("post-text").value = "";
            }
        }
        let chatContact = "";
        function openChat(contactName) {
            document.getElementById("chat-box").style.display = "block";
            document.getElementById("chat-title").innerText = "Chat with " + contactName;
            chatContact = contactName;
            document.getElementById("chat-messages").innerHTML = "";
        }
        function sendMessage() {
            let input = document.getElementById("chat-input");
            let message = input.value.trim();
            if (message !== "") {
                let chatMessages = document.getElementById("chat-messages");
                let msgDiv = document.createElement("div");
                msgDiv.className = "message";
                msgDiv.innerText = "You: " + message;
                chatMessages.appendChild(msgDiv);
                input.value = "";
            }
        }
    </script>
</body>
</html>
