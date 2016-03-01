function cancel() {
  if ($id == 0) {
    window.location.replace("/");
  } else {
    window.location.replace("/news/article/"+$id);
  }
}
function del() {
    window.location.replace("/admin/news/article/"+$id+"/delete/");
}
function createnew() {
    window.location.replace("/news/article/0/edit");
}
