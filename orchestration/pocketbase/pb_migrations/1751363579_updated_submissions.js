/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // add field
  collection.fields.addAt(11, new Field({
    "hidden": false,
    "id": "select1083226839",
    "maxSelect": 1,
    "name": "enrichment_state",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "Active",
      "Suceeded",
      "Failed"
    ]
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // remove field
  collection.fields.removeById("select1083226839")

  return app.save(collection)
})
