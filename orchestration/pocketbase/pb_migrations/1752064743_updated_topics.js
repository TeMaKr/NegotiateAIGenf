/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2800040823")

  // update collection data
  unmarshal({
    "createRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\"",
    "deleteRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\"",
    "updateRule": "@collection.api_tokens.value ?= @request.headers.x_api_token || @request.auth.id != \"\""
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2800040823")

  // update collection data
  unmarshal({
    "createRule": "@request.headers.x_api_token = @collection.api_tokens.value || @request.auth.id != \"\" ",
    "deleteRule": "@request.headers.x_api_token = @collection.api_tokens.value || @request.auth.id != \"\" ",
    "updateRule": "@request.headers.x_api_token = @collection.api_tokens.value || @request.auth.id != \"\" "
  }, collection)

  return app.save(collection)
})
