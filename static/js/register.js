const usernameField = document.querySelector('#username');
const invuserFeedbackField = document.querySelector('#invalid-user-feedback');
const emailField = document.querySelector('#email');
const invemailFeedbackField = document.querySelector('#invalid-email-feedback');

const passwordField = document.querySelector('#password');
const passToggle = document.querySelector('#toggleButton');

const submitButton = document.querySelector('.submit-btn');



usernameField.addEventListener("keyup", (event) => {
    // let key = event.key;console.log(key);
    const usernVal = event.
        target.value;

    if (usernVal) {
        fetch("/authentication/user-val/", {
            body: JSON.stringify({ username: usernVal }),
            method: "POST"
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("data", data);
                console.log(username);
                if (data.username_error) {
                    username.classList.add("is-invalid");
                    invuserFeedbackField.innerHTML = `<p>${data.username_error}</p>`;
                    invuserFeedbackField.style.display = "block";
                    
                    submitButton.disabled = true;

                } else {
                    username.classList.remove("is-invalid");
                    invuserFeedbackField.style.display = "none";
                    submitButton.removeAttribute("disabled");
                }
            });
    }
});

emailField.addEventListener("keyup", (event) => {
    const emailValue = event.target.value;

    if (emailValue) {
        fetch("/authentication/email-val/", {
            body: JSON.stringify({ email: emailValue }),
            method: "POST"
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("data", data);
                if (data.email_error) {
                    email.classList.add("is-invalid");
                    invemailFeedbackField.innerHTML += `<p>${data.email_error}</p>`;
                    invemailFeedbackField.style.display = "block";
                    submitButton.disabled = true;
                }
                else{
                    email.classList.remove("is-invalid");
                    invemailFeedbackField.style.display = "none";
                    submitButton.removeAttribute("disabled");
                }
            })
    }
})


passToggle.addEventListener("click", (event) => {
    if(passwordField.classList.contains("Hashed")){
        passwordField.classList.remove("Hashed");
        passwordField.classList.add("Showing");
        passToggle.textContent = "Hide";

        passwordField.type = "text";
    }
    else{
        passwordField.classList.remove("Showing");
        passwordField.classList.add("Hashed");
        passToggle.textContent = "Show";

        passwordField.type = "password";
    }
})