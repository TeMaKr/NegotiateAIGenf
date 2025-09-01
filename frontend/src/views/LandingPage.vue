<template>
  <div class="bg-white pt-16">
    <v-container>
      <v-row class="text-center align-center justify-center mt-16">
        <v-col cols="12" md="10" lg="9" xl="8" xxl="6">
          <h1 class="fontsize-h1 mb-6">NegotiateAI</h1>
          <p
            class="mt-6 mb-2 fontsize-h6 fontsize-subtitle-1-md-and-down fontsize-subtitle-2-xs"
          >
            AI-powered insights and smart document access to
          </p>
          <p
            class="mb-8 fontsize-h6 fontsize-subtitle-1-md-and-down fontsize-subtitle-2-xs"
          >
            support the UN negotiations for a global plastics treaty.
          </p>
          <div class="mt-10" :class="{ 'd-flex flex-column': mdAndDown }">
            <v-btn
              class="mb-4"
              :class="{ 'mr-4': !mdAndDown }"
              variant="flat"
              color="primary-variant-2"
              :to="{ name: 'ChatInterface', query: { ...route.query } }"
              size="large"
              >Submissions Analyser</v-btn
            >
            <v-btn
              variant="flat"
              border="sm"
              :to="{ name: 'SubmissionsByTopic', query: { ...route.query } }"
              class="mb-4"
              :class="{ 'mr-4': !mdAndDown }"
              color="primary"
              size="large"
              >Advanced Analyser
            </v-btn>

            <v-btn
              v-if="mdAndDown"
              variant="flat"
              border="sm"
              :to="{ name: 'DocumentList', query: { ...route.query } }"
              color="secondary"
              class="mb-4"
              :class="{ 'mr-4': !mdAndDown }"
              size="large"
              >Submissions Browser</v-btn
            >
            <v-btn
              v-if="mdAndDown"
              variant="flat"
              color="primary-variant"
              border="sm"
              :to="{ name: 'DraftTreatyExplorer', query: { ...route.query } }"
              class="mb-4"
              size="large"
              >Draft Treaty Explorer</v-btn
            >
          </div>

          <p id="ai-disclaimer" class="fontsize-subtitle-2">
            AI disclaimer:
            <span class="text-medium-emphasis"
              >This tool uses AI to generate responses based on publicly
              available negotiation documents. While we strive for accuracy and
              transparency, answers may occasionally be incomplete or
              inaccurate. If in doubt, please check the original sources. See
              our
              <a
                class="text-medium-emphasis text-decoration-underline"
                text="technical documentation"
                href="/documentation"
                target="_blank"
                rel="noreferrer"
              />
              for more information.</span
            >
          </p>
        </v-col>
      </v-row>
    </v-container>
    <div class="py-0">
      <v-img
        class="hidden-sm-and-up"
        cover
        src="../assets/Hero-Section-Graphic-Mobile.png"
        alt="Hero section mobile"
      ></v-img>
      <v-img
        class="hidden-xs hidden-lg-and-up"
        cover
        src="../assets/Hero-Section-Graphic-Tablet.png"
        alt="Hero section tablet"
      ></v-img>
      <v-img
        class="hidden-md-and-down"
        cover
        src="../assets/Hero-Section-Image-Desktop.png"
        alt="Hero section desktop"
      ></v-img>
    </div>
  </div>
  <!-- About Section -->
  <v-container class="section-spacing-top large-section-spacing-bottom">
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="9" xl="8" xxl="6">
        <v-row>
          <v-col>
            <h2 class="fontsize-h2 pt-3">About</h2>
            <p class="landing-page-text-block">
              NegotiateAI is designed to streamline access to key information on
              the UN Plastic Treaty Negotiations to develop a legally binding
              instrument on plastic pollution, including the marine environment.
              The app offers a centralised, comprehensive database of documents
              submitted by Delegations and Groups of States, available on the
              official
              <a
                href="https://www.unep.org/inc-plastic-pollution"
                target="_blank"
                class="text-primary"
                rel="noopener noreferrer"
                >Intergovernmental Negotiating Committee on Plastic Pollution</a
              >
              website, along with a suite of interactive tools to support
              analysis and engagement. With powerful search and smart analysis
              features, NegotiateAI helps users quickly
              <strong>(1) find relevant content, (2) compare positions</strong>,
              and
              <strong
                >(3) identify key themes across the draft treaty text</strong
              >. Whether you are a delegate, an observer or a researcher, the
              app is designed to help you stay oriented in the complexity of the
              negotiations and engage more effectively with the evolving
              process. For more information on the NegotiateAI development,
              please visit the
              <a
                href="https://www.blog-datalab.com/home/negotiateai/"
                target="_blank"
                class="text-primary"
                >GIZ Data Lab Blog</a
              >.
            </p>
          </v-col>
        </v-row>

        <v-row class="mt-16">
          <v-col cols="12">
            <v-icon
              icon="mdi-message-question"
              color="primary"
              size="x-large"
              cover
            ></v-icon>
            <h3 class="fontsize-h4 pt-3">Submissions Analyser</h3>
          </v-col>
          <v-col v-if="!mdAndDown" cols="12" md="6" class="pr-14">
            <p class="landing-page-text-block pt-0 mt-0">
              The Submissions Analyser simplifies the
              <strong>search and analysis</strong> of documents submitted by
              Delegations and Groups of States, enabling delegates and other
              stakeholders to quickly identify crucial information. With an
              intuitive interface, the tool supports
              <strong>treaty-specific queries</strong> and provides
              <strong>direct links to relevant submissions</strong> for in-depth
              research. Users can enter general or highly specific questions via
              a free-text field, and use filters to narrow their search by topic
              or country.
            </p>
            <v-btn
              class="mt-6"
              color="primary"
              text
              :to="{ name: 'ChatInterface', query: { ...route.query } }"
              >Start Now</v-btn
            >
          </v-col>

          <v-col v-if="!mdAndDown" cols="12" md="6">
            <v-img
              to="chat-interface"
              alt="A depiction of the submissions querier"
              cover
              src="../assets/Submission-Analyser.png"
            ></v-img>
          </v-col>

          <!-- Mobile/Tablet Layout -->
          <v-col v-if="mdAndDown" cols="12">
            <v-img
              to="chat-interface"
              alt="A depiction of the submissions querier"
              cover
              src="../assets/Submission-Analyser.png"
              class="my-4"
            ></v-img>
            <p class="landing-page-text-block">
              The Submissions Analyser simplifies the
              <strong>search and analysis</strong> of documents submitted by
              Delegations and Groups of States, enabling delegates and other
              stakeholders to quickly identify crucial information. With an
              intuitive interface, the tool supports
              <strong>treaty-specific queries</strong> and provides
              <strong>direct links to relevant submissions</strong> for in-depth
              research. Users can enter general or highly specific questions via
              a free-text field, and use filters to narrow their search by topic
              or country.
            </p>
            <v-btn
              class="mt-6"
              color="primary"
              text
              :to="{ name: 'ChatInterface', query: { ...route.query } }"
              >Start Now</v-btn
            >
          </v-col>
        </v-row>

        <v-row class="mt-16 mb-16">
          <v-col cols="12" md="6" class="hidden-md-and-down"></v-col>
          <v-col cols="12" md="6">
            <v-icon
              icon="mdi-table-search"
              color="secondary-variant"
              size="x-large"
            ></v-icon>
            <h3 class="fontsize-h4 pt-3">Advanced Analyser</h3>
          </v-col>
          <v-col v-if="!mdAndDown" cols="12" md="6" class="pr-8">
            <v-img
              to="chat-interface"
              alt="A depiction of the submissions analyser"
              src="../assets/Advanced-Analyser.png"
            ></v-img>
          </v-col>

          <v-col v-if="!mdAndDown" cols="12" md="6">
            <p class="landing-page-text-block mt-0 pt-0">
              Advanced Analyser provides a structured way to
              <strong>explore and compare submissions</strong> from INC-5.1 and
              INC-5.2. Submissions are officially assigned to articles or
              thematic areas currently under negotiation, such as waste
              management or product design. To support deeper analysis, each
              topic has been further broken down into manually defined
              <strong>Key Elements</strong> – analytical categories that
              highlight specific aspects within a topic. For further exploration
              of these topics and Key Elements, the
              <router-link
                :to="{ name: 'DraftTreatyExplorer', query: { ...route.query } }"
                class="text-primary"
              >
                <span>Draft Treaty Explorer</span>
              </router-link>
              provides detailed insights into the topics' structure and
              development of the treaty articles in various draft versions. The
              analytical structure of the Key Elements helps users compare
              Delegations/Groups of States positions more easily and engage with
              the content at a more detailed level. The tool allows users to
              filter submissions by session, topic, and Delegations or Groups of
              States, and then compare up to three selected Key Elements side by
              side. To support deeper understanding, the tool also generates
              <strong>concise AI-powered summaries</strong> that highlight the
              main arguments, positions, and divergences across submissions. The
              feature is designed to make it easier to grasp the evolving
              negotiation landscape at a glance.
            </p>
            <v-btn
              class="mt-3"
              color="primary"
              text
              :to="{ name: 'SubmissionsByTopic', query: { ...route.query } }"
              >Start Now</v-btn
            >
          </v-col>

          <!-- Mobile/Tablet Layout -->
          <v-col v-if="mdAndDown" cols="12">
            <v-img
              to="chat-interface"
              alt="A depiction of the submissions analyser"
              src="../assets/Advanced-Analyser.png"
              class="my-4"
            ></v-img>
            <p class="landing-page-text-block">
              Advanced Analyser provides a structured way to
              <strong>explore and compare submissions</strong> from INC-5.1 and
              INC-5.2. Submissions are officially assigned to articles or
              thematic areas currently under negotiation, such as waste
              management or product design. To support deeper analysis, each
              topic has been further broken down into manually defined
              <strong>Key Elements</strong> – analytical categories that
              highlight specific aspects within a topic. For further exploration
              of these topics and Key Elements, the
              <router-link
                :to="{ name: 'DraftTreatyExplorer', query: { ...route.query } }"
                class="text-primary"
              >
                <span>Draft Treaty Explorer</span>
              </router-link>
              provides detailed insights into the topics' structure and
              development of the treaty articles in various draft versions. The
              analytical structure of the Key Elements helps users compare
              Delegations/Groups of States positions more easily and engage with
              the content at a more detailed level. The tool allows users to
              filter submissions by session, topic, and Delegations or Groups of
              States, and then compare up to three selected Key Elements side by
              side. To support deeper understanding, the tool also generates
              <strong>concise AI-powered summaries</strong> that highlight the
              main arguments, positions, and divergences across submissions. The
              feature is designed to make it easier to grasp the evolving
              negotiation landscape at a glance.
            </p>
            <v-btn
              class="mt-3"
              color="primary"
              text
              :to="{ name: 'SubmissionsByTopic', query: { ...route.query } }"
              >Start Now</v-btn
            >
          </v-col>
        </v-row>

        <!-- Data Section -->
        <div class="section-spacing-top">
          <v-icon
            icon="mdi-file-search-outline"
            color="secondary-variant"
            size="x-large"
          ></v-icon>
          <h3 class="fontsize-h3 pt-3">What about Data?</h3>
          <v-row class="mb-12">
            <v-col cols="12" md="6" :class="{ 'pr-14': !mdAndDown }">
              <h4 class="fontsize-h5 pt-6">Submissions Analyser Data</h4>
              <p class="landing-page-text-block">
                The dataset comprises official documents from the INC
                (Intergovernmental Negotiating Committee on Plastic Pollution),
                encompassing all submissions by INC members, written statements
                and in-session documents from individual Delegations and Groups
                of States across all sessions conducted to date. Observer
                documents are excluded from this collection. The
                <router-link
                  :to="{ name: 'ChatInterface', query: { ...route.query } }"
                  class="text-primary"
                >
                  <span>Submissions Analyser</span>
                </router-link>
                is specifically configured to analyse in-session documents,
                whilst the complete dataset is accessible through our
                <router-link
                  :to="{ name: 'DocumentList', query: { ...route.query } }"
                  class="text-primary"
                >
                  <span>Submissions Browser</span> </router-link
                >.
              </p>

              <p>
                We continually update the dataset as new submissions become
                available. Whilst there may be a delay when new submissions are
                received, verified documents from ongoing rounds are added once
                manually reviewed by our team. The current status can always be
                checked in our
                <router-link
                  :to="{ name: 'DocumentList', query: { ...route.query } }"
                  class="text-primary"
                >
                  <span>Submissions Browser</span>
                </router-link>
              </p>
            </v-col>
            <v-col cols="12" md="6">
              <h4 class="fontsize-h5 pt-6">Advanced Analyser Data</h4>
              <p class="landing-page-text-block">
                This feature draws upon official INC submissions from Sessions
                5.1 and 5.2, specifically analysing in-session submissions from
                these negotiation rounds. Submissions are officially assigned to
                articles or thematic areas currently under negotiation, such as
                waste management or product design. Each topic has been further
                broken down into manually defined Key Elements – analytical
                categories that highlight specific aspects within a topic.
              </p>
              <p class="landing-page-text-block">
                For this tool, submissions have been processed to extract
                relevant passages based on the Key Elements. The system
                automatically performs this extraction process for all new
                documents added to the database. Users can access the complete
                extraction data through our
                <router-link
                  :to="{
                    name: 'SubmissionsByTopic',
                    query: { ...route.query },
                  }"
                  class="text-primary"
                >
                  <span>Advanced Analyser</span> </router-link
                >. Please note that this is an AI-based extraction process and
                may occasionally contain inaccuracies.
              </p>
            </v-col>
          </v-row>
        </div>

        <!-- Technical Approach Section -->
        <div class="section-spacing-top">
          <v-icon
            icon="mdi-developer-board"
            color="secondary-variant"
            size="x-large"
          ></v-icon>
          <h3 class="fontsize-h3 pt-3">What's our Technological Approach</h3>
          <v-row class="pb-14" align="center">
            <v-col>
              <p class="landing-page-text-block">
                The generative component of both applications is based on
                <strong>Retrieval Augmented Generation (RAG)</strong> to combine
                search-based methods with generative AI models. Whilst
                search-based models can find relevant information from text,
                they cannot provide comprehensive answers in natural language.
                Conversely, whilst generative models can produce answers in
                natural language, these can be inaccurate without context. RAG
                addresses these limitations by leveraging the strengths of both
                approaches whilst minimising their weaknesses. With RAG, filters
                can first be applied to narrow down the documents. Relevant
                passages from the (filtered) documents are then identified using
                a machine learning model based on natural language input. The
                identified context is then sent to a generative AI model (in our
                case <strong>OpenAI GPT-4</strong>) together with the original
                input.
              </p>
              <p class="landing-page-text-block">
                <strong>Limitations</strong>: As part of our transparency
                efforts, we acknowledge certain limitations of our current
                system. Without appropriate filters, there may be less accurate
                responses. Additionally, like all generative AI systems, our
                tool may occasionally produce inaccurate information. Due to
                processing capacity constraints, not all documents can be
                considered simultaneously for each query, which may limit the
                comprehensiveness of responses. These limitations are inherent
                to current generative AI technology and affect similar systems
                across the field.
              </p>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="10" xl="8" class="mx-auto">
              <v-img
                src="../assets/technical-approach.png"
                max-width="100%"
                contain
              >
              </v-img>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </v-container>

  <div class="bg-white">
    <!-- Vision Section -->
    <v-container class="large-section-spacing-top">
      <v-row class="justify-center">
        <v-col cols="12" lg="9" xl="8" xxl="6">
          <v-row>
            <v-col cols="12">
              <h2 class="fontsize-h2">Our Vision</h2>
            </v-col>
            <v-col :class="{ 'pr-14': !mdAndDown }">
              <p class="landing-page-text-block mt-0 pt-0">
                The initial NegotiateAI prototype has already shown strong
                potential to improve negotiation processes and has laid the
                foundation for broader adoption. Building on this, our current
                focus is on delivering
                <strong>precise, evidence-based analyses</strong> of treaty
                submissions. Our goal is to help Delegations navigate the
                growing volume of unstructured information through
                <strong>targeted, efficient, and in-depth analysis</strong>. The
                latest features help users navigate and understand the
                submissions more effectively –
                <strong
                  >enabling more informed comparisons across Delegations/Groups
                  of States and topics</strong
                >, and providing insights into the negotiation process that are
                more accessible than ever.
              </p>

              <p class="landing-page-text-block">
                Looking ahead, our role beyond the INC negotiation process
                remains open: whether by continuously refining the app to
                increase transparency and trace the evolution of the draft
                treaty text, or by developing new tools to help countries align
                treaty obligations with their national legal systems. As the
                final scope of the treaty is still undecided, so too is the
                exact direction of our future involvement. But one thing is
                certain: we are committed to
                <strong>developing relevant, practical tools</strong> that
                continue to support implementation even once a treaty is in
                place and has been ratified.
              </p>
              <p class="landing-page-text-block">
                Collaboration and feedback from users and partners are essential
                as we refine the tool for its next iteration and beyond. Our
                priority is to make the app as valuable and helpful as possible
                for the target group by tailoring features to their specific
                needs and addressing real-world challenges they face. If you
                have any feedback, please reach out to us at
                <a class="text-primary" href="mailto:datalab@giz.de"
                  >datalab@giz.de</a
                >
              </p>
            </v-col>
            <v-col cols="12" md="6">
              <v-img
                src="../assets/Vision-Section-Image.png"
                :cover="mdAndDown"
                max-height="553"
              ></v-img>
            </v-col>
          </v-row>

          <!-- Why This Matters Section -->
          <div class="section-spacing-top">
            <v-icon
              icon="mdi-flag-outline"
              color="secondary-variant"
              size="x-large"
            ></v-icon>
            <h3 class="fontsize-h3 pt-3">Why This Matters</h3>
            <v-row align="center">
              <v-col>
                <p class="landing-page-text-block">
                  The United Nations has embarked on a monumental task:
                  negotiating a legally binding agreement to tackle the global
                  plastic pollution crisis. The goal is to establish a robust
                  framework that ends plastic pollution and promotes sustainable
                  production and consumption of plastic worldwide.
                </p>
                <p class="landing-page-text-block">
                  Representatives from <strong>around 180 countries</strong> are
                  involved in this extensive process. The resolution to
                  elaborate such a legally binding instrument was adopted in
                  March 2022 at the
                  <strong>UN Environment Assembly (UNEA-5.2)</strong> in
                  Nairobi. Between 2022 and 2024,
                  <strong>five negotiation rounds</strong> took place. While the
                  fifth session (INC-5) in Busan, Republic of Korea, was
                  intended to be the final round, it ended without agreement on
                  a treaty text – leaving key issues unresolved and the treaty
                  still under negotiation. As a result, the process was
                  adjourned and the urgently needed continuation of talks has
                  now been scheduled for
                  <strong>INC-5.2, taking place in Geneva in August 2025</strong
                  >. This upcoming session will be critical to bridging
                  remaining gaps and paving the way towards a final agreement.
                </p>
                <p class="landing-page-text-block">
                  The urgent need for a treaty arises from the
                  <strong
                    >estimated 4.8 to 12.7 million tonnes of plastic entering
                    oceans yearly</strong
                  >
                  and predictions of global plastic waste production nearly
                  <strong>tripling by 2060 compared to 2019</strong> without
                  intervention, as an OECD study predicts. Plastic production,
                  heavily reliant on fossil fuels and toxic additives, threatens
                  both the environment and human health.
                </p>
              </v-col>
            </v-row>
          </div>

          <!-- Did You Know Section -->
          <div class="section-spacing-top">
            <v-icon
              icon="mdi-information-outline"
              color="secondary-variant"
              size="x-large"
            ></v-icon>
            <h3 class="fontsize-h3 pt-3">Did you know?</h3>
            <v-row class="mt-4">
              <v-col>
                <v-slide-group>
                  <v-slide-group-item
                    v-for="(fact, index) in facts"
                    :key="index"
                  >
                    <v-card
                      width="322"
                      class="mr-4 py-6"
                      :color="fact.background"
                    >
                      <div class="px-6">
                        <v-img
                          class="mb-4"
                          height="85px"
                          :src="fact.image"
                          :alt="fact.imageAlt"
                          width="85px"
                        />
                        <p class="text-uppercase my-4 font-weight-bold text-h6">
                          {{ fact.title }}
                        </p>
                        <p>{{ fact.description }}</p>
                      </div>
                    </v-card>
                  </v-slide-group-item>
                </v-slide-group>
              </v-col>
            </v-row>
          </div>

          <!-- About Us Section -->
          <div class="section-spacing-top">
            <v-icon
              icon="mdi-account-group"
              color="secondary-variant"
              size="x-large"
            ></v-icon>
            <h3 class="fontsize-h3 pt-3">About Us</h3>
            <v-row align="center">
              <v-col>
                <p class="landing-page-text-block">
                  At GIZ Data Lab, we combine expertise in data science with a
                  clear focus on sustainability and data for development. As a
                  digital innovation hub within GIZ, we experiment with
                  <strong
                    >data-driven solutions to tackle complex global
                    challenges.</strong
                  >
                  With NegotiateAI, we empower negotiators and stakeholders in
                  international negotiations by providing deep, actionable
                  insights from negotiation texts and data, which can be
                  especially helpful for smaller Delegations with limited
                  resources to participate more effectively. Our goal is to make
                  the complex negotiation process more transparent, efficient,
                  and inclusive.
                  <strong
                    >We believe that better data means better decisions for our
                    planet’s future</strong
                  >. Join us on the journey to unlock the power of data insights
                  for meaningful cooperative action. NegotiateAI was developed
                  in close
                  <strong>collaboration with the global sector project</strong>
                  that supports the German Federal Ministry for the Environment,
                  Climate Action, Nature Conservation and Nuclear Safety (BMUKN)
                  on the topic of marine litter prevention and management. The
                  sector project provides BMUKN with on-demand advisory services
                  related to the INC process and pilots innovative approaches
                  for tackling plastic pollution in GIZ’s partner countries.
                </p>
              </v-col>
            </v-row>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <div class="py-0">
      <v-img
        class="hidden-sm-and-up"
        src="../assets/Footer-Section-Graphic-Mobile.png"
        alt="Footer section mobile"
      >
      </v-img>
      <v-img
        class="hidden-xs hidden-lg-and-up"
        src="../assets/Footer-Section-Graphic-Tablet.png"
        alt="Footer section tablet"
      >
      </v-img>
      <v-img
        class="hidden-md-and-down"
        src="../assets/Footer-Section-Image-Desktop.png"
        alt="Footer section desktop"
      ></v-img>
    </div>
  </div>
</template>

<script setup lang="ts">
import plasticBottle from "../assets/Plastic_Bottle.svg";
import turtle from "../assets/Turtle.svg";
import foodPackaging from "../assets/Food_Packaging.svg";
import cigarettes from "../assets/Cigaretts.svg";
import { useDisplay } from "vuetify";
import { useRoute } from "vue-router";

const { xs, mdAndDown } = useDisplay();
const route = useRoute();

const facts = [
  {
    title: "Historic Global Treaty",
    description:
      "In March 2022, the UN Environment Assembly adopted a groundbreaking resolution to create the world's first legally binding treaty on plastic pollution. The Intergovernmental Negotiating Committee has conducted negotiations across four continents, with the final session scheduled for Geneva in August 2025.",
    image: plasticBottle,
    imageAlt: "Plastic bottle illustration",
    background: "primary",
  },
  {
    title: "Submission Volume",
    description:
      "The negotiation process has generated over 1900 official submissions from INC members throughout all sessions to date.",
    image: foodPackaging,
    imageAlt: "Food packaging illustration",
    background: "secondary",
  },
  {
    title: "Global Participation",
    description:
      "About 185 delegations from across the globe have actively engaged in these negotiations with individual submissions, representing unprecedented international involvement.",
    image: turtle,
    imageAlt: "Sea turtle illustration",
    background: "primary-variant",
  },
  {
    title: "Draft Treaty Evolution",
    description:
      "The transition from the Compilation Text (Session 4) to the Chair's Text (Session 5.1)  resulted in a substantial reduction in the number of pages and brackets within the draft treaty. Explore this development further through our Draft Treaty Evolution feature.",
    image: cigarettes,
    imageAlt: "Cigarette waste illustration",
    background: "secondary-variant",
  },
];
</script>

<style scoped>
.landing-page-text-block {
  text-align: justify;
  padding-top: 0px;
  padding-bottom: 16px;
  color: rgba(var(--v-theme-on-background), 0.8);
}

@media (min-width: 1264px) {
  .landing-page-text-block {
    padding-top: 24px;
    padding-bottom: 12px;
  }
}

.section-spacing-top {
  margin-top: 80px;
}

.large-section-spacing-top {
  padding-top: 80px;
}

.large-section-spacing-bottom {
  padding-bottom: 80px;
}

@media (min-width: 600px) {
  .section-spacing-top {
    margin-top: 120px;
  }

  .large-section-spacing-top {
    padding-top: 240px;
  }

  .large-section-spacing-bottom {
    padding-bottom: 240px;
  }
}

#ai-disclaimer {
  padding: 10px 0;
  font-weight: 400;
  letter-spacing: 0.1px;
  color: rgb(var(--v-theme-on-background));
}

.fontsize-h1 {
  color: rgb(var(--v-theme-primary-variant-2));
}
</style>

.highlight-text{ text-primary weight: bold }
