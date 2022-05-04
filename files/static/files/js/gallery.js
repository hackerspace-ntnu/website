$(() => {
    // Initialize collapsibles (one per category)
    M.Collapsible.init(
        document.querySelectorAll('.collapsible.expandable'),
        { accordion: false }
    );
});
