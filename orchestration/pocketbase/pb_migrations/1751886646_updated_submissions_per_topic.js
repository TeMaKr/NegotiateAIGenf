/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, value as topic_id, \n       topics.name as topic_name,\n       COUNT(*) as submissions_count  \nFROM submissions, json_each(topic)\nLEFT JOIN topics ON topics.id = value\nGROUP BY value, topics.name"
  }, collection)

  // remove field
  collection.fields.removeById("json541123963")

  // remove field
  collection.fields.removeById("json2324736937")

  // remove field
  collection.fields.removeById("json2363381545")

  // remove field
  collection.fields.removeById("json1980144287")

  // remove field
  collection.fields.removeById("json1795630405")

  // remove field
  collection.fields.removeById("json190089999")

  // remove field
  collection.fields.removeById("json385153371")

  // add field
  collection.fields.addAt(2, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "_clone_4ThM",
    "max": 0,
    "min": 0,
    "name": "topic_name",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
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

  // add field
  collection.fields.addAt(2, new Field({
    "hidden": false,
    "id": "json2324736937",
    "maxSize": 1,
    "name": "key",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(3, new Field({
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
  collection.fields.addAt(4, new Field({
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
  collection.fields.addAt(5, new Field({
    "hidden": false,
    "id": "json1795630405",
    "maxSize": 1,
    "name": "json",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(6, new Field({
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
  collection.fields.addAt(7, new Field({
    "hidden": false,
    "id": "json385153371",
    "maxSize": 1,
    "name": "root",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // remove field
  collection.fields.removeById("_clone_4ThM")

  return app.save(collection)
})
