/*
 * When document finish loading, listen for user submission
 * and prevent originl form from submitting
 * Submission will be done using AJAX 
 * */
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("form").onsubmit = function() {
        const request = new XMLHttpRequest();
        const user_text = document.querySelector("input[type='text']").value;
        // Making sure user did indeed type/paste in text
        if ( user_text.length < 1 ) {
            return false;
        }
        if (user_text.includes(" ")) {
            return false;
        } 
        // request to server and response from server
        request.open("POST", "submission/");
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.success ) {
                // data is a JSON which hold response from server
                let output_space = document.querySelector(".url_output")
                // Make the hidden text box visible and output respponse
                // text into it
                output_space.style.display = "block";
                document.querySelector("#output").value = data.success;
            }
        }
        const data = new FormData();
        data.append("url", user_text);
        request.send(data);
        // Prevent page loading
        return false;
    }
})
