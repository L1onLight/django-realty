let ratingS = document.getElementsByClassName("rating-s")

for (let index = 0; index < ratingS.length; index++) {
    const element = ratingS[index];
    const rating = element.querySelector("#rating-number").innerText
    const stars_1 = element.querySelectorAll(".mainStar-s")

    for (let index = 0; index < rating; index++) {
        const item = stars_1[index];
        item.classList.add("filled")
    }


}


function transform(method, div) {
    const s_star = document.getElementById("s-static")
    const f_star = document.getElementById("s-form")
    if (method === "show") {
        div.tag = 'textarea'
        div.classList.add("ss")
        const newText = document.createElement("textarea")
        newText.classList.add("review-body")
        newText.name = "review_body_edit"
        newText.id = "body-1"
        newText.rows = 5
        newText.innerText = div.innerHTML
        newText.required = true
        div.parentElement.appendChild(newText)
        s_star.classList.add("d-hidden")
        f_star.classList.remove("d-hidden")
        div.classList.add("d-hidden")


    } else {
        const newText = document.getElementById("body-1")
        newText.remove()
        s_star.classList.remove("d-hidden")
        f_star.classList.add("d-hidden")

        div.classList.remove("d-hidden")


        // div.tag = "div"
    }
}

const editB = document.getElementById("edit-btn")
editB.addEventListener("click", function (e) {
    e.preventDefault()
    const userReview = document.getElementById("user-review")
    const saveBtn = document.getElementById("save-btn")
    saveBtn.classList.remove('hidden')
    // saveBtn.classList.console.log(userReview)
    const reviewBody = userReview.querySelector("#review-body")

    if (editB.innerText === "Edit") {
        editB.innerText = "Cancel"
        transform("show", reviewBody)
    } else {
        editB.innerText = "Edit"
        saveBtn.classList.add("hidden")
        transform("hide", reviewBody)

    }
    console.log(reviewBody)
})