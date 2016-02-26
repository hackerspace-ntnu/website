/**
 * Created by martinsimensen on 26.02.2016.
 */
 function myFunction() {
    document.getElementById("my_drop_down_admin").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.drop_btn')) {

    var drop_downs = document.getElementsByClassName("drop_down_content");
    var i;
    for (i = 0; i < drop_downs.length; i++) {
      var open_drop_down = drop_downs[i];
      if (open_drop_down.classList.contains('show')) {
        open_drop_down.classList.remove('show');
      }
    }
  }
}