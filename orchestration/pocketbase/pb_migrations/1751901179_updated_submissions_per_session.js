/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906")

  // update collection data
  unmarshal({
    "listRule": "",
    "viewRule": ""
  }, collection)

  // remove field
  collection.fields.removeById("_clone_kqtb")

  // add field
  collection.fields.addAt(2, new Field({
    "hidden": false,
    "id": "_clone_C00D",
    "maxSelect": 1,
    "name": "session",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "1",
      "2",
      "3",
      "4",
      "5.1",
      "5.2"
    ]
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906")

  // update collection data
  unmarshal({
    "listRule": null,
    "viewRule": null
  }, collection)

  // add field
  collection.fields.addAt(2, new Field({
    "hidden": false,
    "id": "_clone_kqtb",
    "maxSelect": 1,
    "name": "session",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "1",
      "2",
      "3",
      "4",
      "5.1",
      "5.2"
    ]
  }))

  // remove field
  collection.fields.removeById("_clone_C00D")

  return app.save(collection)
})
