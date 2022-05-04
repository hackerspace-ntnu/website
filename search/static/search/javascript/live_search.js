const searchResults = document.getElementById("search-results");

// Perform search on page load
document.addEventListener('DOMContentLoaded', function () {
    updateList();
});

// Listen for keystroke events
let timeout = null;
const searchField = document.getElementById("search-input");
searchField.addEventListener('keyup', () => {
    // Clear the timeout if it has already been set.
    // This will prevent the previous task from executing
    // if user is still typing
    clearTimeout(timeout);

    // Make a new timeout for updating search
    timeout = setTimeout(function () {
        updateSearch(searchField.value)
    }, 100);
});

function updateSearch(s) {
    search = s;
    pageNumber = 1;
    updateList();
}

function updatePageNumber(p) {
    pageNumber = p;
    updateList();
}

function updateList() {
    let url;
    if (!search) {
        url = '/search';
        searchResults.innerHTML = ""
    } else {
        url = `/search/?q=${search}&p=${pageNumber}`;

        // Refresh list content from api
        fetch(`/api${url}`, {
            type: 'GET',
        }).then((data) => {
            data.text().then((content) => {
                searchResults.innerHTML = content;
            });
        })
    }
    // Update url to allow direct links to search
    const state = window.history.state;
    const title = window.document.title;
    window.history.pushState(state, title, url);
}
