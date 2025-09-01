/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { QuerySubmissionIn } from "../models/QuerySubmissionIn";
import type { QuerySubmissionOut } from "../models/QuerySubmissionOut";
import type { SummaryKeyElementIn } from "../models/SummaryKeyElementIn";
import type { SummaryKeyElementOut } from "../models/SummaryKeyElementOut";
import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";
export class AiToolsService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}
  /**
   * Query Submission
   * @param requestBody
   * @returns QuerySubmissionOut Successful Response
   * @throws ApiError
   */
  public querySubmissionApiQuerySubmissionPost(
    requestBody: QuerySubmissionIn,
  ): CancelablePromise<QuerySubmissionOut> {
    return this.httpRequest.request({
      method: "POST",
      url: "/api/query-submission",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Summarize Key Element
   * @param requestBody
   * @returns SummaryKeyElementOut Successful Response
   * @throws ApiError
   */
  public summarizeKeyElementApiSummarizeKeyElementPost(
    requestBody: SummaryKeyElementIn,
  ): CancelablePromise<SummaryKeyElementOut> {
    return this.httpRequest.request({
      method: "POST",
      url: "/api/summarize-key-element",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
