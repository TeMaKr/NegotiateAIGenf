/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3346360724")

  // update collection data
  unmarshal({
    "listRule": ""
  }, collection)

  // remove field
  collection.fields.removeById("_clone_1Bog")

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_W1o8",
    "max": 0,
    "min": 0,
    "name": "session",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3346360724")

  // update collection data
  unmarshal({
    "listRule": null
  }, collection)

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_1Bog",
    "max": 0,
    "min": 0,
    "name": "session",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // remove field
  collection.fields.removeById("_clone_W1o8")

  return app.save(collection)
})
