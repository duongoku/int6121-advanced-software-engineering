function getTimeDescriptionFromSeconds(seconds) {
    // The format should be the same as the one on facebook: e.g. "2 hours ago", "5 minutes ago", "just now", "1 day ago", etc.
    let timeDescription = "";

    if (seconds < 60) {
        timeDescription = `${seconds} seconds ago`;
    } else if (seconds < 3600) {
        timeDescription = `${Math.floor(seconds / 60)} minutes ago`;
    } else if (seconds < 86400) {
        timeDescription = `${Math.floor(seconds / 3600)} hours ago`;
    } else if (seconds < 604800) {
        timeDescription = `${Math.floor(seconds / 86400)} days ago`;
    } else if (seconds < 2592000) {
        timeDescription = `${Math.floor(seconds / 604800)} weeks ago`;
    } else if (seconds < 31536000) {
        timeDescription = `${Math.floor(seconds / 2592000)} months ago`;
    } else {
        timeDescription = `${Math.floor(seconds / 31536000)} years ago`;
    }

    return timeDescription;
}

async function getLikeList(jobDescriptionId) {
    var like_lists = await fetch(
        `/api/interactions/like?post_uuid=${jobDescriptionId}`,
        {
            method: "GET",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `bearer ${localStorage.getItem("accessToken")}`,
            },
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            return data;
        });
    return like_lists;
}

function getCommentList(jobDescriptionId) {
    fetch(
        `/api/interactions/comment?post_uuid=${jobDescriptionId}&limit=10&offset=0`,
        {
            method: "GET",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `bearer ${localStorage.getItem("accessToken")}`,
            },
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            createCommentListContainer(data, jobDescriptionId);
        });
}

function createLikeListContainer(likeList) {
    let likeListHTML = document.createElement("div");
    likeListHTML.innerHTML += `<div> Likes: ${likeList.length}</div>`;
    for (let i = 0; i < likeList.length; i++) {
        let likeItem = document.createElement("div");
        likeItem.setAttribute("class", "container");
        likeItem.innerHTML = `
            <div class=row style="margin-bottom:10px;">
                <div class="col-md-2">
                    <img class="rounded-circle" src="data:image/png;base64,${likeList[i].LikeOwnerAvatar}" alt="John" style="width: 45px; aspect-ratio: 1;">
                </div>
                <div class="col-md-5">
                    <a class="nav-item" href="/profile/?id=${likeList[i].LikeOwner}" style="text-decoration: none;color: inherit;">
                        ${likeList[i].LikeOwnerName} 
                    </a>
                </div>
            </div>
        `;
        likeListHTML.appendChild(likeItem);
    }

    let likeModal = document.getElementById("likeListModalBody");
    likeModal.innerHTML = "";
    likeModal.appendChild(likeListHTML);
}

function createCommentListContainer(commentList, jobDescriptionId) {
    let commentListHTML = document.createElement("div");
    for (let i = 0; i < commentList.length; i++) {
        let commentItem = document.createElement("div");
        commentItem.setAttribute("class", "card");
        commentItem.setAttribute("style", "padding: 10px");
        commentItem.innerHTML = `
        <div class="card-header">
            <img src="data:image/png;base64,${commentList[i].CommentOwnerAvatar}" alt="John" style="width:5%; aspect-ratio: 1">
            &nbsp;
            <a class="nav-item" href="/profile/?id=${commentList[i].CommentOwner}" style="text-decoration: none;color: inherit;">
                ${commentList[i].CommentOwnerName} 
            </a>
        </div>

        <div class="card-body">
            <p>${commentList[i].CommentContent}</p>
        </div>
        `;
        commentListHTML.appendChild(commentItem);
    }

    let cmtContainer = document.getElementById(
        `cmt_${jobDescriptionId}_container`
    );
    cmtContainer.innerHTML = "";
    cmtContainer.appendChild(commentListHTML);

    let cmtInput = document.createElement("div");
    cmtInput.setAttribute("class", "card");
    cmtInput.innerHTML = `
        <div class="card-header">
            <div class="form-floating">
                <textarea class="form-control" placeholder="Leave a comment here" id="form_floating_${jobDescriptionId}" style="height: 100px"></textarea>
                <label for="floatingTextarea">Comment</label>
            </div>
        </div>
        
        <div class="card-footer">
            <button type="button" class="btn btn-primary" id="add_cmt_${jobDescriptionId}">Comment</button>
        </div>
    `;
    cmtContainer.appendChild(cmtInput);

    document
        .getElementById(`add_cmt_${jobDescriptionId}`)
        .addEventListener("click", () => {
            addComment(jobDescriptionId);
        });
}

async function addComment(jobDescriptionId) {
    let comment_msg = document.getElementById(
        `form_floating_${jobDescriptionId}`
    ).value;

    let comment = {
        CommentContent: comment_msg,
        PostUUID: jobDescriptionId,
    };

    fetch(`/api/interactions/comment`, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
        body: JSON.stringify(comment),
    })
        .then(function (response) {
            if (response.status != 200) {
                alert(
                    "Something went wrong, please try post your comment later"
                );
            }
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            getCommentList(jobDescriptionId);
        })
        .catch(function (error) {
            console.log(error);
        });
}

async function applyForJob(postId) {
    let response = await fetch(`/api/post/${postId}/apply`, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    });
    try {
        let data = await response.json();
        if (response.status != 200) {
            alert(data.detail);
        } else {
            alert("Application submitted successfully!");
        }
    } catch (error) {
        console.log(error);
    }
}

async function createJdContainer(jdData) {
    let jdHTML = document.createElement("div");

    jdHTML.innerHTML = `
    <div class="card shadow gedf-card mb-3">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="mr-2">
                        <img class="rounded-circle" style="width: 45px; aspect-ratio: 1;" src="data:image/png;base64,${jdData.PostOwnerAvatar
        }" alt="">
                    </div>
                    <div class="ml-2">
                        <div class="h5 m-0"> 
                            &nbsp;
                            <a class="nav-item" href="/profile/?id=${jdData.PostOwner
        }" style="text-decoration: none;color: inherit;">
                                ${jdData.PostOwnerName} 
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card-body">
            <div class="text-muted h7 mb-2"> <i class="fa fa-clock-o"></i> ${getTimeDescriptionFromSeconds(
            jdData.PostTimestamp
        )}</div>
            <h5 class="card-title">${jdData.PostTitle}</h5>

            <p class="card-text">
                ${jdData.PostRichContent}
            </p>
        </div>

        <div class="card-footer pb-0 pt-2">
            <button type="button" class="btn btn-secondary mb-2" id="like_${jdData.PostUUID
        }" data-bs-toggle="modal" data-bs-target="#likeListModal">
                <span id="like_num_${jdData.PostUUID}"> 
                    View Likes
                </span>
            </button>
            <button type="button" class="btn btn-outline-primary mb-2" id="like_action_${jdData.PostUUID
        }">
                <a class="card-link" style="text-decoration: none;">
                    <i class="fa fa-gittip"></i> <span id="like_name_${jdData.PostUUID
        }">Like</span>
                </a>
            </button>
            
            <button type="button" class="btn btn-outline-primary mb-2" id="cmt_${jdData.PostUUID
        }">
                <a class="card-link" style="text-decoration: none;">
                    <i class="fa fa-comment"></i> Comment
                </a>
            </button>

            <button type="button" class="btn btn-primary mb-2" id="apply_${jdData.PostUUID
        }">
                Apply for job
            </button>
            <button type="button" class="btn btn-info mb-2" id="view_applicants_${jdData.PostUUID
        }" data-bs-toggle="modal" data-bs-target="#applicantListModal" ${jdData.PostOwner == localStorage.getItem("userId") ? '' : 'style=\"display: none\";'
        }">
                <span id="apply_num_${jdData.PostUUID}"> 
                    View applicants
                </span>
            </button>
        </div>
        <div id="cmt_${jdData.PostUUID}_container" style="display: none;"></div>
    </div>
    `;

    fetch(
        `/api/interactions/like?post_uuid=${jdData.PostUUID}`,
        {
            method: "GET",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `bearer ${localStorage.getItem("accessToken")}`,
            },
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            for (let i = 0; i < data.length; i++) {
                if (data[i].LikeOwner == localStorage.getItem("userId")) {
                    console.log(`You liked ${jdData.PostUUID}`);
                    document.getElementById(
                        `like_name_${jdData.PostUUID}`
                    ).innerHTML = `Unlike`;
                }
            }
        });

    document.getElementById("jdContainer").appendChild(jdHTML);

    document.getElementById(`like_${jdData.PostUUID}`).onclick =
        async () => {
            likeList = await getLikeList(jdData.PostUUID);
            createLikeListContainer(likeList);
        };

    document.getElementById(`cmt_${jdData.PostUUID}`).onclick =
        () => {
            let commentListContainer = document.querySelector(`#cmt_${jdData.PostUUID}_container`);
            if (commentListContainer.style.display == "none") {
                commentListContainer.style.display = "block";
                getCommentList(jdData.PostUUID);
            } else {
                commentListContainer.style.display = "none";
            }
        };

    document.getElementById(
        `like_action_${jdData.PostUUID}`
    ).onclick = () => {
        fetch(
            `/api/interactions/like?post_uuid=${jdData.PostUUID}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `bearer ${localStorage.getItem(
                        "accessToken"
                    )}`,
                },
            }
        )
            .then(function (response) {
                if (response.status == 200) {
                    if (
                        document.getElementById(
                            `like_name_${jdData.PostUUID}`
                        ).innerHTML == `Like`
                    ) {
                        document.getElementById(
                            `like_name_${jdData.PostUUID}`
                        ).innerHTML = `Unlike`;
                    } else {
                        document.getElementById(
                            `like_name_${jdData.PostUUID}`
                        ).innerHTML = `Like`;
                    }
                }
                return response.json();
            })
            .then(function (data) {
                // console.log("Like action done");
                return;
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    document.getElementById(`apply_${jdData.PostUUID}`).onclick =
        () => {
            applyForJob(jdData.PostUUID);
        };

    document.getElementById(`view_applicants_${jdData.PostUUID}`).addEventListener('click', () => {
        renderApplicantList(jdData.PostUUID);
    });
}

document.addEventListener("DOMContentLoaded", async function () {
    let response = await fetch("/api/posts/all?offset=0&limit=10", {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    });
    let data = await response.json();
    for (let i = 0; i < data.length; i++) {
        await createJdContainer(data[i]);
    }
});

async function getApplicationList(postUUID) {
    const response = await fetch(`/api/post/${postUUID}/applications`, {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${localStorage.getItem("accessToken")}`,
        },
    });
    const applicationList = await response.json();
    return {
        status: response.status,
        list: applicationList,
    };
}

async function createApplicationListContainer(applicationList) {
    if (applicationList.length == 0) {
        return `
        <h5>No applications to show</h5>
        `;
    }
    const applicationListHtml = [];
    for (let i = 0; i < applicationList.length; i++) {
        let application = applicationList[i];
        let response = await fetch(`/api/profile/profile?uuid=${application.ApplicantUUID}`, {
            method: "GET",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `bearer ${localStorage.getItem("accessToken")}`,
            },
        })
        try {
            let data = await response.json();
            // Shows realname and avatar (.UserRealName and .UserAvatar)
            applicationListHtml.push(`
            <div class="row bg-light align-items-center m-2 p-1">
                <div class="col-2">
                    <img
                        src="${data.UserAvatar ? 'data:image/png;base64,' + data.UserAvatar : 'https://placehold.co/200x200'}"
                        alt="Avatar"
                        class="rounded-circle"
                        style="width: 45px; aspect-ratio: 1"
                    />
                </div>
                <div class="col-10">
                    <a class="nav-item" href="/profile/?id=${data.UUID}" style="text-decoration: none;color: inherit;">
                        ${data.UserRealName}
                    </a>
                </div>
            </div>
            `);
        } catch (error) {
            console.log(error);
        }
    }
    return applicationListHtml.join(``);
}

async function renderApplicantList(postUUID) {
    const result = await getApplicationList(postUUID);
    let resultHtml;
    if (result.status != 200) {
        resultHtml = `<h5>${result.list.detail}</h5>`;
    } else {
        resultHtml = await createApplicationListContainer(result.list);
    }
    document.getElementById('applicantListModalBody').innerHTML = resultHtml;
}

function extractInfoFromJd(jdElement) {
    jdElement = jdElement.querySelector(".card.shadow.gedf-card.mb-3");
    let username = jdElement.children[0].textContent.trim();
    let title = jdElement.children[1].querySelector(".card-title").textContent.trim();
    let text = jdElement.children[1].querySelector(".card-text").textContent.trim()
    return username + "\n" + title + "\n" + text;
}

function filterJd() {
    let jdContainer = document.getElementById("jdContainer");
    let jdElements = Array.from(jdContainer.children);
    jdElements.splice(0, 2);
    for (let i = 0; i < jdElements.length; i++) {
        let jdElement = jdElements[i];
        let jdText = extractInfoFromJd(jdElement);
        if (jdText.toLowerCase().includes(document.querySelector("#jdSearchInput").value.toLowerCase())) {
            jdElement.style.display = "block";
        } else {
            jdElement.style.display = "none";
        }
    }
}

document.querySelector("#jdSearchInput").addEventListener("keyup", filterJd);