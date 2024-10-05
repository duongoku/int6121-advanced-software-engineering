function login() {
    let forms = document.querySelectorAll('.needs-validation');
    for (let i = 0; i < forms.length; i++) {
        let form = forms[i];
        form.classList.add('was-validated')
        if (!form.checkValidity()) {
            return;
        }
    }

    let username = document.querySelector("#username").value;
    let password = document.querySelector("#password").value;
    let login_url = "/api/user/login";
    let data = {
        username: username,
        password: password,
    };

    let formBody = [];

    for (let property in data) {
        let encodedKey = encodeURIComponent(property);
        let encodedValue = encodeURIComponent(data[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    fetch(login_url, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        accept: "application/json",
        body: formBody,
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.access_token !== undefined) {
                document.querySelector("#login-notification").style.display = "none";
                localStorage.setItem("accessToken", data.access_token);
                window.location.href = "/home";
            } else {
                document.querySelector("#login-notification").style.display = "block";
                document.querySelector("#login-notification").innerHTML = `*${data.detail}`;
            }
        })
        .catch(function (error) {
            console.log(error);
        });

    // url_bearer = "/api/profile/me";
    // fetch(url_bearer, {
    //     method: "GET",
    //     mode: "cors",
    //     headers: {
    //         "Content-Type": "application/json",
    //         Authorization: `bearer ${localStorage.getItem("accessToken")}`,
    //     },
    // })
    //     .then(function (response) {
    //         return response.json();
    //     })
    //     .then(function (data) {
    //         console.log(data);
    //         localStorage.setItem("userId", JSON.stringify(data.UUID));
    //     })
    //     .catch(function (error) {
    //         console.log(error);
    //     });
}

document.querySelector("#loginButton").onclick = login;
document.querySelector("#login-notification").style.display = "none";

if (localStorage.getItem("accessToken") !== null) {
    window.location.href = "/home";
}