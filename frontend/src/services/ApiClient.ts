/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from "./core/BaseHttpRequest";
import type { OpenAPIConfig } from "./core/OpenAPI";
import { AxiosHttpRequest } from "./core/AxiosHttpRequest";
import { AiToolsService } from "./services/AiToolsService";
import { DefaultService } from "./services/DefaultService";
import { SubmissionsService } from "./services/SubmissionsService";
type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;
export class ApiClient {
  public readonly aiTools: AiToolsService;
  public readonly default: DefaultService;
  public readonly submissions: SubmissionsService;
  public readonly request: BaseHttpRequest;
  constructor(
    config?: Partial<OpenAPIConfig>,
    HttpRequest: HttpRequestConstructor = AxiosHttpRequest,
  ) {
    this.request = new HttpRequest({
      BASE: config?.BASE ?? "",
      VERSION: config?.VERSION ?? "0.1.0",
      WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
      CREDENTIALS: config?.CREDENTIALS ?? "include",
      TOKEN: config?.TOKEN,
      USERNAME: config?.USERNAME,
      PASSWORD: config?.PASSWORD,
      HEADERS: config?.HEADERS,
      ENCODE_PATH: config?.ENCODE_PATH,
    });
    this.aiTools = new AiToolsService(this.request);
    this.default = new DefaultService(this.request);
    this.submissions = new SubmissionsService(this.request);
  }
}
