/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, json_extract(value, '$') as topic_id, COUNT(*) as submissions_count\nFROM submissions, json_each(submissions.topic)\nGROUP BY topic"
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883")

  // update collection data
  unmarshal({
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, json_extract(value, '$') as topic_id, COUNT(*) as submissions_count\nFROM submissions, json_each(submissions.topic)\nGROUP BY topic_id"
  }, collection)

  return app.save(collection)
})
