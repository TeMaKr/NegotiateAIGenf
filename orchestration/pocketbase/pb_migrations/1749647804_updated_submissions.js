/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // add field
  collection.fields.addAt(9, new Field({
    "autogeneratePattern": "[a-z0-9]{1,5}",
    "hidden": false,
    "id": "text1902483401",
    "max": 5,
    "min": 1,
    "name": "retriever_id",
    "pattern": "^[a-z0-9]{1,5}$",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // remove field
  collection.fields.removeById("text1902483401")

  return app.save(collection)
})
