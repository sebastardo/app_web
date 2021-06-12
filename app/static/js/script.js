
/**
 * Verify if field value already exists in DB
 * @param {*} value Value to compare
 * @param {*} field Field in DB
 * @param {*} updateId Form field ID to be updated
 */
function validateField(value, field, updateId) {
    let url = `/validatefield?field=${field}&value=${value}`;
    let request;
    if (window.XMLHttpRequest) {
        request = new window.XMLHttpRequest();
    }
    else {
        request = new window.ActiveXObject("Microsoft.XMLHTTP");
    }
    if (value.length >= 4) {
        request.open("GET", url, true);
        request.send();
        request.onreadystatechange = function () {
            if (request.readyState == 4 && request.status == 200) {
                if (request.responseText == "Used") {
                    document.getElementById(updateId).classList.add("d-block");
                }
                else {
                    document.getElementById(updateId).classList.remove("d-block");
                }
            }
        };
    }
}
/**
 * Verify if both passwords match
 * @param {*} pass1 Password
 * @param {*} pass2 Password
 * @param {*} updateId Form field ID to be updated
 */
function verifyPasswords(pass1, pass2, updateId) {
    console.log(pass1)
    console.log(pass2)
    if (pass1 != "" && pass2 != "") {
        if (pass1 == pass2) {
            document.getElementById(updateId).classList.remove("d-block");
            return true;
        }
        else {
            document.getElementById(updateId).classList.add("d-block");
            return false;
        }
    }
    else {
        return false;
    }
}

