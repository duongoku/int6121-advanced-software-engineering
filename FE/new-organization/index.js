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

// IDK What this does lmao
document.addEventListener("click", function (event) {
    if (event.target.matches("i.del")) {
        event.target.parentNode.remove();
    }
});

const imageUploadButton = document.querySelector("#img-upload-button");
const imageUploadPreview = document.querySelector("#organization-logo");
const imageUploadPreviewContext = imageUploadPreview.getContext("2d");

imageUploadButton.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const image = new Image();
                image.onload = function () {
                    imageUploadPreviewContext.clearRect(0, 0, imageUploadPreviewContext.width, imageUploadPreviewContext.height);
                    imageUploadPreviewContext.drawImage(image, 0, 0, image.width, image.height, 0, 0, imageUploadPreview.width, imageUploadPreview.height);
                }
                image.src = e.target.result;
                imageUploadPreview.style.display = 'block';
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

document
    .getElementById("post-organization")
    .addEventListener("click", function (e) {
        e.preventDefault();
        let forms = document.querySelectorAll('.needs-validation');
        for (let i = 0; i < forms.length; i++) {
            let form = forms[i];
            form.classList.add('was-validated')
            if (!form.checkValidity()) {
                return;
            }
        }

        let organizationName =
            document.getElementById("organization-name").value;
        let organizationDescription = document.getElementById(
            "organization-description"
        ).value;
        let organizationLogo = imageUploadPreview.toDataURL("image/jpeg").split("base64,")[1]
            .slice(0, -2);

        let organization = {
            OrganizationName: organizationName,
            OrganizationDescription: organizationDescription,
            OrganizationAvatar: organizationLogo,
        };

        console.log(JSON.stringify(organization));

        fetch("/api/orgs/create", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `bearer ${localStorage.getItem("accessToken")}`,
            },
            accept: "application/json",
            body: JSON.stringify(organization),
        })
            .then(function (response) {
                if (response.status === 200) {
                    return response.json();
                } else {
                    alert("Something went wrong, please try again later!");
                }
            })
            .then(function (data) {
                console.log(data);
                window.location.href = "/profile?id=me";
            })
            .catch(function (error) {
                console.log(error);
            });
    });
