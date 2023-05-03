const primaryNav = document.querySelector("#primary-navigation");
const navToggle = document.querySelector("#nav-toggle");

navToggle.addEventListener('click', function(evt){
    console.log(evt.target)
    const showNav = primaryNav.getAttribute("data-visible"); 

    if (showNav === "false"){
        primaryNav.setAttribute("data-visible", true);
        navToggle.setAttribute("area-expanded", true);
        
    } else {
        primaryNav.setAttribute("data-visible", false);
        navToggle.setAttribute("area-expanded", false);
    }
});


// LOADER
// navbar-homepage buttons
const navHomepage = document.querySelector("#homepage-nav")
const navActivities = document.querySelector("#activities-nav")
const navEvents = document.querySelector("#events-nav")
const navPlaces = document.querySelector("#places-nav")
const navInfo = document.querySelector("#info-nav")
const navCenter = document.querySelector("#center-nav")
const navAlert = document.querySelector("#alert-nav")
const activityLinks = document.querySelector("#activity-link")
const placeLinks = document.querySelector("#place-link")

const loader = document.querySelector("#loader")
const page = document.querySelector("#main-content")
const body = document.querySelector("body")

function showLoader() {
    body.classList.remove(...body.classList)
    page.classList.add("hidden")
    loader.classList.remove("hidden")
}

const timeout = setTimeout(showLoader, 750);

window.addEventListener("load", function () {
    clearTimeout(timeout);
    page.classList.remove("hidden");
    loader.classList.add("hidden");
});

window.onbeforeunload = function() {
    const timeout = setTimeout(showLoader, 750);
};

// navHomepage.addEventListener("click", showLoader)
// navActivities.addEventListener("click", showLoader)
// navEvents.addEventListener("click", showLoader)
// navPlaces.addEventListener("click", showLoader)
// // navInfo.addEventListener("click", showLoader)
// // navCenter.addEventListener("click", showLoader)
// // navAlert.addEventListener("click", showLoader)

// activityLinks.forEach(link => link.addEventListener("click", showLoader))
// placeLinks.forEach(link => link.addEventListener("click", showLoader))