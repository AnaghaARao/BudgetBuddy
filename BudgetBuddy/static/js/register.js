const usernameField = document.querySelector("#usernameField");
const feedBackField = document.querySelector(".invalid-feedback");

usernameField.addEventListener("keyup", (e) => {
    console.log('77777',77777);

    const usernameVal = e.target.value;
    // console.log('usernameVal', usernameVal); -> testing
    if(usernameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({username: usernameVal }),
            method: "POST",
        }).then(res=>res.json())
        .then(data=>{
            console.log("data", data);
            if(data.username_error){
                usernameField.classList.add("is-invalid");
            }
        });
    } 
});