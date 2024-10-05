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