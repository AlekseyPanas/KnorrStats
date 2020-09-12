// background fade image adjustment

function fade_bg_size() {
    // Ensures that the fade background image at the top with the logo is fully height of parent
    let logo_header_height = $(".index-logo-head").outerHeight().toString();
    $(".index-logo-head").css("background-size", "100% " + logo_header_height + "px");
};

$(window).ready(fade_bg_size);
$(window).resize(fade_bg_size);





// Scroll Progress Bar

$(window).scroll(() => {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
});