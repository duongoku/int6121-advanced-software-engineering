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

function transferDataToHtml(data) {
    let fullNameUnderAvatarField = document.getElementById("user-full-name-under-avatar");
    fullNameUnderAvatarField.innerHTML = data.UserRealName;

    let fullNameField = document.getElementById("user-full-name");
    fullNameField.innerHTML = data.UserRealName;

    let emailField = document.getElementById("email");
    emailField.innerHTML = data.UserEmail;

    let phoneField = document.getElementById("phone");
    phoneField.innerHTML = data.UserPhoneNumber;

    let educationField = document.getElementById("education");
    educationField.innerHTML = data.UserProfileEducation;

    if (data.UserAvatar) {
        let avatarField = document.getElementById("avatar");
        avatarField.src = `data:image/png;base64,${data.UserAvatar}`;
    }

    let aboutMeField = document.getElementById("about-me");
    aboutMeField.innerHTML = data.UserProfileRichContent;

    let experienceField = document.getElementById("experiences");
    experienceField.innerHTML = data.UserProfileExperience;
}

document
    .getElementById("new-organization")
    .addEventListener("click", function () {
        window.location.href = "/new-organization";
    });


let url_bearer = "/api/profile/me";

if (userId != "me") {
    url_bearer = `/api/profile/profile?uuid=${userId}`;
}

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

function showOrgs(orgs) {
    let orgsField = document.getElementById("organizations");
    orgsField.innerHTML = "";

    for (let i = 0; i < orgs.length; i++) {
        let org = orgs[i];
        showOrg(org, orgsField);
    }
}

function showOrg(org, orgsField) {
    let orgField = document.createElement("div");
    orgField.className = "container-fluid";
    orgField.innerHTML = `
                <div class="row" style="padding: 10px">
                    <div class="col image-col">
                        <img src="data:image/png;base64,${org.OrganizationAvatar}">
                    </div>
                    <a class="col-md nav-item text-center" href="/organization?id=${org.UUID}"> ${org.OrganizationName} </a>
                    <div class="col-md-auto text-center my-profile-function">
                        <a class="text-center btn btn-outline-danger btn-sm" id="del_${org.UUID}">Delete organization</a>
                    </div>
                </div>
            `;
    orgsField.appendChild(orgField);

    document.getElementById(`del_${org.UUID}`).onclick = () => {
        // console.log(org.UUID);
        delOrganization(org.UUID);
    };
}

function delOrganization(orgId) {
    fetch(`/api/orgs/leave?org_uuid=${orgId}`, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            if (data.status == "success") {
                window.location.href = "/profile?id=me";
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

if (userId == "me") {
    url_getOrgs = "/api/orgs/mine";
} else {
    url_getOrgs = `/api/orgs/user?user_uuid=${userId}`;
}

fetch(url_getOrgs, {
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
        showOrgs(data);
        if (userId != "me") {
            let myProfileFunctionElements = document.querySelectorAll(".my-profile-function");
            for (let i = 0; i < myProfileFunctionElements.length; i++) {
                myProfileFunctionElements[i].style.display = "none";
            }
        }
    })
    .catch(function (error) {
        console.log(error);
    });

if (userId != "me") {
    let myProfileFunctionElements = document.querySelectorAll(".my-profile-function");
    for (let i = 0; i < myProfileFunctionElements.length; i++) {
        myProfileFunctionElements[i].style.display = "none";
    }
}

document.getElementById("button-edit").addEventListener("click", function () {
    window.location.href = "/profile/edit";
});