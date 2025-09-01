/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, key, type, fullkey, json, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // add field
  collection.fields.addAt(2, new Field({
    "hidden": false,
    "id": "json2363381545",
    "maxSize": 1,
    "name": "type",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(3, new Field({
    "hidden": false,
    "id": "json1980144287",
    "maxSize": 1,
    "name": "fullkey",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "json1795630405",
    "maxSize": 1,
    "name": "json",
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
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, key, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // remove field
  collection.fields.removeById("json2363381545")

  // remove field
  collection.fields.removeById("json1980144287")

  // remove field
  collection.fields.removeById("json1795630405")

  return app.save(collection)
})
