const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailField = document.querySelector("#emailFieldxx");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField")
const showPasswordToggle = document.querySelector(".showPasswordToggle");

usernameField.addEventListener("keyup", (e) => {
    console.log('77777',77777); // test
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    // to prevent the error message display initially
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display='none'; // to display incase username-error

    if(usernameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({username: usernameVal }),
            method: "POST",
        }).then(res=>res.json())
        .then(data=>{
            console.log("data", data);
            usernameSuccessOutput.style.display = "none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display='block'; // to display incase username-error
                feedBackArea.innerHTML = `<p>${data.username_error}<p>`;
            }
        });
    } 
});

emailField.addEventListener("keyup", (e) => {
    console.log("88888", 88888);
    
    emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if(emailVal.length > 0){
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email : emailVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data)=>{
            console.log("data", data);
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}<p>`;
            }
        });
    }
});

const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text"); // this shows the password
    }else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password"); // this hides the password
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);