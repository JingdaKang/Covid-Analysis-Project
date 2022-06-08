function (doc) {
    emit([doc.SA3_NAME16,doc.sentiments,doc.text],1);
  }