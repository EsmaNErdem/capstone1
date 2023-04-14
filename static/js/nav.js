const primaryNav = document.querySelector("#primary-navigation");
const navToggle = document.querySelector(".mobile-nav-toggle");

navToggle.addEventListener('click', function(evt){
    const showNav = primaryNav.getAttribute("data-visible"); 

    if (showNav === "false"){
        primaryNav.setAttribute("data-visible", true);
        navToggle.setAttribute("area-expanded", true);
        
    } else if (showNav === "true") {
        primaryNav.setAttribute("data-visible", false);
        navToggle.setAttribute("area-expanded", false);
    }
});