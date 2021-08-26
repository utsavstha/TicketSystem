document.addEventListener('DOMContentLoaded', function () {
    const arrUpClass = document.querySelectorAll(".up-arrow");
    for (let i of arrUpClass) {
        i.addEventListener("click", (e) => {
            if (e.target.classList.contains("up-arrow")) {
                sortUp(e);
            }
        })
    }
    const arrDownClass = document.querySelectorAll(".down-arrow");
    for (let i of arrDownClass) {
        i.addEventListener("click", (e) => {
            if (e.target.classList.contains("down-arrow")) {
                sortDown(e);
            }
        })
    }
}, false);

function sortUp(e) {
    let parent = e.target.parentElement.parentElement.parentElement.parentElement;
    toSort = Array.prototype.slice.call(parent.children, 0);
    backup = toSort[0]
    toSort.shift()
    toSort.sort(function (a, b) {
        var one = getPriorityValue(a);
        var two = getPriorityValue(b)
        return one - two;
    });
    parent.innerHTML = "";
    parent.appendChild(backup);
    for (var i = 0, l = toSort.length; i < l; i++) {
        parent.appendChild(toSort[i]);
    }

}

function getPriorityValue(element) {
    return element.getAttribute('data-value')
}

function sortDown(e) {
    let parent = e.target.parentElement.parentElement.parentElement.parentElement;
    toSort = Array.prototype.slice.call(parent.children, 0);
    backup = toSort[0]
    toSort.shift()
    toSort.sort(function (a, b) {
        var one = getPriorityValue(a);
        var two = getPriorityValue(b)
        return two - one;
    });
    parent.innerHTML = "";
    parent.appendChild(backup);
    for (var i = 0, l = toSort.length; i < l; i++) {
        parent.appendChild(toSort[i]);
    }
}