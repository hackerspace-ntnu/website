function displaySkill(id){

  // Iterate both tabs for small and med/large
  for(tabsDiv of document.querySelectorAll('.tabs')){

    // Tabs controller instance
    const tabsInstance = M.Tabs.getInstance(tabsDiv);

    // Search through all tab bodies
    for(const tab of document.querySelectorAll('.tab')){

      const collapsibleDiv = document.querySelector(tab.querySelector('a').getAttribute("href"));

      // Collapsible controller instance
      const collapsibleInstance = M.Collapsible.getInstance(collapsibleDiv.querySelector('.collapsible'));

      // Collapsible items (represented by their headers)
      const collapsibleItems = collapsibleDiv.querySelectorAll('.skill-anchor');

      // Search through all tab items
      for(i = 0;i<collapsibleItems.length;i++){

        // Close this item
        collapsibleInstance.close(i);

        // Check if user is redirecting to this item
        if(collapsibleItems[i].id == 'skill' + id){

          // Switch to this tab
          tabsInstance.select(collapsibleDiv.id);

          // Open item to display skill details
          collapsibleInstance.open(i);

          // Scroll to item position
          window.location.hash = collapsibleItems[i].id;

        }
      }
    }
  }
}
