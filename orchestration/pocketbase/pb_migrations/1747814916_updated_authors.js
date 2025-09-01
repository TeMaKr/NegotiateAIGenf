/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_4091785131")

  // update collection data
  unmarshal({
    "listRule": ""
  }, collection)

  // remove field
  collection.fields.removeById("_clone_nMC1")

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_mpys",
    "max": 0,
    "min": 0,
    "name": "author",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_4091785131")

  // update collection data
  unmarshal({
    "listRule": null
  }, collection)

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_nMC1",
    "max": 0,
    "min": 0,
    "name": "author",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // remove field
  collection.fields.removeById("_clone_mpys")

  return app.save(collection)
})
