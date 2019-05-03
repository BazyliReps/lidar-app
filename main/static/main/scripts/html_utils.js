function hide(id) {
    const elem = document.getElementById(id);
    if (elem.style.display === "block") {
        elem.style.display = "none";
    } else {
        elem.style.display = "block";
    }
}