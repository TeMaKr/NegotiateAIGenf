import axios from "axios";
import { ApiClient } from "../services/ApiClient";

axios.defaults.xsrfHeaderName = "x-csrf-token";
axios.defaults.xsrfCookieName = "csrf_token";
axios.defaults.withXSRFToken = true;
axios.defaults.baseURL =
  import.meta.env.VITE_FAST_API_BASE_URL ?? "http://localhost:8000";
axios.defaults.withCredentials = true;

export default new ApiClient({
  WITH_CREDENTIALS: true,
});

export { axios };
