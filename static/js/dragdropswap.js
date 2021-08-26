function allowDrop(ev) {
    ev.preventDefault();  // default is not to allow drop
}
function dragStart(ev) {
    // The 'text/plain' is referring the Data Type (DOMString) 
    // of the Object being dragged.
    // ev.target.id is the id of the Object being dragged
    var caller = ev.target || ev.srcElement;

    ev.dataTransfer.setData("text/plain", ev.target.id);
    ev.dataTransfer.setData("id", caller.id);

}
function dropIt(ev) {
    ev.preventDefault();  // default is not to allow drop
    let sourceId = ev.dataTransfer.getData("text/plain");
    let ticketId = ev.dataTransfer.getData("id");

    let sourceIdEl = document.getElementById(sourceId);
    let sourceIdParentEl = sourceIdEl.parentElement;
    // ev.target.id here is the id of target Object of the drop
    let targetId = findUpTag(ev.target).id;
    let targetEl = document.getElementById(findUpTag(ev.target).id);
    let targetParentEl = targetEl.parentElement;

    console.log(sourceIdEl.id);
    console.log(targetId);

    // Compare List names to see if we are going between lists
    // or within the same list
    if (targetParentEl.id !== sourceIdParentEl.id) {
        // If the source and destination have the same 
        // className (card), then we risk dropping a Card in to a Card
        // That may be a cool feature, but not for us!
        if (targetEl.className === sourceIdEl.className) {
            // Append to parent Object (list), not to a 
            // Card in the list
            // This is in case you drag and drop a Card on top 
            // of a Card in a different list
            targetParentEl.appendChild(sourceIdEl);

        } else {
            console.log("target", ev.target);

            if (targetId === 'list1') {
                changeState(ticketId, 0, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list2') {
                changeState(ticketId, 1, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list3') {
                changeState(ticketId, 2, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list4') {
                changeState(ticketId, 3, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list5') {
                changeState(ticketId, 0, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list6') {
                changeState(ticketId, 1, targetId, sourceId, appendToDestination);
            } else if (targetId === 'list7') {
                changeState(ticketId, 2, targetId, sourceId, appendToDestination);
            } else {
                changeState(ticketId, 3, targetId, sourceId, appendToDestination);
            }

        }

    } else {
        // Same list. Swap the text of the two cards
        // Just like swapping the values in two variables

        // Temporary holder of the destination Object
        let holder = targetEl;
        // The text of the destination Object. 
        // We are really just moving the text, not the Card
        let holderText = holder.textContent;
        // Replace the destination Objects text with the sources text
        targetEl.textContent = sourceIdEl.textContent;
        // Replace the sources text with the original destinations
        sourceIdEl.textContent = holderText;
        holderText = '';
    }

}
function appendToDestination(target, source) {
    let sourceIdEl = document.getElementById(source);
    // ev.target.id here is the id of target Object of the drop
    let targetEl = document.getElementById(target)
    targetEl.appendChild(sourceIdEl);
}

function findUpTag(el) {
    if (el.id == "list1" || el.id == "list2" || el.id == "list3" || el.id == "list4" || el.id == "list5" || el.id == "list6" || el.id == "list7" || el.id == "list8") {
        return el;
    }
    while (el.parentNode) {
        el = el.parentNode;

        if (el.id == "list1" || el.id == "list2" || el.id == "list3" || el.id == "list4" || el.id == "list5" || el.id == "list6" || el.id == "list7" || el.id == "list8") {
            return el;

        }
    }
    console.log("not found");
    return null;
}

function getParentId(element) {
    console.log("new");
    console.log(element);
    if (element.id != null) {
        console.log(element.id);
        return element.id;
    } else {
        getParentId(element.parentNode);
    }
}
function changeState(id, destination, target, source, callback) {
    let data = new FormData();
    let csrftoken = getCookie('csrftoken');

    data.append("id", id);
    data.append("state", destination);
    data.append("csrfmiddlewaretoken", csrftoken);
    axios.post('change_ticket_state/', data) // 4
        .then(res => {
            if (res.data.status) {
                console.log(res.data);
                callback(target, source);
            }
        }) // 5
        .catch(errors => console.log(errors));
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
