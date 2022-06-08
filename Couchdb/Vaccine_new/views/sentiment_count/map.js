function (doc) {
    emit([doc.sentiment,doc.text],1);
  }