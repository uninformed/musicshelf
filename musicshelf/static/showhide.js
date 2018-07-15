function hideAllBut(target) {
  // find all fieldsets
  let fieldsets = document.getElementsByTagName("fieldset");
  for (var i=0; i<fieldsets.length; i++) {
    // enable the fieldset with given id
    if (fieldsets[i].id == target) {
      fieldsets[i].disabled = false;
    }
    // disable the rest
    else {
      fieldsets[i].disabled = true;
    }
  }
}
