import { createPlausible } from "v-plausible/vue";

export default createPlausible({
  init: {
    domain: "negotiate-ai.com",
    trackLocalhost: false,
  },
  settings: {
    enableAutoOutboundTracking: true,
    enableAutoPageviews: true,
  },
  partytown: false,
});
