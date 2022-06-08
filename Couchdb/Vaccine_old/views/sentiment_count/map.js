function (doc) {
  emit([doc.sentiments,doc.text],1);
}