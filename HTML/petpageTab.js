// ==UserScript==
// @name         Petpage Info Tab
// @description  Displays a box on Neopet Petpages with stats about the neopet like owner, age, etc.
// @author       penguinluver222
// @include        http*://www.neopets.com/~*
// @include        http*://www.neopets.com//~*
// ==/UserScript==

var petStats = {
    'name': document.getElementsByTagName("title")[0].innerHTML.trim().split(" ")[0], // get Neopet name,
    'year':'',
    'birthday':'',
    'owner': document.links[0].href.split("=")[1], // get username
}
var div = document.createElement("div");

function getBG(key) {
    let colors = {
    'red':'#F79895',
    'orange':'#FCCBA1',
    'yellow':'#FAF4BF',
    'green':'#BDE7BD',
    'grey': '#CCCCCC'
}
    let bg
    let value = petStats[key]
    if (key === 'name') {
        // classify names:
        if ( /\d/.test(value) ) {
            // VBN (red) if name has numbers
            bg = colors.red; }
        else if ( /_/.test(value) ) {
            //BN (orange) if name has underscores & no numbers
            bg = colors.orange; }
        else if ( /[A-Z]/.test(value.slice(1)) ) {
            // BN if random uppercase letters
            bg = colors.orange; }
        else if ( /[A-Z]/.test(value.slice(0,1)) ) {
            // WN if capitalized with no numbers or underscores
                 bg = colors.green; }
        else {
            // DN if all lowercase
            bg = colors.yellow; }
    }
    else if (key === 'owner') {
        let owner = petStats.owner
        if (value === 'none') {
            bg = colors.green;
            petStats.owner = `<b><a href="/pound/adopt.phtml?search=${petStats.name}" target="new">Adopt! ᐅ</a></b>`
        }
        else {
            bg = colors.grey;
            petStats.owner = `Owner:<br><a href="/userlookup.phtml?user=${owner}" target="new">${owner}</a>`
        }
    }
    else if (key ==='year') {

        if ( value === 'N/A' ) {
            bg = colors.grey;}
        else {
            petStats.year = `Y${petStats.year} (${petStats.year + 1998})`
            if (value < 3 ) {
                bg = colors.green; }
            else if (value < 10 ) {
                bg = colors.yellow; }
            else if (value < 20 ) {
                bg = colors.orange; }
            else {
                bg = colors.red; }
        }
    }
    else {
        bg = colors.grey;
    }
    return bg
    //div.innerHTML += `<p><b>${key}: </b>\t${petStats[key]}</p>`;
}

function getAge() {
    let age = {
        'hours':'',
        'bdayDT':'',
    }

    try {
        age.hours = document.body.innerHTML.match(/[0-9]* hours/)[0].split(" ")[0]; // finds pet age in hours
    }
    catch {
        petStats.birthday = '';
        petStats.year = '';
    }

    if ( age.hours ) {
        let dtOptions = {
            timeZone: 'America/Los_Angeles',
            month: 'long',
            day: 'numeric'
        }
        // Calculates pet's birthday
        age.bdayDT = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Los_Angeles" }));
        age.bdayDT.setHours(age.bdayDT.getHours() - parseInt(age.hours, 10));

        // Update Pet Age & Birthday
        petStats.birthday = new Intl.DateTimeFormat('default', dtOptions).format(age.bdayDT)
        petStats.year = age.bdayDT.getFullYear() - 1998
    }
}

function loadButtons(){
    var btn = document.createElement('div');
    var btn_x = document.createElement('div');

    btn.innerHTML = '<div id="btn_" class="btn">ᐊ</div>' //<button id='myButton'>Send default message</button>";
    div.appendChild(btn);

    btn_x.innerHTML = '<div id="btn_x" class="btn">⨉</div>' //<button id='myButton'>Send default message</button>";
    div.appendChild(btn);
    div.appendChild(btn_x);

    document.getElementById('btn_').addEventListener('click', hideMe, false);
    document.getElementById('btn_x').addEventListener('click', closeMe, false);
}

function hideMe() {
    var x = document.getElementById("petInfo_");
    var btn_ = document.getElementById("btn_");
    if (btn_.innerHTML==="ᐊ") {
        x.style.margin = '0 0 0 -102px';
        btn_.innerHTML = 'ᐅ';
    } else {
        btn_.innerHTML = 'ᐊ';
        x.style.margin = '0';
  }
}

function closeMe() {
    var x = document.getElementById("petInfo_")
    console.log('woop')
    x.style.display="none"
}

function createHTML() {
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = `
            #petInfo_ {
                position:fixed;
                top:14px;
                z-index:100;
                background:#ccc;
                min-width:100px;
                margin-left:0px;
                border:1px solid #999;
            }
            #petInfo_ p {
                display: block;
                text-align:center;
                padding:5px;
                margin:1px 0px;
                font:11px Tahoma;
            }

            #petInfo_ p a {
            color: #777;
            font:auto;
            letter-spacing:0px;
            border:0;
            margin:0;
            padding:0;
            }

            #petInfo_ img {
            display:block;
            margin: auto;
            padding:2px;
            border-radius:5px;}

            #btn_ {
            top:20px; }
            #btn_x {
            top:0px;
            }

            .btn {
            float:right;
            position:absolute;
            right:-18px;
            width:18px;
            height:18px;
            padding:0px;
            text-align:center;
            background:#ccc;}

            .btn:hover {
            cursor:pointer;}

        `;
    document.body.appendChild(css);

    div.setAttribute("id","petInfo_");
    div.innerHTML = `<img src="https://pets.neopets.com/cpn/${petStats.name}/1/3.png">`
    document.body.appendChild(div);
    //let showStats = (({name, birthday,owner}) => ({name, birthday,owner}))(petStats)
    for (const key in petStats) {
        if (petStats[key] != '') {
        div.innerHTML += `<p style="background:${getBG(key)};">\t${petStats[key]}</p>`; }
        console.log(petStats.key)
    }


    loadButtons();
}


getAge();
createHTML();
/*if (btn) {
    btn.addEventListener ("click", hideMe() , false);
}*/
