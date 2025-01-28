const form = document.querySelector('form');
form.addEventListener('submit', (event) =>{
    event.preventDefault();
    const formData = new FormData(form);
    validateForm();

});

function validateEmail(email) {
    console.log("Validating email")
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

function validatePassword(password) {
    console.log("Validating password")
    var re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
    return re.test(password);
};

function validateForm(){
    let email = document.forms["register-form"]["email"].value;
    let password = document.forms["register-form"]["password"].value
    
    let emailBool = validateEmail(email);
    let passwordBool = validatePassword(password)

    if ( email== ""){
        alert("Email must be filled out");
        return
    }else if (emailBool == false){
        alert("Email format is incorrect");
        return

    }
    
    if(password = ""){
        alert("Password must be filled out");
        return
    }else if (passwordBool == false){
        alert("Pasword format is incorrect \n" +
            "Should contain:\n" +
            "-8 caracters minimum\n" +
            "-At least 1 special sign\n" +
            "-At least 1 capital letter");
        return
    }

    sendBackendData(email,password)
}

function sendBackendData(email,password){
    console.log(email)
    console.log(password)

    const url = "http://127.0.0.1:8000/"
    const data = {
        email : email,
        password : password
    }

    fetch(url, 
        {method: "POST",
         headers : {
            "Content-Type" : "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if(!response.ok){
                throw new Error('HTTP error! status: $(response.status');
            }
            return response.json();
        })
        .then((responseData) => {
            console.log("Server response:", responseData);
        })

        .catch((error) => {
            console.error("Error sending credentials: ", error);
        });
}
