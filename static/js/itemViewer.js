function changeMainImage(img) {
    removeActive();
    const mainImage = document.getElementById("mainImageViewer");
    mainImage.src = img.src;
    img.classList.add("active-carousel");

    scrollToActiveImage(img)
}

function scrollToActiveImage(activeImage) {
    console.log('tr')
    const carouselContainer = document.getElementById("carousel");
    carouselContainer.scrollLeft = activeImage.offsetLeft - carouselContainer.offsetLeft;
}

function removeActive() {
    const imgArray = document.getElementsByClassName("secondary-img");
    for (let index = 0; index < imgArray.length; index++) {
        const element = imgArray[index];
        element.classList.remove("active-carousel");
    }
}

function nextImage() {
    const imgArray = document.getElementsByClassName("secondary-img");
    const activeImage = document.querySelector(".active-carousel");
    const mainImage = document.getElementById("mainImageViewer");
    let item = NaN;

    if (activeImage) {
        const currentIndex = Array.from(imgArray).indexOf(activeImage);
        activeImage.classList.remove("active-carousel");

        const nextIndex = (currentIndex + 1) % imgArray.length;
        imgArray[nextIndex].classList.add("active-carousel");
        mainImage.src = imgArray[nextIndex].src;
        item = imgArray[nextIndex];
    } else {
        imgArray[0].classList.add("active-carousel");
        item = imgArray[0];
    }
    scrollToActiveImage(item);

}

function previousImage() {
    const imgArray = document.getElementsByClassName("secondary-img");
    const activeImage = document.querySelector(".active-carousel");
    const mainImage = document.getElementById("mainImageViewer");
    let item = NaN;
    if (activeImage) {
        const currentIndex = Array.from(imgArray).indexOf(activeImage);
        activeImage.classList.remove("active-carousel");

        const prevIndex =
            (currentIndex - 1 + imgArray.length) % imgArray.length;
        imgArray[prevIndex].classList.add("active-carousel");
        mainImage.src = imgArray[prevIndex].src;
        item = imgArray[prevIndex];
    } else {
        imgArray[imgArray.length - 1].classList.add("active-carousel");
        item = imgArray[imgArray.length - 1];
    }
    scrollToActiveImage(item);

}

function handleScroll(event) {
    event = event || window.event; // Handle older browser versions

    const isShiftPressed = event.shiftKey || false;

    if (isShiftPressed) {
        return;
    }

    if (event.preventDefault) {
        event.preventDefault();
    } else {
        event.returnValue = false; // Handle older browser versions
    }
    const scrollAmount = event.deltaY || event.detail || event.wheelDelta;
    const carousel = document.getElementById("carousel");
    carousel.scrollLeft += scrollAmount;
}


document.getElementById("nextBtn").addEventListener("click", nextImage);
document.getElementById("prevBtn").addEventListener("click", previousImage);
