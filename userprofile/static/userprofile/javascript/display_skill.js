document.addEventListener('DOMContentLoaded', function() {

    // Initalize collapsibles (one per skill)
    var collapsibles = document.querySelectorAll('.collapsible.expandable');
    M.Collapsible.init(collapsibles, {
      accordion: false
    });

    // Initalize tabs (for skill categories: reachable, unreachable, acquired)
    M.Tabs.init(document.querySelectorAll('.tabs'));

    // Retrieve redirect skill id from custom attribute in script tag
    const id = document.getElementById("display_skill").getAttribute('data-redirect-to');
    if(id){
      displaySkill(id);
    }

});

function displaySkill(id){

  // Iterate both tabs for small and med/large
  for(tabsDiv of document.querySelectorAll('.tabs')){

    // Tabs controller instance
    const tabsInstance = M.Tabs.getInstance(tabsDiv);

    // Search through all tab bodies
    for(const tab of document.querySelectorAll('.tab')){

      const collapsibleDiv = document.querySelector(tab.querySelector('a').getAttribute("href"));

      const collapsible = collapsibleDiv.querySelector('.collapsible');

      if(!collapsible){
        continue;
      }

      // Collapsible controller instance
      const collapsibleInstance = M.Collapsible.getInstance(collapsible);

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
          document.getElementById(collapsibleItems[i].id).scrollIntoView();

          // Update url skill id
          window.history.replaceState(null, '', id);

        }
      }
    }
  }
}
