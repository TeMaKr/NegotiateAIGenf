/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2800040823")

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "select597064199",
    "maxSelect": 2,
    "name": "key_element",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "plastic products - national level",
      "trade"
    ]
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2800040823")

  // update field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "select597064199",
    "maxSelect": 1,
    "name": "key_element",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "plastic products - national level",
      "trade"
    ]
  }))

  return app.save(collection)
})
