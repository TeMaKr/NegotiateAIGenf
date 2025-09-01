/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "select2765332939",
    "maxSelect": 2,
    "name": "draft_category",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "Production/Supply",
      "Plastic products & Chemicals of concern",
      "Plastic Product design"
    ]
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "select2765332939",
    "maxSelect": 2,
    "name": "draft_category",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "select",
    "values": [
      "Production/Supply",
      "Plastic products & Chemicals of concern",
      "Plastic Product design",
      "test"
    ]
  }))

  return app.save(collection)
})
