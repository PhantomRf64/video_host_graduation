const video_view = document.getElementById("video_player");
const likeBtn = document.getElementById("likeBtn");
const dislikeBtn = document.getElementById("dislikeBtn");
const commentForm = document.getElementById("comment_form");

let viewSent = false;
let likeProcessing = false;
let dislikeProcessing = false;

// ------------------------
// Отправка просмотров
// ------------------------
if (video_view) {
    video_view.addEventListener("timeupdate", function () {
        if (!video_view.duration || video_view.paused) return;

        const percent = (video_view.currentTime / video_view.duration) * 100;

        if (percent >= 35 && !viewSent) {
            viewSent = true;

            fetch(viewsUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ watched_percent: percent })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("views_count").innerText = data.views;
            });
        }
    });
}

// ------------------------
// Лайк
// ------------------------
if (likeBtn) {
    likeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        if (likeProcessing) return;  // блокируем повтор
        likeProcessing = true;

        fetch(reactionUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ action: "like" })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("likes").innerText = data.count_likes;
            document.getElementById("dislikes").innerText = data.count_dislikes;
            document.getElementById("views_count").innerText = data.count_views;
        })
        .finally(() => likeProcessing = false);
    });
}

// ------------------------
// Дизлайк
// ------------------------
if (dislikeBtn) {
    dislikeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        if (dislikeProcessing) return;
        dislikeProcessing = true;

        fetch(reactionUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ action: "dislike" })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("likes").innerText = data.count_likes;
            document.getElementById("dislikes").innerText = data.count_dislikes;
            document.getElementById("views_count").innerText = data.count_views;
        })
        .finally(() => dislikeProcessing = false);
    });
}

// ------------------------
// Комментарии
// ------------------------
if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const text = document.getElementById("comment_text").value.trim();
        if (!text) return;

        fetch(commentsUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ text: text })
        })
        .then(res => res.json())
        .then(data => {
            const div = document.getElementById("comments");
            const p = document.createElement("p");
            p.className = "mb-1 text-light";
            p.innerHTML = `<strong>${data.author}:</strong> ${data.text}`;
            div.appendChild(p);
            document.getElementById("comment_text").value = "";
        });
    });
}