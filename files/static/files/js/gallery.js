document.addEventListener('DOMContentLoaded', function() {

    // Initalize collapsibles (one per catagory)
    const collapsibles = document.querySelectorAll('.collapsible.expandable');
    M.Collapsible.init(collapsibles, {
      accordion: false
    });
});
