/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, count(*) as submissions_count, session FROM submissions group by session"
  }, collection)

  // remove field
  collection.fields.removeById("_clone_0JW1")

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "number1073325736",
    "max": null,
    "min": null,
    "name": "submissions_count",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

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

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, session FROM submissions group by session"
  }, collection)

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

  // remove field
  collection.fields.removeById("number1073325736")

  // remove field
  collection.fields.removeById("_clone_kqtb")

  return app.save(collection)
})
