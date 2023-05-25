//profile image toggle
const profileToggle = document.querySelector("#profile-toggle");
const profileNav = document.querySelector("#profile-navigation")

profileToggle.addEventListener("mouseover", function(evt){
    const showProfileNav = profileNav.getAttribute("data-visible"); 

    if (showProfileNav === "false"){
        profileNav.setAttribute("data-visible", true);
        
    } else {
        profileNav.setAttribute("data-visible", false);
    }
});

window.addEventListener("click", function(evt) {
    profileNav.setAttribute("data-visible", false);
});

// navbar responsive toggle
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

window.addEventListener("load", function () {
    page.classList.remove("hidden");
    loader.classList.add("hidden");
});

window.onbeforeunload = function() {
    showLoader()
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


// Logo JS effect
const image =document.querySelector(".logo")
image.addEventListener('mouseover', () => {
    image.style.transition = 'transform 1s linear';
    image.style.transform = 'rotateY(360deg)';
  });
  
  image.addEventListener('mouseout', () => {
    image.style.transition = 'transform 0.5s linear';
    image.style.transform = 'rotateY(0deg)';
  });