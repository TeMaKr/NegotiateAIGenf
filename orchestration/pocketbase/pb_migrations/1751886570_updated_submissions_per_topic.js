/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, key, type, fullkey, json, path, root, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // add field
  collection.fields.addAt(5, new Field({
    "hidden": false,
    "id": "json190089999",
    "maxSize": 1,
    "name": "path",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(6, new Field({
    "hidden": false,
    "id": "json385153371",
    "maxSize": 1,
    "name": "root",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, key, type, fullkey, json, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // remove field
  collection.fields.removeById("json190089999")

  // remove field
  collection.fields.removeById("json385153371")

  return app.save(collection)
})
