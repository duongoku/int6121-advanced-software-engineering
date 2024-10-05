function toMyProfile() {
    window.location.href = "/profile/?id=me";
}

document.addEventListener("DOMContentLoaded", async function () {
    let url_bearer = "/api/profile/me";
    let response = await fetch(url_bearer, {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    })
    let data = await response.json();
    localStorage.setItem("userId", data.UUID);
    if (data.UserAvatar) {
        document.querySelector("#profile-avatar").src = `data:image/png;base64,${data.UserAvatar}`;
    }
    if (data.UserRealName) {
        document.querySelector("#profile-real-name").textContent = data.UserRealName;
        document.querySelector("#profile-real-name").style.display = "block";
    }
    if (data.UserProfileRichContent) {
        document.querySelector("#profile-rich-content").textContent = data.UserProfileRichContent;
        document.querySelector("#profile-rich-content").style.display = "block";
    }
    document
        .getElementById("to-my-profile")
        .addEventListener("click", toMyProfile);
});


fetch("/api/orgs/mine", {
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
        let organizations = data;
        let organizationsContainer = document.getElementById("organizations");

        for (let i = 0; i < organizations.length; i++) {
            let orgOption = `<option value="${organizations[i].UUID}">${organizations[i].OrganizationName}</option>`;
            organizationsContainer.innerHTML += orgOption;
        }
    });

document.getElementById("submit").addEventListener("click", function () {
    orgUUID = document.getElementById("organizations").value;

    if (orgUUID == "none") {
        alert("Please select an organization to create a job description");
        return;
    }

    let jobDescription = {
        PostTitle: document.getElementById("title").value,
        PostRichContent: document.getElementById("rich-content").value,
        PostOrganization: orgUUID,
    };

    fetch("/api/post/new", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
        body: JSON.stringify(jobDescription),
    })
        .then(function (response) {
            if (response.status == 200) {
                alert("Job description created successfully");
                window.location.href = "/home";
            } else {
                alert(
                    "Something went wrong, can't create new job description!"
                );
            }
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            // window.location.href = "/home";
        })
        .catch(function (error) {
            console.log(error);
        });
});
