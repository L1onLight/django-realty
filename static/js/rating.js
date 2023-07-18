// const fieldSet = document.getElementById()

function autoRating() {
    if (document.getElementById("rating-number-form")) {
        const stars = document.getElementsByClassName("mainStar")
        const rating = document.getElementById("rating-number-form").innerText
        for (let i = 0; i < stars.length && i < rating; i++) {
            const item = stars[i];
            item.classList.add("filled")
        }
    } else {
        const stars = document.getElementsByClassName("mainStar")

        for (let i = 0; i < stars.length && i < 10; i++) {
            const item = stars[i];
            item.classList.add("filled")
        }
    }

}

autoRating()

function removeRating() {
    const stars = document.getElementsByClassName("mainStar")

    for (let index = 0; index < stars.length; index++) {
        const element = stars[index];
        element.classList.remove("filled")

    }
}

function setRating(label) {
    const val = document.getElementById(label.getAttribute("for")).value
    const stars = document.getElementsByClassName("mainStar")

    removeRating()
    for (let i = 0; i < stars.length && i < val; i++) {
        const item = stars[i];
        item.classList.add("filled")
    }
}


const labels = document.querySelectorAll(".stars label")
labels.forEach((label) => {
    label.addEventListener('click', function () {
        setRating(label)
    })
});
