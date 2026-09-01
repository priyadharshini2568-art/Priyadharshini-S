document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault(); // Prevent page reload

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error-msg");

    // Example credentials
    if(username === "admin" && password === "1234") {
        window.location.href = "homepage.html"; // Redirect to homepage
    } else {
        errorMsg.textContent = "Invalid username or password!";
    }
});