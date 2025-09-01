/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // add field
  collection.fields.addAt(10, new Field({
    "hidden": false,
    "id": "select728423354",
    "maxSelect": 1,
    "name": "document_type",
    "presentable": false,
    "required": true,
    "system": false,
    "type": "select",
    "values": [
      "statement",
      "pre session submission",
      "insession document"
    ]
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // remove field
  collection.fields.removeById("select728423354")

  return app.save(collection)
})
