async function check_token() {
    if (localStorage.getItem("accessToken") == null) {
        window.location.href = "/login";
    }

    let response = await fetch("/api/auth/check_token", {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    });

    if (response.status == 200) {
        return;
    } else {
        localStorage.removeItem("accessToken");
        window.location.href = "/login";
    }
}

check_token();

document.getElementById("logout").addEventListener("click", function () {
    localStorage.removeItem("accessToken");
    window.location.href = "/login";
});

document.querySelector("#searchInput").addEventListener("keyup", async function (event) {
    let query = event.target.value;
    if (query == "") {
        document.querySelector("#searchResults").innerHTML = "";
        return;
    }
    let response = await fetch(`/api/profile/search?query=${encodeURIComponent(query)}&limit=1000`, {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    })
    try {
        let data = await response.json();
        let searchResultsElement = document.querySelector("#searchResults");
        searchResultsElement.innerHTML = "";
        for (let i = 0; i < data.length; i++) {
            let user = data[i];
            let searchResultElement = document.createElement("a");
            searchResultElement.classList.add("list-group-item", "list-group-item-action");
            searchResultElement.href = `/profile/?id=${user.UUID}`;
            searchResultElement.innerHTML = `
                <div class="row user-info-row p-2">
                    <div class="col">${user.UserRealName}</div>
                    <div class="col">${user.UserEmail}</div>
                    <div class="col">${user.UserProfileEducation}</div>
                    <div class="col">${user.UserProfileExperience}</div>
                </div>
            `;
            searchResultsElement.appendChild(searchResultElement);
        }
    } catch (error) {
        console.log(error);
    }
});

const params = new URLSearchParams(window.location.search);
const userId = params.get("id");

// IDK What this does lmao
document.addEventListener("click", function (event) {
    if (event.target.matches("i.del")) {
        event.target.parentNode.remove();
    }
});

const imageUploadButton = document.querySelector("#change-avatar");
const imageUploadPreview = document.querySelector("#avatar");
const imageUploadPreviewContext = imageUploadPreview.getContext("2d");

function updateImageSource(canvasElement, newSrc) {
    const ctx = canvasElement.getContext('2d');
    const image = new Image();
    image.onload = function () {
        ctx.clearRect(0, 0, ctx.width, ctx.height);
        ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, canvasElement.width, canvasElement.height);
    }
    image.src = newSrc;
    canvasElement.style.display = 'block';
}

imageUploadButton.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function (e) {
                updateImageSource(imageUploadPreview, e.target.result);
            }
            reader.readAsDataURL(file);
        } else {
            imageUploadPreview.display = 'none';
            alert('Please select an image file.');
            return;
        }
    } else {
        imageUploadPreview.display = 'none';
    }
});


function transferDataToHtml(data) {
    let fullNameUnderAvatarField = document.getElementById("user-full-name-under-avatar");
    fullNameUnderAvatarField.innerHTML = data.UserRealName;

    let fullNameField = document.getElementById("user-full-name");
    fullNameField.value = data.UserRealName;

    let emailField = document.getElementById("email");
    emailField.value = data.UserEmail;

    let phoneField = document.getElementById("phone");
    phoneField.value = data.UserPhoneNumber;

    let educationField = document.getElementById("education");
    educationField.value = data.UserProfileEducation;

    if (data.UserAvatar) {
        updateImageSource(imageUploadPreview, `data:image/png;base64,${data.UserAvatar}`);
    }

    let aboutMeField = document.getElementById("about-me");
    aboutMeField.innerHTML = data.UserProfileRichContent;

    let experienceField = document.getElementById("experiences");
    experienceField.innerHTML = data.UserProfileExperience;
}

let url_bearer = "/api/profile/me";
fetch(url_bearer, {
    method: "GET",
    mode: "cors",
    headers: {
        "Content-Type": "application/json",
        Authorization: `bearer ${localStorage.getItem("accessToken")}`,
    },
})
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        console.log(data);
        transferDataToHtml(data);
    })
    .catch(function (error) {
        console.log(error);
    });


document.getElementById("button-save").addEventListener("click", function () {
    let forms = document.querySelectorAll('.needs-validation');
    for (let i = 0; i < forms.length; i++) {
        let form = forms[i];
        form.classList.add('was-validated')
        if (!form.checkValidity()) {
            return;
        }
    }

    new_profile = {
        UserRealName: document.getElementById("user-full-name").value,
        UserEmail: document.getElementById("email").value,
        UserAvatar: imageUploadPreview.toDataURL("image/jpeg").split("base64,")[1].slice(0, -2),
        UserPhoneNumber: document.getElementById("phone").value,
        UserProfileRichContent: document.getElementById("about-me").value,
        UserProfileEducation: document.getElementById("education").value,
        UserProfileExperience: document.getElementById("experiences").value,
    };

    console.log(new_profile);

    fetch("/api/profile/me", {
        method: "PUT",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
        accept: "application/json",
        body: JSON.stringify(new_profile),
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            window.location.href = "/profile/?id=me";
        })
        .catch(function (error) {
            console.log(error);
        });
});
