setInterval(() => {

    const amount = document.getElementById("id_amount");
    const amount_currect = document.querySelector(".amount-currect");

    if (amount.value !== ""){

        let main_array = [];
        const reverse_array = amount.value.split("").reverse();
        let amount_str = "";

        for(let i=0; i < reverse_array.length; i++ ){
            if (i%3 === 0 && i !== 0){
                main_array.push('.');
                main_array.push(reverse_array[i]);
            }else {
                main_array.push(reverse_array[i]);
            }
        };
        main_array = main_array.reverse();
        for(let i=0; i<main_array.length;i++){
            amount_str += main_array[i];
        }
        amount_currect.innerText = amount_str;

    }else if (amount.value === ""){
        amount_currect.innerText = "";
    }
},100);
setInterval(() => {    const card_number = document.getElementById("id_to");

    if (card_number.value.length === 36){
        let hmx = new XMLHttpRequest();
        hmx.open("GET",`api/v1/card/${card_number.value}`,false);
        hmx.send();
        let guide = document.querySelector(".guide");

        if (hmx.responseText === undefined) {
            guide.innerText = `${card_number.value} : card not found`;
        }
        else{
            guide.innerText = `${card_number.value} : ${JSON.parse(hmx.responseText).username}`;
        }

    }else if(card_number.value.length === 0 ){
        let guide = document.querySelector(".guide");
        guide.innerText = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
    }},2000
)