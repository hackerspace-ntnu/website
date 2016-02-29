function edit() {
    document.getElementById("edit").style.display="list-item";
    document.getElementById("content").style.display="none";
    document.getElementById("cancelBtn").style.display="list-item";
    document.getElementById("editBtn").style.display="none";
}
function cancel() {
    location.reload();
}
function del() {
    var url = window.location.href;
    var id = url.substr(url.length-3, url.length-2);
    window.location.replace("/admin/news/article"+id+"delete/");
}
function createnew() {
    window.location.replace("/admin/news/article/add/");
}
