/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1609645464")

  // update collection data
  unmarshal({
    "listRule": ""
  }, collection)

  // remove field
  collection.fields.removeById("_clone_Jl92")

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_0g3C",
    "max": 0,
    "min": 0,
    "name": "draft_categories",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1609645464")

  // update collection data
  unmarshal({
    "listRule": null
  }, collection)

  // add field
  collection.fields.addAt(0, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_Jl92",
    "max": 0,
    "min": 0,
    "name": "draft_categories",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // remove field
  collection.fields.removeById("_clone_0g3C")

  return app.save(collection)
})
