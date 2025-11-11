function create_card(user){
    let hmx = new XMLHttpRequest();
    hmx.open("POST","card-call",false);
    hmx.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    hmx.send(`user_id=${user}&secret_key=hi`);
    if (hmx.status === 201){
        window.location.reload();
    }

}