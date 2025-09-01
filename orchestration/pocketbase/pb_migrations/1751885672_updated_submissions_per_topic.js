/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id FROM submissions, json_each(topic) as topic_value"
  }, collection)

  // remove field
  collection.fields.removeById("number1073325736")

  // remove field
  collection.fields.removeById("_clone_44D3")

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, count(*) as submissions_count, topic FROM submissions group by topic"
  }, collection)

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
    "cascadeDelete": false,
    "collectionId": "pbc_2800040823",
    "hidden": false,
    "id": "_clone_44D3",
    "maxSelect": 999,
    "minSelect": 0,
    "name": "topic",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  return app.save(collection)
})
