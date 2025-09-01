/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "createRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\"",
    "deleteRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\"",
    "updateRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\""
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "createRule": "",
    "deleteRule": "",
    "updateRule": ""
  }, collection)

  return app.save(collection)
})
