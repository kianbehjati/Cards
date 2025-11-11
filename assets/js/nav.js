let ham = document.querySelector(".hamdiv");
let hamli = document.querySelector(".hamlist");
let ham_btn = document.querySelector(".nav-ico");
let theme = document.querySelector(".theme-ico");


function theme_change(sun,moon){
    let header_links = document.querySelectorAll(".link");
    let header = document.querySelector("header");
    let footer = document.querySelector('.footer');
    let abouts = document.querySelectorAll(".about");
    let form = document.querySelector("form");
    let inputs = document.querySelectorAll(".input");
    let phoneinput = document.querySelector(".phone-input");
    let country_search = document.querySelector(".search-box");
    let country_name = document.querySelectorAll(".country-single");
    let user_panel_content = document.querySelector(".user-panel-content");
    let user_edit_content = document.querySelector(".user-edit-content");
    let content = document.querySelector(".content");
    let text_area = document.querySelector('textarea');

    if (theme.id === "moon"){
        ham_btn.src = "/static/img/ham/white.png";

        localStorage.setItem("theme","Dark");

        theme.innerHTML = `<img src="${sun}" alt="" height="35">`;

        theme.id = "sun";
        document.body.style.backgroundColor = "#000000";
        header.style.background = "#1a1a1a";
        footer.style.backgroundColor = "#1a1a1a";
        header.style.color = "#f4f4f4";

        document.body.style.color = "#f4f4f4";
        if (abouts.length === 0){
            content.style.backgroundColor = "#1a1a1a";
            content.style.boxShadow = "none";
        }

        // if (user_edit_content !== null){
        //     user_edit_content.style.backgroundColor = "#1a1a1a"
        //     user_edit_content.style.boxShadow = "none"
        // }
        // if (user_panel_content !== null){
        //     user_panel_content.style.backgroundColor = "#1a1a1a"
        //     user_panel_content.style.boxShadow = "none"
        // }
        if (country_search !== null) {
            country_search.style.background = "#1a1a1a";
            country_search.style.color = "#f4f4f4";
            for (country of country_name){
                country.style.background = "#1a1a1a";
                country.style.color = "#f4f4f4";
            }
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
        if (phoneinput !== null){
            phoneinput.style.color = "#f4f4f4";
        }
        for (about of abouts){
            about.style.backgroundColor = "#1a1a1a";
            about.style.border = "none";
        }
        if (text_area !== null){
            text_area.style.color = "#000000";
        }


    }else if (theme.id === "sun"){

        localStorage.setItem("theme","Light");
        ham_btn.src = "/static/img/ham/black.png";
        theme.id = "moon";
        theme.innerHTML = `<img src="${moon}" alt="" height="35">`;
        header.style.background = "linear-gradient(90deg, rgba(115,222,250,1) 0%, rgba(244,244,244,1) 29%)";
        header.style.backgroundColor = "rgb(115,222,250)";
        footer.style.backgroundColor = "#f4f4f4";
        document.body.style.backgroundColor = "#FFFFFF";


        document.body.style.color = "#000000";

        if (abouts.length === 0){
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
                country.style.color = "#000000"
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
        if (phoneinput !== null){
            phoneinput.style.color = "#000000";
        }
        for (about of abouts){
            about.style.backgroundColor = "#f4f4f4";
            about.style.border = "none";
        }
        if (text_area !== null){
            text_area.style.color = "#f4f4f4";
        }
    }
}

ham_btn.addEventListener("click", () => {
    if (ham.style.maxHeight == "500px"){

        ham.style.maxHeight = "0";
        hamli.style.transition = "opacity 1s";
        hamli.style.opacity = "0";

        setTimeout(() => {
            ham.style.visibility = "hidden";
            hamli.style.transition = "opacity 0.5s 0.7s";
            },1500);


    }else {
        ham.style.visibility = "visible";
        hamli.style.opacity = "1";
        ham.style.maxHeight = "500px";
    }
});