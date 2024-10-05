function signup() {
    let forms = document.querySelectorAll('.needs-validation');
    for (let i = 0; i < forms.length; i++) {
        let form = forms[i];
        form.classList.add('was-validated')
        if (!form.checkValidity()) {
            return;
        }
    }

    let first_name = document.querySelector("#first_name").value;
    let last_name = document.querySelector("#last_name").value;
    let real_name = `${first_name} ${last_name}`;
    let email = document.querySelector("#email").value;
    let username = document.querySelector("#username").value;
    let password = document.querySelector("#password").value;

    let signup_url = "/api/user/register";
    let data = {
        real_name: real_name,
        username: username,
        email: email,
        password: password,
    };

    fetch(signup_url, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        accept: "application/json",
        body: JSON.stringify(data),
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.success) {
                alert("Sign up successful, please login");
                window.location.href = "/login";
            } else {
                alert(data.detail);
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

document.getElementById("signupButton").onclick = signup;
