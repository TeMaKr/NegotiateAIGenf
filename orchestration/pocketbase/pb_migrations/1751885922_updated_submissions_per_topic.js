/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT s.id, s.title, s.topic FROM submissions as s, json_each(topic) as topic_value"
  }, collection)

  // remove field
  collection.fields.removeById("_clone_MxjV")

  // add field
  collection.fields.addAt(1, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_RDQE",
    "max": 0,
    "min": 0,
    "name": "title",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(2, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2800040823",
    "hidden": false,
    "id": "_clone_9A2k",
    "maxSelect": 999,
    "minSelect": 0,
    "name": "topic",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT s.id, s.title FROM submissions as s, json_each(topic) as topic_value"
  }, collection)

  // add field
  collection.fields.addAt(1, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_MxjV",
    "max": 0,
    "min": 0,
    "name": "title",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // remove field
  collection.fields.removeById("_clone_RDQE")

  // remove field
  collection.fields.removeById("_clone_9A2k")

  return app.save(collection)
})
