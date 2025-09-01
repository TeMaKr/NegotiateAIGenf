/**
 * This file was @generated using pocketbase-typegen
 */

import type PocketBase from "pocketbase";
import type { RecordService } from "pocketbase";

export enum Collections {
  Authorigins = "_authOrigins",
  Externalauths = "_externalAuths",
  Mfas = "_mfas",
  Otps = "_otps",
  Superusers = "_superusers",
  ApiTokens = "api_tokens",
  Authors = "authors",
  Submissions = "submissions",
  SubmissionsPerSession = "submissions_per_session",
  SubmissionsPerTopic = "submissions_per_topic",
  Topics = "topics",
  Users = "users",
}

// Alias types for improved usability
export type IsoDateString = string;
export type RecordIdString = string;
export type HTMLString = string;

export type GeoPoint = {
  lon: number;
  lat: number;
};

type ExpandType<T> = unknown extends T
  ? T extends unknown
    ? { expand?: unknown }
    : { expand: T }
  : { expand: T };

// System fields
export type BaseSystemFields<T = unknown> = {
  id: RecordIdString;
  collectionId: string;
  collectionName: Collections;
} & ExpandType<T>;

export type AuthSystemFields<T = unknown> = {
  email: string;
  emailVisibility: boolean;
  username: string;
  verified: boolean;
} & BaseSystemFields<T>;

// Record types for each collection

export type AuthoriginsRecord = {
  collectionRef: string;
  created?: IsoDateString;
  fingerprint: string;
  id: string;
  recordRef: string;
  updated?: IsoDateString;
};

export type ExternalauthsRecord = {
  collectionRef: string;
  created?: IsoDateString;
  id: string;
  provider: string;
  providerId: string;
  recordRef: string;
  updated?: IsoDateString;
};

export type MfasRecord = {
  collectionRef: string;
  created?: IsoDateString;
  id: string;
  method: string;
  recordRef: string;
  updated?: IsoDateString;
};

export type OtpsRecord = {
  collectionRef: string;
  created?: IsoDateString;
  id: string;
  password: string;
  recordRef: string;
  sentTo?: string;
  updated?: IsoDateString;
};

export type SuperusersRecord = {
  created?: IsoDateString;
  email: string;
  emailVisibility?: boolean;
  id: string;
  password: string;
  tokenKey: string;
  updated?: IsoDateString;
  verified?: boolean;
};

export type ApiTokensRecord = {
  created?: IsoDateString;
  id: string;
  updated?: IsoDateString;
  value?: string;
};

export type AuthorsRecord = {
  created?: IsoDateString;
  geometry?: GeoPoint;
  id: string;
  name?: string;
  type?: string;
  updated?: IsoDateString;
};

export enum SubmissionsSessionOptions {
  "E1" = "1",
  "E2" = "2",
  "E3" = "3",
  "E4" = "4",
  "E5.1" = "5.1",
  "E5.2" = "5.2",
}

export enum SubmissionsDocumentTypeOptions {
  "statement" = "statement",
  "pre session submission" = "pre session submission",
  "insession document" = "insession document",
}
export type SubmissionsRecord<Tkey_element = unknown> = {
  author?: RecordIdString[];
  created?: IsoDateString;
  description?: string;
  document_type: SubmissionsDocumentTypeOptions;
  file?: string;
  href?: string;
  id: string;
  key_element?: null | Tkey_element;
  retriever_id?: string;
  session?: SubmissionsSessionOptions;
  title?: string;
  topic?: RecordIdString[];
  updated?: IsoDateString;
  verified?: boolean;
};

export enum SubmissionsPerSessionSessionOptions {
  "E1" = "1",
  "E2" = "2",
  "E3" = "3",
  "E4" = "4",
  "E5.1" = "5.1",
  "E5.2" = "5.2",
}
export type SubmissionsPerSessionRecord = {
  id: string;
  session?: SubmissionsPerSessionSessionOptions;
  submissions_count?: number;
};

export type SubmissionsPerTopicRecord<Ttopic_id = unknown> = {
  id: string;
  submissions_count?: number;
  topic_id?: null | Ttopic_id;
  topic_name?: string;
};

export enum TopicsKeyElementOptions {
  "objectives - life cycle approach" = "objectives - life cycle approach",
  "objectives - protection of health and environment" = "objectives - protection of health and environment",
  "objective - plastic pollution" = "objective - plastic pollution",
  "objective - marine environment" = "objective - marine environment",
  "principles - rio declaration" = "principles - rio declaration",
  "principles - right to development and equity" = "principles - right to development and equity",
  "principles - common but differentiated responsibility" = "principles - common but differentiated responsibility",
  "principles - state sovereignty and international cooperation" = "principles - state sovereignty and international cooperation",
  "principles - precautionary and polluter-pays principles" = "principles - precautionary and polluter-pays principles",
  "principles - support for developing countries" = "principles - support for developing countries",
  "principles - use of best available science, indigenous and traditional knowledge" = "principles - use of best available science, indigenous and traditional knowledge",
  "party" = "party",
  "plastic" = "plastic",
  "plastic pollution" = "plastic pollution",
  "plastic product" = "plastic product",
  "plastic waste" = "plastic waste",
  "regional economic integration organization" = "regional economic integration organization",
  "plastic products - national level" = "plastic products - national level",
  "Plastic products criteria" = "Plastic products criteria",
  "products - measures" = "products - measures",
  "products - monitoring" = "products - monitoring",
  "products - global measures" = "products - global measures",
  "products - submission of proposal" = "products - submission of proposal",
  "products - information need" = "products - information need",
  "products - subsidiary body or review committee" = "products - subsidiary body or review committee",
  "products - review committee" = "products - review committee",
  "products - guidance" = "products - guidance",
  "products - conference of the parties" = "products - conference of the parties",
  "products - trade" = "products - trade",
  "products - list of products" = "products - list of products",
  "chemicals - measures" = "chemicals - measures",
  "chemicals - traceability" = "chemicals - traceability",
  "chemicals - list" = "chemicals - list",
  "chemicals - criteria" = "chemicals - criteria",
  "chemicals - risk management" = "chemicals - risk management",
  "chemicals - plans" = "chemicals - plans",
  "chemicals - report" = "chemicals - report",
  "chemicals - submissions" = "chemicals - submissions",
  "chemicals - information may be as annex/criteria" = "chemicals - information may be as annex/criteria",
  "chemicals - process" = "chemicals - process",
  "chemicals - technical and scientific committee" = "chemicals - technical and scientific committee",
  "chemicals - conference of the parties" = "chemicals - conference of the parties",
  "chemicals - dip con" = "chemicals - dip con",
  "chemicals - annex list of chemicals" = "chemicals - annex list of chemicals",
  "chemicals - annex risk management" = "chemicals - annex risk management",
  "registration and justification of exemptions" = "registration and justification of exemptions",
  "phase-out dates" = "phase-out dates",
  "statement of need" = "statement of need",
  "public registry and transparency" = "public registry and transparency",
  "duration and expiry" = "duration and expiry",
  "extension process and criteria" = "extension process and criteria",
  "availability of alternatives" = "availability of alternatives",
  "withdrawal and reapplication" = "withdrawal and reapplication",
  "product design - design criteria" = "product design - design criteria",
  "product design - circular economy principles" = "product design - circular economy principles",
  "product design - sustainable alternatives and innovation" = "product design - sustainable alternatives and innovation",
  "sectoral guidance development" = "sectoral guidance development",
  "non-discrimination clause trade" = "non-discrimination clause trade",
  "alignment with international standards" = "alignment with international standards",
  "global production target" = "global production target",
  "lifecycle management measures" = "lifecycle management measures",
  "data reporting obligations" = "data reporting obligations",
  "reporting format and guidance" = "reporting format and guidance",
  "review mechanism for target adjustment" = "review mechanism for target adjustment",
  "prevent plastic releases and leakages" = "prevent plastic releases and leakages",
  "prevent plastic pellets release and leakages" = "prevent plastic pellets release and leakages",
  "manage fishing gear pollution" = "manage fishing gear pollution",
  "research and monitoring – leakage pathways" = "research and monitoring – leakage pathways",
  "promote best available technologies and practices" = "promote best available technologies and practices",
  "guidance by conference of parties (cop)" = "guidance by conference of parties (cop)",
  "consider national circumstances" = "consider national circumstances",
  "ensure environmentally sound management (esm)" = "ensure environmentally sound management (esm)",
  "infrastructure development" = "infrastructure development",
  "promote circular economy approaches" = "promote circular economy approaches",
  "prevent littering, open dumping/burning, ocean dumping" = "prevent littering, open dumping/burning, ocean dumping",
  "fishing gear waste" = "fishing gear waste",
  "set national collection and recycling targets" = "set national collection and recycling targets",
  "just transition - waste sector" = "just transition - waste sector",
  "behavior change and awareness" = "behavior change and awareness",
  "transboundary movement controls" = "transboundary movement controls",
  "promote extended producer responsibility" = "promote extended producer responsibility",
  "support implementation by conference of parties (cop)" = "support implementation by conference of parties (cop)",
  "identify and monitor plastic pollution hotspots" = "identify and monitor plastic pollution hotspots",
  "pollution removal and cleanup" = "pollution removal and cleanup",
  "use of science and local knowledge" = "use of science and local knowledge",
  "stakeholder engagement and knowledge exchange" = "stakeholder engagement and knowledge exchange",
  "just transition - general principles and considering national context" = "just transition - general principles and considering national context",
  "just transition - affected groups and workes" = "just transition - affected groups and workes",
  "just transition - monitoring and reporting of transition measures" = "just transition - monitoring and reporting of transition measures",
  "provision of financial support" = "provision of financial support",
  "conditions for support - prioritization and needs" = "conditions for support - prioritization and needs",
  "structure and operation of the mechanism" = "structure and operation of the mechanism",
  "funding sources and replenishment" = "funding sources and replenishment",
  "funding uses - eligible activities" = "funding uses - eligible activities",
  "capacity building and technical assistance" = "capacity building and technical assistance",
  "technology transfer - terms and delivery" = "technology transfer - terms and delivery",
  "international cooperation and coordination" = "international cooperation and coordination",
  "establish compliance & implementation committee" = "establish compliance & implementation committee",
  "committee procedures and reporting" = "committee procedures and reporting",
  "national implementation plans" = "national implementation plans",
  "stakeholder engagement in planning" = "stakeholder engagement in planning",
  "review and update of national plans" = "review and update of national plans",
  "national reporting obligations" = "national reporting obligations",
  "report format and timeline" = "report format and timeline",
  "public access and transparency" = "public access and transparency",
  "evaluation of convention effectiveness" = "evaluation of convention effectiveness",
  "basis for evaluation" = "basis for evaluation",
  "modalities of evaluation process" = "modalities of evaluation process",
  "exchange of best practices and policy knowledge" = "exchange of best practices and policy knowledge",
  "sharing scientific, traditional and indigenous knowledge" = "sharing scientific, traditional and indigenous knowledge",
  "information on risks and impacts of plastic pollution" = "information on risks and impacts of plastic pollution",
  "national focal points for information coordination" = "national focal points for information coordination",
  "online clearinghouse managed by the secretariat" = "online clearinghouse managed by the secretariat",
  "use of existing platforms and networks" = "use of existing platforms and networks",
  "research, technologies and innovation exchange" = "research, technologies and innovation exchange",
  "protection of confidential information" = "protection of confidential information",
  "public awareness and environmental education" = "public awareness and environmental education",
  "access to information and knowledge" = "access to information and knowledge",
  "scientific research and data monitoring" = "scientific research and data monitoring",
  "inclusion of traditional and local knowledge" = "inclusion of traditional and local knowledge",
  "standardized monitoring methods and approaches" = "standardized monitoring methods and approaches",
  "capacity-building and multi-level training" = "capacity-building and multi-level training",
  "human health considerations" = "human health considerations",
  "conference of the parties – mandate and governance functions of the cop" = "conference of the parties – mandate and governance functions of the cop",
  "conference of the parties – rules of procedure and decision-making at cop meetings" = "conference of the parties – rules of procedure and decision-making at cop meetings",
  "conference of the parties – frequency and modalities of cop sessions" = "conference of the parties – frequency and modalities of cop sessions",
  "conference of the parties – authority to establish subsidiary bodies" = "conference of the parties – authority to establish subsidiary bodies",
  "conference of the parties – engagement with international and non-state actors" = "conference of the parties – engagement with international and non-state actors",
  "conference of the parties – observer participation and objection rules" = "conference of the parties – observer participation and objection rules",
  "establishment of scientific and technical subsidiary bodies" = "establishment of scientific and technical subsidiary bodies",
  "committees, panels, tors and working arrangements" = "committees, panels, tors and working arrangements",
  "secretariat – functions and mandate" = "secretariat – functions and mandate",
  "support for conference of the parties meetings and parties" = "support for conference of the parties meetings and parties",
  "reporting and documentation duties" = "reporting and documentation duties",
  "coordination with other international bodies" = "coordination with other international bodies",
  "hosting and institutional arrangements" = "hosting and institutional arrangements",
  "unep executive director as default secretariat" = "unep executive director as default secretariat",
  "cooperation and peaceful settlement of disputes" = "cooperation and peaceful settlement of disputes",
  "declaration of compulsory arbitration and icj jurisdiction by parties" = "declaration of compulsory arbitration and icj jurisdiction by parties",
  "declarations by regional economic integration organizations" = "declarations by regional economic integration organizations",
  "duration and revocation of declarations" = "duration and revocation of declarations",
  "effect of expiry or revocation on ongoing proceedings" = "effect of expiry or revocation on ongoing proceedings",
  "conciliation procedures by conference of the parties" = "conciliation procedures by conference of the parties",
  "procedure for amending the convention" = "procedure for amending the convention",
  "timeline and entry into force for amendments" = "timeline and entry into force for amendments",
  "role of the depositary in amendment communication" = "role of the depositary in amendment communication",
  "annexes as integral part of the convention" = "annexes as integral part of the convention",
  "scope of annexes limited to procedural and technical matters" = "scope of annexes limited to procedural and technical matters",
  "procedure for adoption and non-acceptance of new annexes" = "procedure for adoption and non-acceptance of new annexes",
  "amendment of annexes follows same procedure as adoption" = "amendment of annexes follows same procedure as adoption",
  "special provisions for parties with declarations (art. 27)" = "special provisions for parties with declarations (art. 27)",
  "voting rights of parties and organizations" = "voting rights of parties and organizations",
  "opening of the convention for signature" = "opening of the convention for signature",
  "locations and timeframe for signing the convention" = "locations and timeframe for signing the convention",
  "ratification, acceptance, approval, and accession" = "ratification, acceptance, approval, and accession",
  "obligations of regional economic integration organizations" = "obligations of regional economic integration organizations",
  "declaration of competence" = "declaration of competence",
  "conditional entry into force of additional annexes and amendments" = "conditional entry into force of additional annexes and amendments",
  "conditions for entry into force of the convention" = "conditions for entry into force of the convention",
  "entry into force for later ratifiers" = "entry into force for later ratifiers",
  "reservations - no reservations allowed" = "reservations - no reservations allowed",
  "withdrawal – possible after three years" = "withdrawal – possible after three years",
  "withdrawal – takes effect one year after notification" = "withdrawal – takes effect one year after notification",
  "depositary – un secretary-general" = "depositary – un secretary-general",
  "authentic texts – equal authenticity of six official un languages" = "authentic texts – equal authenticity of six official un languages",
}
export type TopicsRecord = {
  article?: string;
  child?: RecordIdString[];
  created?: IsoDateString;
  id: string;
  key_element?: TopicsKeyElementOptions[];
  name?: string;
  updated?: IsoDateString;
};

export type UsersRecord = {
  created?: IsoDateString;
  email: string;
  emailVisibility?: boolean;
  first_name: string;
  id: string;
  last_name: string;
  password: string;
  tokenKey: string;
  updated?: IsoDateString;
  verified?: boolean;
};

// Response types include system fields and match responses from the PocketBase API
export type AuthoriginsResponse<Texpand = unknown> =
  Required<AuthoriginsRecord> & BaseSystemFields<Texpand>;
export type ExternalauthsResponse<Texpand = unknown> =
  Required<ExternalauthsRecord> & BaseSystemFields<Texpand>;
export type MfasResponse<Texpand = unknown> = Required<MfasRecord> &
  BaseSystemFields<Texpand>;
export type OtpsResponse<Texpand = unknown> = Required<OtpsRecord> &
  BaseSystemFields<Texpand>;
export type SuperusersResponse<Texpand = unknown> = Required<SuperusersRecord> &
  AuthSystemFields<Texpand>;
export type ApiTokensResponse<Texpand = unknown> = Required<ApiTokensRecord> &
  BaseSystemFields<Texpand>;
export type AuthorsResponse<Texpand = unknown> = Required<AuthorsRecord> &
  BaseSystemFields<Texpand>;
export type SubmissionsResponse<
  Tkey_element = unknown,
  Texpand = unknown,
> = Required<SubmissionsRecord<Tkey_element>> & BaseSystemFields<Texpand>;
export type SubmissionsPerSessionResponse<Texpand = unknown> =
  Required<SubmissionsPerSessionRecord> & BaseSystemFields<Texpand>;
export type SubmissionsPerTopicResponse<
  Ttopic_id = unknown,
  Texpand = unknown,
> = Required<SubmissionsPerTopicRecord<Ttopic_id>> & BaseSystemFields<Texpand>;
export type TopicsResponse<Texpand = unknown> = Required<TopicsRecord> &
  BaseSystemFields<Texpand>;
export type UsersResponse<Texpand = unknown> = Required<UsersRecord> &
  AuthSystemFields<Texpand>;

// Types containing all Records and Responses, useful for creating typing helper functions

export type CollectionRecords = {
  _authOrigins: AuthoriginsRecord;
  _externalAuths: ExternalauthsRecord;
  _mfas: MfasRecord;
  _otps: OtpsRecord;
  _superusers: SuperusersRecord;
  api_tokens: ApiTokensRecord;
  authors: AuthorsRecord;
  submissions: SubmissionsRecord;
  submissions_per_session: SubmissionsPerSessionRecord;
  submissions_per_topic: SubmissionsPerTopicRecord;
  topics: TopicsRecord;
  users: UsersRecord;
};

export type CollectionResponses = {
  _authOrigins: AuthoriginsResponse;
  _externalAuths: ExternalauthsResponse;
  _mfas: MfasResponse;
  _otps: OtpsResponse;
  _superusers: SuperusersResponse;
  api_tokens: ApiTokensResponse;
  authors: AuthorsResponse;
  submissions: SubmissionsResponse;
  submissions_per_session: SubmissionsPerSessionResponse;
  submissions_per_topic: SubmissionsPerTopicResponse;
  topics: TopicsResponse;
  users: UsersResponse;
};

// Type for usage with type asserted PocketBase instance
// https://github.com/pocketbase/js-sdk#specify-typescript-definitions

export type TypedPocketBase = PocketBase & {
  collection(idOrName: "_authOrigins"): RecordService<AuthoriginsResponse>;
  collection(idOrName: "_externalAuths"): RecordService<ExternalauthsResponse>;
  collection(idOrName: "_mfas"): RecordService<MfasResponse>;
  collection(idOrName: "_otps"): RecordService<OtpsResponse>;
  collection(idOrName: "_superusers"): RecordService<SuperusersResponse>;
  collection(idOrName: "api_tokens"): RecordService<ApiTokensResponse>;
  collection(idOrName: "authors"): RecordService<AuthorsResponse>;
  collection(idOrName: "submissions"): RecordService<SubmissionsResponse>;
  collection(
    idOrName: "submissions_per_session",
  ): RecordService<SubmissionsPerSessionResponse>;
  collection(
    idOrName: "submissions_per_topic",
  ): RecordService<SubmissionsPerTopicResponse>;
  collection(idOrName: "topics"): RecordService<TopicsResponse>;
  collection(idOrName: "users"): RecordService<UsersResponse>;
};
