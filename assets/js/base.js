let theme_local = localStorage.getItem("theme");
let header_links = document.querySelectorAll(".link");
let header = document.querySelector("header");
let abouts = document.querySelectorAll(".about");
let form = document.querySelector("form");
let inputs = document.querySelectorAll(".input");
let phone_input_base = document.querySelector(".phone-input");
let country_search = document.querySelector(".search-box");
let content = document.querySelector(".content");
let country_names = document.querySelector(".country-single");
let ham_lines = document.querySelector(".nav-ico");
let footer = document.querySelector(".footer");
let text_area = document.querySelector('textarea')


if (theme_local === "Dark"){

    ham_lines.src = "/static/img/ham/white.png";
    theme.innerHTML = `<img src="/static/img/theme/sun.png" alt="" height="35">`;
    document.body.style.backgroundColor = "#000000";
    header.style.background = "#1a1a1a";
    header.style.color = "#f4f4f4";
    footer.style.backgroundColor = "#1a1a1a";
    document.body.style.color = "#f4f4f4";

    if (abouts.length === 0){

        content.style.backgroundColor = "#1a1a1a";
        content.style.boxShadow = "none";
    }
    if (country_search !== null) {
        country_search.style.background = "#1a1a1a";
        country_search.style.color = "#f4f4f4";
    }
    for (i of header_links){
        i.style.color = "#f4f4f4";
    }
    if (form !== null){
        form.style.backgroundColor = "#1a1a1a";
        for (input of inputs){
            input.style.color = "#f4f4f4";
        }
    }
    if (phone_input_base !== null){
        phone_input_base.style.color = "#f4f4f4";
    }
    for (about of abouts){
        about.style.backgroundColor = "#1a1a1a";
        about.style.border = "none";
    }
    if (text_area !== null){
        text_area.style.color = "#f4f4f4"
    }


}
else if (theme_local === "Light"){
    ham_lines.src = "/static/img/ham/black.png";
    theme.innerHTML = `<img src="/static/img/theme/moon.png" alt="" height="35">`;
    header.style.background = "linear-gradient(90deg, rgba(115,222,250,1) 0%, rgba(244,244,244,1) 29%)";
    header.style.backgroundColor = "rgb(115,222,250)";
    footer.style.backgroundColor = "#f4f4f4";
    document.body.style.backgroundColor = "#FFFFFF";


    document.body.style.color = "#000000";
    if (abouts.length === 0) {
        content.style.backgroundColor = "#f4f4f4";
        content.style.boxShadow = "#e2e2e2 0px 0px 20px 1px";
    }
    // if (user_edit_content !== null){
    //     user_edit_content.style.backgroundColor = "#f4f4f4"
    //     user_edit_content.style.boxShadow = "#e2e2e2 0px 0px 20px 1px"
    // }
    // if (user_panel_content !== null){
    //     user_panel_content.style.backgroundColor = "#f4f4f4"
    //     user_panel_content.style.boxShadow = "#e2e2e2 0px 0px 20px 1px"
    // }
    if (country_search !== null) {
        country_search.style.background = "#f4f4f4";
        country_search.style.color = "#000000";
        for (country of country_name){
            country.style.background = "#f4f4f4";
        }
    }
    for (i of header_links){
        i.style.color = "#000000";
    }
    if (form !== null){
        form.style.backgroundColor = "#f4f4f4";
        for (input of inputs){
            input.style.color = "#000000";
        }
    }
    if (phone_input_base !== null){
        phone_input_base.style.color = "#000000";
    }
    for (about of abouts){
        about.style.backgroundColor = "#f4f4f4";
        about.style.border = "none";
    }
    if (text_area !== null){
        text_area.style.color = "#000000"
    }
}

