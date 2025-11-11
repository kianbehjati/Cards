function kind(){
    let urlparams = new URLSearchParams(location.search);

    let kind = urlparams.get("kind");
    if (kind === 'incoming'){
        urlparams.set("kind","outgoing");
        location.search = urlparams;
    }else if (kind === 'outgoing'){
        urlparams.set("kind","incoming");
        location.search = urlparams;
    }else {
        urlparams.set("kind","incoming");
        location.search = urlparams;
    }
}
function amount(){
    let urlparams = new URLSearchParams(location.search);

    let amount = urlparams.get('amount');

    if(amount === "highest"){
        urlparams.set("amount","lowest");
        location.search = urlparams;
    }
    else if (amount === "highest"){
        urlparams.set("amount","highest");
        location.search = urlparams;
    }else {
        urlparams.set("amount","highest");
        location.search = urlparams;
    }
}