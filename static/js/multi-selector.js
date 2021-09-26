var selectedGroups = []

var selectedBoards = []
var filteredBoards = []

var selectedAccounts = []
var filteredAccounts = []

var selectedSupervisors = []
var filteredSupervisors = []

var selectedPriorities = []
var filteredPriorities = []

var selectedClassifications = []
var filteredClassifications = []

var groups_select = undefined
var boards_select = undefined
var users_select = undefined
var supervisors_select = undefined

var priority_select = undefined
var classification_select = undefined


const allBoards = JSON.parse(JSON.parse(document.getElementById('boards').textContent));
const allGroups = JSON.parse(JSON.parse(document.getElementById('groups').textContent));
const allAccounts = JSON.parse(JSON.parse(document.getElementById('accounts').textContent));
const allPriorities = JSON.parse(JSON.parse(document.getElementById('priorities').textContent));
const allClassifications = JSON.parse(JSON.parse(document.getElementById('classifications').textContent));

if (ticket) {
    document.getElementById("staff_complete").checked = ticket.fields.can_staff_complete;
    selectedGroups = ticket.fields.assigned_group;
    selectedSupervisors = ticket.fields.ticket_supervisors;

    selectedBoards = ticket.fields.board;
    console.log("selectedSupervisors", selectedSupervisors);
    selectedAccounts = ticket.fields.assigned_user;
    selectedPriorities = ticket.fields.priority;
    selectedClassifications = ticket.fields.classification;
    filterPriorities(ticket.fields.priority)
    filterClassifications(ticket.fields.classification)
    // selectedGroups.push(ticket.fields.groups.all)
}
// addPriorities();

filteredAccounts = allAccounts
filteredSupervisors = allAccounts
// Initialize function, create initial tokens with itens that are already selected by the user
function init(element) {
    // Create div that wroaps all the elements inside (select, elements selected, search div) to put select inside
    const wrapper = document.createElement("div");
    wrapper.addEventListener("click", clickOnWrapper);
    wrapper.classList.add("multi-select-component");
    // const select = wrapper.querySelector("select");

    // console.log(select);
    // Create elements of search
    const search_div = document.createElement("div");
    search_div.classList.add("search-container");
    const input = document.createElement("input");
    input.classList.add("selected-input");
    input.setAttribute("autocomplete", "off");
    input.setAttribute("tabindex", "0");
    input.addEventListener("keyup", inputChange);
    input.addEventListener("keydown", deletePressed);
    input.addEventListener("click", openOptions);

    const dropdown_icon = document.createElement("a");
    dropdown_icon.setAttribute("href", "#");
    dropdown_icon.classList.add("dropdown-icon");

    dropdown_icon.addEventListener("click", clickDropdown);
    const autocomplete_list = document.createElement("ul");
    autocomplete_list.setAttribute("id", element.id);

    autocomplete_list.classList.add("autocomplete-list")
    search_div.appendChild(input);
    search_div.appendChild(autocomplete_list);
    search_div.appendChild(dropdown_icon);

    // set the wrapper as child (instead of the element)
    element.parentNode.replaceChild(wrapper, element);
    // set element as child of wrapper
    wrapper.appendChild(element);
    wrapper.appendChild(search_div);
    if (element.id == "group") {
        groups_select = element;
    } else if (element.id == "boards") {
        boards_select = element;
    } else if (element.id == "assigned-users") {
        users_select = element;
    } else if (element.id == "priority") {
        priority_select = element;
    } else if (element.id == "classification") {
        classification_select = element;
    } else if (element.id == "supervisors") {
        supervisors_select = element;
    }
    console.log("element", element);
    createInitialTokens(element);
    addPlaceholder(wrapper);
}

function removePlaceholder(wrapper) {
    const input_search = wrapper.querySelector(".selected-input");
    input_search.removeAttribute("placeholder");
}

function addPlaceholder(wrapper) {
    const input_search = wrapper.querySelector(".selected-input");
    const tokens = wrapper.querySelectorAll(".selected-wrapper");
    if (!tokens.length && !(document.activeElement === input_search))
        input_search.setAttribute("placeholder", "---------");
}


// Function that create the initial set of tokens with the options selected by the users
function createInitialTokens(select) {
    let {
        options_selected
    } = getOptions(select);
    console.log("createInitialTokens", select.id);
    console.log("createInitialTokens", options_selected);
    const wrapper = select.parentNode;

    for (let i = 0; i < options_selected.length; i++) {
        createToken(wrapper, options_selected[i], select.id);
    }

}


// Listener of user search
function inputChange(e) {
    const wrapper = e.target.parentNode.parentNode;
    const select = wrapper.querySelector("select");
    const dropdown = wrapper.querySelector(".dropdown-icon");

    const input_val = e.target.value;

    if (input_val) {
        dropdown.classList.add("active");
        populateAutocompleteList(select, input_val.trim());
    } else {
        dropdown.classList.remove("active");
        const event = new Event('click');
        dropdown.dispatchEvent(event);
    }
}


// Listen for clicks on the wrapper, if click happens focus on the input
function clickOnWrapper(e) {
    const wrapper = e.target;
    if (wrapper.tagName == "DIV") {
        const input_search = wrapper.querySelector(".selected-input");
        const dropdown = wrapper.querySelector(".dropdown-icon");
        if (!dropdown.classList.contains("active")) {
            const event = new Event('click');
            dropdown.dispatchEvent(event);
        }
        input_search.focus();
        removePlaceholder(wrapper);
    }

}

function openOptions(e) {
    const input_search = e.target;
    const wrapper = input_search.parentElement.parentElement;
    const dropdown = wrapper.querySelector(".dropdown-icon");
    if (!dropdown.classList.contains("active")) {
        const event = new Event('click');
        dropdown.dispatchEvent(event);
    }
    e.stopPropagation();

}

// Function that create a token inside of a wrapper with the given value
function createToken(wrapper, target, parent = "none") {
    const search = wrapper.querySelector(".search-container");
    // Create token wrapper
    const token = document.createElement("div");
    token.classList.add("selected-wrapper");
    const token_span = document.createElement("span");
    token_span.classList.add("selected-label");
    var id = 0;
    console.log("createToken", parent);
    if (target.dataset == undefined) {
        if (parent == "group") {
            for (let i = 0; i < allGroups.length; i++) {
                if (allGroups[i].pk == target) {
                    token_span.innerText = allGroups[i].fields.name;
                    id = allGroups[i].pk
                }
            }
        } else if (parent == "boards") {
            for (let i = 0; i < allBoards.length; i++) {

                if (allBoards[i].pk == target) {
                    token_span.innerText = allBoards[i].fields.title;
                    id = allBoards[i].pk
                }
            }
        } else if (parent == "assigned-users") {
            for (let i = 0; i < allAccounts.length; i++) {
                if (allAccounts[i].pk == target) {
                    token_span.innerText = allAccounts[i].fields.email;
                    id = allAccounts[i].pk
                }
            }
        } else if (parent == "supervisors") {
            for (let i = 0; i < allAccounts.length; i++) {
                if (allAccounts[i].pk == target) {
                    token_span.innerText = allAccounts[i].fields.email;
                    id = allAccounts[i].pk
                }
            }
        }

    } else {
        token_span.innerText = target.dataset.value;
        id = target.id;
    }


    const close = document.createElement("a");
    close.classList.add("selected-close");
    close.setAttribute("tabindex", "-1");
    close.setAttribute("data-option", target.id);
    close.setAttribute("id", id);
    close.setAttribute("data-hits", 0);
    close.setAttribute("href", "#");
    close.innerText = "x";
    close.addEventListener("click", removeToken)
    token.appendChild(token_span);
    token.appendChild(close);
    wrapper.insertBefore(token, search);
    // console.log(target.id);
    // setSelected(target);
}


function refreshBoardsAndAccounts() {

}

// Listen for clicks in the dropdown option
function clickDropdown(e) {

    const dropdown = e.target;
    const wrapper = dropdown.parentNode.parentNode;
    const input_search = wrapper.querySelector(".selected-input");
    const select = wrapper.querySelector("select");
    dropdown.classList.toggle("active");

    if (dropdown.classList.contains("active")) {
        removePlaceholder(wrapper);
        input_search.focus();

        if (!input_search.value) {
            populateAutocompleteList(select, "", true);
        } else {
            populateAutocompleteList(select, input_search.value);

        }
    } else {
        clearAutocompleteList(select);
        addPlaceholder(wrapper);
    }
}


// Clears the results of the autocomplete list
function clearAutocompleteList(select) {
    const wrapper = select.parentNode;

    const autocomplete_list = wrapper.querySelector(".autocomplete-list");
    autocomplete_list.innerHTML = "";
}

// Populate the autocomplete list following a given query from the user
function populateAutocompleteList(select, query, dropdown = false) {
    // console.log("populateAutocompleteList", select);
    const {
        autocomplete_options
    } = getOptions(select);
    console.log("options");
    console.log(autocomplete_options);
    let options_to_show;
    if (dropdown)
        options_to_show = autocomplete_options;
    else
        options_to_show = autocomplete(query, autocomplete_options);

    // console.log("population auto complete", autocomplete_options);

    const wrapper = select.parentNode;
    const input_search = wrapper.querySelector(".search-container");
    const autocomplete_list = wrapper.querySelector(".autocomplete-list");
    autocomplete_list.innerHTML = "";
    const result_size = options_to_show.length;
    // console.log(options_to_show);
    if (result_size == 1) {

        const li = document.createElement("li");
        li.innerText = options_to_show[0][0];
        li.setAttribute('data-value', options_to_show[0][0]);
        li.setAttribute('id', options_to_show[0][1]);
        li.addEventListener("click", selectOption);
        autocomplete_list.appendChild(li);
        if (query.length == options_to_show[0][0].length) {
            const event = new Event('click');
            li.dispatchEvent(event);

        }
    } else if (result_size > 1) {

        for (let i = 0; i < result_size; i++) {
            const li = document.createElement("li");
            li.innerText = options_to_show[i][0];
            li.setAttribute('data-value', options_to_show[i][0]);
            li.setAttribute('id', options_to_show[i][1]);

            li.addEventListener("click", selectOption);
            autocomplete_list.appendChild(li);
        }
    } else {
        const li = document.createElement("li");
        li.classList.add("not-cursor");
        li.innerText = "No options found";
        autocomplete_list.appendChild(li);
    }
}


// Listener to autocomplete results when clicked set the selected property in the select option 
function selectOption(e) {
    const wrapper = e.target.parentNode.parentNode.parentNode;
    const input_search = wrapper.querySelector(".selected-input");

    if (e.target.parentNode.id == "group") {
        selectedGroups.push(e.target.id);

        // for (let i = 0; i < allBoards.length; i++) {
        //     if (allBoards[i].fields.group.toString() == e.target.id) {
        //         filteredBoards.push(allBoards[i])


        //     }

        // }
        populateAutocompleteList(boards_select, "", true)
        // addPriorities()
    } else if (e.target.parentNode.id == "boards") {
        selectedBoards.push(parseInt(e.target.id));
        filterPriorities()
        filterClassifications()
    } else if (e.target.parentNode.id == "assigned-users") {
        selectedAccounts.push(e.target.id);
    } else if (e.target.parentNode.id == "supervisors") {
        selectedSupervisors.push(e.target.id);
    }
    // else if (e.target.parentNode.id == "priority") {
    //     selectedPriorities.push(e.target.id);
    // } else if (e.target.parentNode.id == "classification") {
    //     selectedClassifications.push(e.target.id);
    // }
    // populateAutocompleteList(select, "")

    // console.log(e.target.parentNode);
    createToken(wrapper, e.target);
    if (input_search.value) {
        input_search.value = "";
    }

    input_search.focus();

    e.target.remove();
    const autocomplete_list = wrapper.querySelector(".autocomplete-list");


    if (!autocomplete_list.children.length) {
        const li = document.createElement("li");
        li.classList.add("not-cursor");
        li.innerText = "No options found";
        autocomplete_list.appendChild(li);
    }

    const event = new Event('keyup');
    input_search.dispatchEvent(event);
    e.stopPropagation();
}


// function that returns a list with the autcomplete list of matches
function autocomplete(query, options) {
    // No query passed, just return entire list
    if (!query) {
        return options;
    }
    let options_return = [];
    for (let i = 0; i < options.length; i++) {
        if (options[i][0].toLowerCase().includes(query.toLowerCase())) {
            options_return.push(options[i]);
        }

    }
    return options_return;
}


// Returns the options that are selected by the user and the ones that are not
function getOptions(select) {
    // Select all the options available
    // console.log(select);
    var all_options = []
    var options_selected = []
    if (select.id == "group") {
        all_options = allGroups.map(el => [el.fields.name, el.pk.toString()])
        options_selected = selectedGroups
    } else if (select.id == "boards") {
        all_options = allBoards.map(el => [el.fields.title, el.pk.toString()])
        options_selected = selectedBoards
    } else if (select.id == "assigned-users") {
        all_options = filteredAccounts.map(el => [el.fields.email, el.pk.toString()])
        options_selected = selectedAccounts
    } else if (select.id == "supervisors") {
        all_options = filteredSupervisors.map(el => [el.fields.email, el.pk.toString()])
        options_selected = selectedSupervisors
    }

    // const options_selected = Array.from(
    //     select.querySelectorAll("option:checked")
    // ).map(el => [el.value, el.id]);
    const autocomplete_options = [];
    // console.log("all options");
    // console.log(all_options);
    // console.log("all selected");
    // console.log(options_selected);
    all_options.forEach(option => {
        if (!doesInclude(options_selected, option)) {
            autocomplete_options.push(option);
        }

    });

    autocomplete_options.sort();
    return {
        options_selected,
        autocomplete_options,
    };





}

function doesInclude(options_selected, option) {
    for (var i = 0; i < options_selected.length; i++) {
        if (options_selected[i] == option[1]) {
            return true;
        }
    }
    return false;

}

// Listener for when the user wants to remove a given token.
function removeToken(e) {
    // Get the value to remove
    const value_to_remove = e.target.dataset.option;
    const wrapper = e.target.parentNode.parentNode;
    const select = wrapper.querySelector("select");

    const input_search = wrapper.querySelector(".selected-input");
    const dropdown = wrapper.querySelector(".dropdown-icon");
    // Get the options in the select to be unselected
    const option_to_unselect = wrapper.querySelector(`select option[value="${value_to_remove}"]`);
    // option_to_unselect.removeAttribute("selected");
    // Remove token attribute

    if (select.id == "group") {

        var updatedFilteredBoards = []



        for (let i = 0; i < selectedGroups.length; i++) {
            if (selectedGroups[i] == e.target.id) {
                console.log("delete");

                // selectedGroups.splice(i, 1)
                delete selectedGroups[i];
                // updatedSelectedGroups.push(e.target.id)
            }
        }

        for (let i = 0; i < filteredBoards.length; i++) {
            if (filteredBoards[i].fields.group != e.target.id) {
                // filteredBoards.splice(i, 1)
                updatedFilteredBoards.push(filteredBoards[i])
            }
        }
        filteredBoards = updatedFilteredBoards
        populateAutocompleteList(boards_select, "", true)
    } else if (select.id == "boards") {
        for (let i = 0; i < selectedBoards.length; i++) {
            if (selectedBoards[i] == e.target.id) {
                delete selectedBoards[i];
            }
        }

        // populateAutocompleteList(boards_select, "", true)


        // for (let i = 0; i < filteredPriorities.length; i++) {
        //     if (filteredPriorities[i].fields.board.toString() == e.target.id) {
        //         // filteredBoards.splice(i, 1)
        //         updatedFilteredPriorities.push(filteredPriorities[i])
        //     }
        // }
        // filteredPriorities = updatedFilteredPriorities

        // for (let i = 0; i < filteredClassifications.length; i++) {
        //     if (filteredClassifications[i].fields.board.toString() == e.target.id) {
        //         // filteredBoards.splice(i, 1)
        //         var updatedFilteredClassifications = []
        //             .push(filteredClassifications[i])
        //     }
        // }
        // filteredClassifications = updatedFilteredClassifications
        // populateAutocompleteList(priority_select, "", true)
        // populateAutocompleteList(classification_select, "", true)

    } else if (select.id == "assigned-users") {
        for (let i = 0; i < selectedAccounts.length; i++) {
            if (selectedAccounts[i] == e.target.id) {
                delete selectedAccounts[i];
            }
        }
    } else if (select.id == "supervisors") {
        for (let i = 0; i < selectedSupervisors.length; i++) {
            if (selectedSupervisors[i] == e.target.id) {
                delete selectedSupervisors[i];
            }
        }
    }

    // else if (select.id == "priority") {
    //     for (let i = 0; i < selectedPriorities.length; i++) {
    //         if (selectedPriorities[i] == e.target.id) {
    //             delete selectedPriorities[i];
    //         }
    //     }
    // } else if (select.id == "classification") {
    //     for (let i = 0; i < selectedClassifications.length; i++) {
    //         if (selectedClassifications[i] == e.target.id) {
    //             delete selectedClassifications[i];
    //         }
    //     }
    // }


    e.target.parentNode.remove();
    input_search.focus();
    dropdown.classList.remove("active");
    const event = new Event('click');
    dropdown.dispatchEvent(event);
    e.stopPropagation();
}

// Listen for 2 sequence of hits on the delete key, if this happens delete the last token if exist
function deletePressed(e) {
    const wrapper = e.target.parentNode.parentNode;
    const input_search = e.target;
    const key = e.keyCode || e.charCode;
    const tokens = wrapper.querySelectorAll(".selected-wrapper");

    if (tokens.length) {
        const last_token_x = tokens[tokens.length - 1].querySelector("a");
        let hits = +last_token_x.dataset.hits;

        if (key == 8 || key == 46) {
            if (!input_search.value) {

                if (hits > 1) {
                    // Trigger delete event
                    const event = new Event('click');
                    last_token_x.dispatchEvent(event);
                } else {
                    last_token_x.dataset.hits = 2;
                }
            }
        } else {
            last_token_x.dataset.hits = 0;
        }
    }
    return true;
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function isEmpty(element) {
    const str = element.value
    return (!str || str.length === 0);
}
function onPostForm() {
    // window.location.replace('127.0.0.1:8000/boards');
    // let goback =

    const csrftoken = getCookie('csrftoken');
    const ticket_name = document.getElementById("ticket_name")
    const description = document.getElementById("description")
    const priority = document.getElementById("priority")
    const classification = document.getElementById("classification")
    const staff_complete = document.getElementById("staff_complete")
    const files = document.getElementById('id_file').files
    if (isEmpty(ticket_name)) {
        alert("Please enter a ticket name")
        return;
    }
    if (isEmpty(description)) {
        alert("Please enter a ticket description")
        return;
    }

    if (selectedBoards.length <= 0) {
        alert("Please select a Board")
        return;
    }

    var data = new FormData();
    data.append('ticket_name', ticket_name.value);
    data.append('description', description.value);
    console.log(classification.value);
    data.append('groups', selectedGroups);
    data.append('boards', selectedBoards);
    data.append('priority', priority.value);
    data.append('classification', classification.value);
    data.append('users', selectedAccounts);
    data.append('supervisors', selectedSupervisors);

    data.append('staff_complete', staff_complete.checked);
    for (let i = 0; i < files.length; i++) {
        data.append(`files[${i}]`, files[i], files[i].name);
    }
    // data.append('files', file);

    fetch("", {
        method: "POST",
        headers: {
            "X-CSRFTOKEN": csrftoken,
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data
    }).then(res => {
        window.location.href = res.url;
        console.log("Request complete! response:", res);
    });
}

// You can call this function if you want to add new options to the select plugin
// Target needs to be a unique identifier from the select you want to append new option for example #multi-select-plugin
// Example of usage addOption("#multi-select-plugin", "tesla", "Tesla")
function addOption(target, val, text) {
    const select = document.querySelector(target);
    let opt = document.createElement('option');
    opt.value = val;
    opt.innerHTML = text;
    select.appendChild(opt);
}

function filterPriorities(id = undefined) {
    let element = document.getElementById("priority")
    element.innerHTML = ""
    console.log("filter prio", allPriorities);
    for (let i = 0; i < allPriorities.length; i++) {
        for (let j = 0; j < selectedBoards.length; j++) {
            if (allPriorities[i].fields.board == selectedBoards[j]) {
                var opt = document.createElement('option');
                opt.value = allPriorities[i].pk;
                opt.innerHTML = allPriorities[i].fields.name;
                if (id != undefined) {
                    if (id == allPriorities[i].pk) {
                        opt.selected = true;
                    }
                }

                element.appendChild(opt);
                console.log(element);

            }
        }

    }
}

function filterClassifications(id = undefined) {
    let element = document.getElementById("classification")
    // element.innerHTML = ""
    for (let i = 0; i < allClassifications.length; i++) {
        for (let j = 0; j < selectedBoards.length; j++) {
            console.log("all classification", selectedBoards);
            if (allClassifications[i].fields.board == selectedBoards[j]) {
                var opt = document.createElement('option');
                opt.value = allClassifications[i].pk;
                opt.innerHTML = allClassifications[i].fields.name;
                if (id != undefined) {
                    if (id == allClassifications[i].pk) {
                        opt.selected = true;
                    }
                }

                element.appendChild(opt);
            }
        }

    }
}

document.addEventListener("DOMContentLoaded", () => {

    // get select that has the options available
    const select = document.querySelectorAll("[data-multi-select-plugin]");
    select.forEach(select => {

        init(select);
    });

    // const submitButton = document.getElementById("#submitform");
    // console.log(submitButton);
    // submitButton.addEventListener('click', () => {
    //     console.log("submit");
    // });

    // Dismiss on outside click
    document.addEventListener('click', () => {
        // get select that has the options available
        const select = document.querySelectorAll("[data-multi-select-plugin]");
        for (let i = 0; i < select.length; i++) {
            if (event) {
                var isClickInside = select[i].parentElement.parentElement.contains(event.target);

                if (!isClickInside) {
                    const wrapper = select[i].parentElement.parentElement;
                    const dropdown = wrapper.querySelector(".dropdown-icon");
                    const autocomplete_list = wrapper.querySelector(".autocomplete-list");
                    //the click was outside the specifiedElement, do something
                    dropdown.classList.remove("active");
                    autocomplete_list.innerHTML = "";
                    addPlaceholder(wrapper);
                }
            }
        }
    });

});


