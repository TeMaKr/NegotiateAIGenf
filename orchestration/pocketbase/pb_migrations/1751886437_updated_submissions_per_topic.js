/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, value as topic_id, submissions.topic, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // add field
  collection.fields.addAt(2, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2800040823",
    "hidden": false,
    "id": "_clone_pbYk",
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
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // remove field
  collection.fields.removeById("_clone_pbYk")

  return app.save(collection)
})
