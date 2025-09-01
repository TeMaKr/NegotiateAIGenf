/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { IncDocumentIn } from "../models/IncDocumentIn";
import type { IncDocumentOut } from "../models/IncDocumentOut";
import type { SynchronizationSubmissionsOut } from "../models/SynchronizationSubmissionsOut";
import type { SynchronizeSubmissionsIn } from "../models/SynchronizeSubmissionsIn";
import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";
export class SubmissionsService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}
  /**
   * Synchronize Submissions
   * Spawn a background task to synchronize the submissions with the UNEP Website from session 5.2.
   * @param requestBody
   * @param xApiToken
   * @returns SynchronizationSubmissionsOut Successful Response
   * @throws ApiError
   */
  public synchronizeSubmissionsApiSynchronizeSubmissionPost(
    requestBody: SynchronizeSubmissionsIn,
    xApiToken?: string | null,
  ): CancelablePromise<SynchronizationSubmissionsOut> {
    return this.httpRequest.request({
      method: "POST",
      url: "/api/synchronize-submission",
      headers: {
        "X-API-Token": xApiToken,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Inc Document
   * Endpoint to process and upsert a document into the 'inc' vector store.
   * @param requestBody
   * @param xApiToken
   * @returns IncDocumentOut Successful Response
   * @throws ApiError
   */
  public incDocumentApiProcessSubmissionPost(
    requestBody: IncDocumentIn,
    xApiToken?: string | null,
  ): CancelablePromise<IncDocumentOut> {
    return this.httpRequest.request({
      method: "POST",
      url: "/api/process-submission",
      headers: {
        "X-API-Token": xApiToken,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
