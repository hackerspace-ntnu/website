function saveAsDraft(){
  saveArticle(true);
}

function saveAndPublish(){
  saveArticle(false);
}

function saveArticle(asDraft){

  let draftCheck = document.getElementById('id_draft');
  draftCheck.checked = asDraft;

  let saveButton = document.getElementById('submit');
  saveButton.click();

}
