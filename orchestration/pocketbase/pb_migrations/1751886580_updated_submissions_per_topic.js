/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, atom, key, type, fullkey, json, path, root, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "json541123963",
    "maxSize": 1,
    "name": "atom",
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
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, key, type, fullkey, json, path, root, value as topic_id, COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nGROUP BY value"
  }, collection)

  // remove field
  collection.fields.removeById("json541123963")

  return app.save(collection)
})
