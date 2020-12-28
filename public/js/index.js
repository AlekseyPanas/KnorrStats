// Ensures that the fade background image at the top with the logo is fully height of parent
function fade_bg_size() { 
    let logo_header_height = $(".index-logo-head").outerHeight().toString();
    $(".index-logo-head").css("background-size", "100% " + logo_header_height + "px");
};

// Gets the position of the invisible logo at the top which acts as a placeholder for animation endpoints
function get_fixed_logo_pos() {
    return $(".index-logo-placeholder").offset();
};

// Same as above except for size
function get_fixed_logo_size() {
    return {
        height: $(".index-logo-placeholder").outerHeight(),
        width: $(".index-logo-placeholder").outerWidth()
    };
};

// Sets the fixed logo position, size, and z-index. Sets navbar logo section's height
function set_top_logo_css() {
    let logo_pos = get_fixed_logo_pos();
    let logo_size = get_fixed_logo_size();

    $(".navbar-logo-container").css("height", 0 + "px");
    $(".index-logo-fixed").css("z-index", 2); 
    $(".index-logo-fixed").css("width", logo_size.width + "px");
    $(".index-logo-fixed").css("height", logo_size.height + "px");
    $(".index-logo-fixed").css("left", logo_pos.left + "px");
    $(".index-logo-fixed").css("top", logo_pos.top + "px");
    $(".index-logo-fixed").css("visibility", "visible");   
}

// Same as above except for when the logo is collapsed in the navbar
function set_scrolled_logo_css() {
    $(".navbar-logo-container").css("height", 40 + "px");
    $(".index-logo-fixed").css("z-index", 5); 
    $(".index-logo-fixed").css("width", 64 + "px");
    $(".index-logo-fixed").css("height", 40 + "px");
    $(".index-logo-fixed").css("left", 10 + "px");
    $(".index-logo-fixed").css("top", 0 + "px");
    $(".index-logo-fixed").css("visibility", "visible");  
}

// When ready
$(window).ready(() => {
    // Calls at first when ready
    fade_bg_size();

    // Scroll Progress Bar
    $(window).scroll(() => {
        var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var scrolled = (winScroll / height) * 100;
        $("#myBar").css("width", scrolled + "%");
    });

    // On resize, adjusts background
    $(window).resize(() => {
        fade_bg_size(); 
        if (is_top) {
            set_top_logo_css();
        };
    });

    // Checks if scrolled to top
    let is_top = (($(window).scrollTop() == 0) ? true : false);
    // Initially sets logo position based on if scrolled to top
    if (is_top) {
        set_top_logo_css();  
    } else {
        set_scrolled_logo_css();  
    }
    // Animate logo to minimize to navbar
    $(window).scroll(() => {
        let logo_pos_nav = {top: 0, left: 10};
        let logo_height_nav = 40 + "px";
        let logo_width_nav = 64 + "px";

        let logo_pos_top = get_fixed_logo_pos();
        let logo_size_top = get_fixed_logo_size();

        var pos = $(window).scrollTop();
        // If scrolled to top
        if (pos == 0) {
            // Makes sure the animation is only stopped and started once
            if (!is_top) {
                // Stops previous animations
                $(".navbar-logo-container").stop();
                $(".index-logo-fixed").stop();

                // Sets z-index below navbar
                $(".index-logo-fixed").css("z-index", 2); 

                // Hides the navbar logo section
                $(".navbar-logo-container").animate({
                    height: 0 + "px"
                }, 250, "swing", () => {})
    
                // Brings logo to large size at top
                $(".index-logo-fixed").animate({
                    left: logo_pos_top.left,
                    top: logo_pos_top.top,
                    height: logo_size_top.height,
                    width: logo_size_top.width
                }, 250, "swing", () => {});
            }

            is_top = true;
            
        // If not scrolled to top
        } else {
            if (is_top) {
                // Stops animations
                $(".navbar-logo-container").stop();
                $(".index-logo-fixed").stop();

                // Sets z-index above navbar
                $(".index-logo-fixed").css("z-index", 5);                

                // Shows navbar logo section
                $(".navbar-logo-container").animate({
                    height: 40 + "px"
                }, 250, "swing", () => {})
    
                // Minimizes logo into navbar
                $(".index-logo-fixed").animate({
                    left: logo_pos_nav.left,
                    top: logo_pos_nav.top,
                    height: logo_height_nav,
                    width: logo_width_nav
                }, 250, "swing", () => {});
            }

            is_top = false;
        }
    });

});