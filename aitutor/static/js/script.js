function searchLessons() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let items = document.getElementsByClassName("lesson-item");

    for (let i = 0; i < items.length; i++) {
        let lesson = items[i].innerText.toLowerCase();
        if (lesson.includes(input)) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }
}