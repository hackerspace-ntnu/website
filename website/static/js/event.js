function cancel() {
  if ($id == 0) {
    window.location.replace("/");
  } else {
    window.location.replace("/news/event/"+$id);
  }
}
function del() {
    window.location.replace("/admin/news/event/"+$id+"/delete/");
}
function createnew() {
    window.location.replace("/news/event/0/edit");
}
