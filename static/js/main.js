const dropDownDiv = document.getElementById("dropdown");
const dropDownBtn = document.getElementById("dropdownBtn");

function activateDropdown() {
    var myDiv = document.getElementsByClassName("nav-background")[0];
    const logo = document.getElementsByClassName("logo-text")[0];
    dropDownDiv.classList.toggle("d-hidden");
    myDiv.classList.toggle("active-navbar");
    logo.classList.toggle("active-logo");
}

dropDownBtn.addEventListener("click", activateDropdown);

function resizeImg() {
    const imagesWrapper = document.getElementsByClassName("img-wrapper");

    for (let index = 0; index < imagesWrapper.length; index++) {
        const element = imagesWrapper[index];
        const img = element.getElementsByClassName("img-Q")[0];
        if (element.offsetWidth > img.offsetWidth) {
            img.classList.add("resize");
        } else if (
            img.offsetWidth < element.offsetWidth &&
            window.offsetWidth > 690
        ) {
            img.classList.remove("resize");
        }

    }
}

if (document.getElementsByClassName("img-wrapper")) {
    resizeImg();
}

function getCsrfToken() {
    // Retrieve the CSRF token from a cookie
    const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
    return cookieValue ? cookieValue[1] : '';
}


function sendPostRequest(url) {
    const csrfToken = getCsrfToken();

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    })
        .then(response => {
            if (response.ok) {
                // Request was successful

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


function removeFav(btn, type, slug) {
    const confirmation = document.createElement("div")
    confirmation.classList.add("confirmation")
    confirmation.classList.add("shadow")

    const confirmationHeader = document.createElement("div")
    confirmationHeader.classList.add("confirmation-header")
    confirmationHeader.classList.add(type)
    const header = document.createElement("h5")
    header.innerText = "Confirmation"
    confirmationHeader.appendChild(header)
    confirmation.appendChild(confirmationHeader)
    const confirmationBody = document.createElement("div")
    confirmationBody.classList.add("confirmation-body")
    confirmationBody.innerHTML = "<p>Are you want to remove this from favorites?</p>"
    confirmation.appendChild(confirmationBody)
    const confirmationButtons = document.createElement("div")
    confirmationButtons.classList.add("confirmation-buttons")


    const confirmBtn = document.createElement("button")
    const cancelBtn = document.createElement("button")
    confirmBtn.innerText = "Yes"
    cancelBtn.innerText = 'No'
    confirmationButtons.appendChild(confirmBtn)
    confirmationButtons.appendChild(cancelBtn)
    cancelBtn.id = "cancel-confirmation"
    cancelBtn.addEventListener("click", function () {
        confirmation.remove()
    })
    confirmation.appendChild(confirmationButtons)
    const body = document.getElementsByTagName('body')[0]
    body.appendChild(confirmation)
    confirmBtn.addEventListener("click", function () {
        removeFavorite(slug);
        confirmation.remove()
        location.reload()
    })

}

function removeFavorite(slug) {
    const url = `/api/remove-fav/${slug}/`;
    sendPostRequest(url);

}

function addFav(btn, slug) {
    if (btn.classList.contains("loved")) {
        const url = `/api/remove-fav/${slug}/`;
        sendPostRequest(url);
        btn.classList.remove('loved')
    } else {
        const url = `/api/add-fav/${slug}/`;
        sendPostRequest(url);
        btn.classList.add('loved')

    }


}

const expandBtns = document.getElementsByClassName("msg-wrapper")

function expandMessages(btn) {
    console.log(btn)
    btn.classList.remove('pointer');
    const pTag = btn.getElementsByTagName("p")[0]
    btn.style.content = 'none !important';
    pTag.classList.remove("hidden")

}

for (let index = 0; index < expandBtns.length; index++) {
    const element = expandBtns[index];
    element.addEventListener('click', function () {
        expandMessages(element)

    })
}

const mainText = document.getElementsByClassName("main-text")

for (let index = 0; index < mainText.length; index++) {
    const element = mainText[index];
    if (element.offsetHeight < 72) {
        element.classList.remove("hidden")
        element.parentElement.classList.remove("pointer")
    }
}

const date = document.getElementById("DATE")
date.innerText = new Date().getFullYear()
