/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906")

  // update collection data
  unmarshal({
    "name": "submissions_per_session"
  }, collection)

  // remove field
  collection.fields.removeById("_clone_1ilU")

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "_clone_0JW1",
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
    "name": "topics_per_session"
  }, collection)

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "_clone_1ilU",
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
  collection.fields.removeById("_clone_0JW1")

  return app.save(collection)
})
