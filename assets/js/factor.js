let amount = document.querySelector('.amount');
let fee = document.querySelector('.fee');
let total = document.querySelector('.total');
let balance = document.querySelector('.balance');


total.innerText = Number(amount.innerText) + Number(((amount.innerText/100)*1.2).toFixed(2));
total.innerText += "$";
fee.innerText = Number((amount.innerText/100)*1.2).toFixed(2) + "$";
amount.innerText += "$";
pop_span.innerHTML = `<img width="30" height="30" src="https://img.icons8.com/officel/30/spam.png" alt="spam"/>  balance is less then ${total.innerText}$`;

