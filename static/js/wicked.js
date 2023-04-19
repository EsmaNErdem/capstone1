
const activityFav = document.querySelectorAll("#activity-fav");
const activityMark = document.querySelectorAll("#activity-mark");
const eventFav = document.querySelectorAll("#event-fav");
const eventMark = document.querySelectorAll("#event-mark");
const placeFav = document.querySelectorAll("#place-fav");
const placeMark = document.querySelectorAll("#place-mark");

// Activity
// Adding event listener to activity hearts

async function toggleActivityFav(event) {
    const heart = event.target;

    if(!heart.classList.contains("favorite")) {
        let id = heart.getAttribute("data-id");
        let title = heart.getAttribute('data-title');
        let imageUrl = heart.getAttribute('data-image-url');
        let description = heart.getAttribute('data-description');
        heart.classList.add("favorite");
        try {
                const resp = await axios.post(
                    "/api/activity/favorite",
                    {
                        id,
                        title,
                        imageUrl,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = heart.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/activity/${id}/favorite`
        );
        heart.classList.remove("favorite");
    }
}


activityFav.forEach((element) => {
    element.addEventListener("click", toggleActivityFav);
});

// Adding event listener to activity bookmarks

async function toggleActivityMark(event) {
    const bookmark = event.target;

    if(!bookmark.classList.contains("bookmark")) {
        let id = bookmark.getAttribute("data-id");
        let title = bookmark.getAttribute('data-title');
        let imageUrl = bookmark.getAttribute('data-image-url');
        let description = bookmark.getAttribute('data-description');
        bookmark.classList.add("bookmark");
        try {
                const resp = await axios.post(
                    "/api/activity/bookmark",
                    {
                        id,
                        title,
                        imageUrl,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = bookmark.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/activity/${id}/bookmark`
        );
        bookmark.classList.remove("bookmark");
    }
}

activityMark.forEach((element) => {
    element.addEventListener("click", toggleActivityMark);
});




// Event
// Adding event listener to event hearts

async function toggleEventFav(event) {
    const heart = event.target;

    if(!heart.classList.contains("favorite")) {
        let id = heart.getAttribute("data-id");
        let title = heart.getAttribute('data-title');
        let description = heart.getAttribute('data-description');
        heart.classList.add("favorite");
        try {
                const resp = await axios.post(
                    "/api/event/favorite",
                    {
                        id,
                        title,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = heart.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/event/${id}/favorite`
        );
        heart.classList.remove("favorite");
    }
}


eventFav.forEach((element) => {
    element.addEventListener("click", toggleEventFav);
});

// Adding event listener to event bookmarks

async function toggleEventMark(event) {
    const bookmark = event.target;

    if(!bookmark.classList.contains("bookmark")) {
        let id = bookmark.getAttribute("data-id");
        let title = bookmark.getAttribute('data-title');
        let description = bookmark.getAttribute('data-description');
        bookmark.classList.add("bookmark");
        try {
                const resp = await axios.post(
                    "/api/event/bookmark",
                    {
                        id,
                        title,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = bookmark.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/event/${id}/bookmark`
        );
        bookmark.classList.remove("bookmark");
    }
}

eventMark.forEach((element) => {
    element.addEventListener("click", toggleEventMark);
});




// Place
// Adding event listener to place hearts

async function togglePlaceFav(place) {
    const heart = place.target;

    if(!heart.classList.contains("favorite")) {
        let id = heart.getAttribute("data-id");
        let imageUrl = heart.getAttribute('data-image-url');
        let title = heart.getAttribute('data-title');
        let description = heart.getAttribute('data-description');
        heart.classList.add("favorite");
        try {
                const resp = await axios.post(
                    "/api/place/favorite",
                    {
                        id,
                        imageUrl,
                        title,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = heart.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/place/${id}/favorite`
        );
        heart.classList.remove("favorite");
    }
}


placeFav.forEach((element) => {
    element.addEventListener("click", togglePlaceFav);
});

// Adding event listener to place bookmarks

async function togglePlaceMark(place) {
    const bookmark = place.target;

    if(!bookmark.classList.contains("bookmark")) {
        let id = bookmark.getAttribute("data-id");
        let imageUrl = bookmark.getAttribute('data-image-url');
        let title = bookmark.getAttribute('data-title');
        let description = bookmark.getAttribute('data-description');
        bookmark.classList.add("bookmark");
        try {
                const resp = await axios.post(
                    "/api/place/bookmark",
                    {
                        id,
                        imageUrl,
                        title,
                        description
                    });
                console.log(resp);
            } catch (err) {
                console.error(err);
            }
    } else {
        let id = bookmark.getAttribute("data-id");
        const resp = await axios.delete(
            `/api/place/${id}/bookmark`
        );
        bookmark.classList.remove("bookmark");
    }
}

placeMark.forEach((element) => {
    element.addEventListener("click", togglePlaceMark);
});
