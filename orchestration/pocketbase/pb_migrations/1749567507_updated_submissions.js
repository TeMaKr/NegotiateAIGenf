/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update field
  collection.fields.addAt(7, new Field({
    "hidden": false,
    "id": "file1542800728",
    "maxSelect": 1,
    "maxSize": 0,
    "mimeTypes": [],
    "name": "file",
    "presentable": false,
    "protected": false,
    "required": false,
    "system": false,
    "thumbs": [],
    "type": "file"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update field
  collection.fields.addAt(7, new Field({
    "hidden": false,
    "id": "file1542800728",
    "maxSelect": 1,
    "maxSize": 0,
    "mimeTypes": [],
    "name": "field",
    "presentable": false,
    "protected": false,
    "required": false,
    "system": false,
    "thumbs": [],
    "type": "file"
  }))

  return app.save(collection)
})
