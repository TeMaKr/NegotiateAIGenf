/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3525142174")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_wvwqzIYcHy` ON `api_tokens` (`value`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3525142174")

  // update collection data
  unmarshal({
    "indexes": []
  }, collection)

  return app.save(collection)
})
