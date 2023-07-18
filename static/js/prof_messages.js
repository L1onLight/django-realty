function sendPostRequestData(url, data) {
    const csrfToken = getCsrfToken();
    console.log(data)
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({message_id: data})
    })
        .then(response => {
            if (response.ok) {
                // Request was successful
                location.reload()
                return response.json(); // Parse the response body as JSON
            } else {
                // Request failed
                throw new Error('POST request failed');
            }
        })
        .then(data => {
            // Process the data received from the server
            console.log(data.message); // Access the message property from the response JSON

        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function moveToArchive(btn) {
    const messageDiv = btn.parentElement.parentElement.parentElement
    const slug = messageDiv.querySelector("#message-item-slug").innerText
    const messageId = messageDiv.querySelector("#message-id").innerText
    const url = `/api/move-to-archive/${slug}/`;
    const data = messageId
    console.log(data)
    sendPostRequestData(url, data)

}

function createOptions(btn) {

    const wrapper = btn.parentElement;
    const newDiv = document.createElement("div");
    newDiv.id = "options";
    const newSpan = document.createElement("span");
    newSpan.classList.add("moveToArchive");
    newSpan.innerText = "Move to Archive";
    newDiv.appendChild(newSpan);
    wrapper.appendChild(newDiv);
    newSpan.addEventListener("click", function () {
        moveToArchive(btn)
    })
    // Event listener to remove newDiv when clicking outside
    wrapper.addEventListener("click", function (event) {
        event.stopPropagation();
    });

    // Event listener to remove newDiv when clicking outside
    document.addEventListener("click", function () {
        newDiv.remove();
    });
}


const moreBtns = document.getElementsByClassName("btn-more")
for (let index = 0; index < moreBtns.length; index++) {
    const element = moreBtns[index];
    element.addEventListener("click", function () {
        if (document.getElementById("options")) {
            const opts = document.getElementById("options")
            opts.remove()
            return
        }
        createOptions(element)

    })
}