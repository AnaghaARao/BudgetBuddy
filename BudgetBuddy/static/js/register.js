const usernameField = document.querySelector("#usernameField");

usernameField.addEventListener("keyup", (e) => {
    console.log('77777',77777);

    const usernameVal = e.target.value;

    // console.log('usernameVal', usernameVal); -> testing


    if(usernameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:{username: usernameVal},
            method: "POST",
        }).then(res=>res.json())
        .then(data=>{
            console.log("data", data);
        });
    }

    
});