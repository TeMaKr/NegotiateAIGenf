<template>
  <v-row class="bg-white">
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto">
      <v-container class="pa-8">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="fontsize-h2 mt-12 mb-12 underlined-header">
            Technical Documentation according to the EU AI Act
          </h1>
          <h2 class="text-h5 mb-4">Application Name: NegotiateAI</h2>

          <div class="mb-4">
            <p>
              <strong>Provider / Supplier:</strong><br />
              GIZ (Deutsche Gesellschaft für International Zusammenarbeit) Data
              Lab<br />
              datalab@giz.de<br />
              Friedrich-Ebert-Alle 32+36<br />
              53113 Bonn
            </p>
          </div>

          <div class="mb-4">
            <p>
              <strong>Deployment:</strong><br />
              Website:
              <a href="https://negotiate-ai.com" target="_blank"
                >https://negotiate-ai.com</a
              ><br />
              Hosting Provider: Hetzner Online GmbH<br />
              Server Location: Nuremberg, Germany
            </p>
          </div>

          <div class="mb-4">
            <p>
              <strong>Development:</strong><br />
              &effect data solutions GmbH<br />
              Pasteurstr. 34<br />
              10407 Berlin
            </p>
          </div>

          <p><strong>Last updated:</strong> 26.07.2025</p>
        </div>

        <!-- Table of Contents -->
        <v-card class="mb-8" outlined>
          <v-card-title class="text-h5">Table of Contents</v-card-title>
          <v-card-text>
            <ol class="toc-list">
              <li>
                <a href="#system-overview" @click="scrollTo('system-overview')"
                  >System Overview</a
                >
                <ol>
                  <li>
                    <a href="#purpose" @click="scrollTo('purpose')"
                      >Purpose and Intended Use</a
                    >
                  </li>
                  <li>
                    <a
                      href="#risk-classification"
                      @click="scrollTo('risk-classification')"
                      >Risk Classification</a
                    >
                  </li>
                  <li>
                    <a
                      href="#system-description"
                      @click="scrollTo('system-description')"
                      >Description of the System</a
                    >
                  </li>
                  <li>
                    <a href="#use-cases" @click="scrollTo('use-cases')"
                      >Intended Use Cases</a
                    >
                  </li>
                </ol>
              </li>
              <li>
                <a href="#ai-components" @click="scrollTo('ai-components')"
                  >AI Components</a
                >
                <ol>
                  <li>
                    <a href="#ai-features" @click="scrollTo('ai-features')"
                      >AI Features</a
                    >
                  </li>
                  <li>
                    <a href="#models-used" @click="scrollTo('models-used')"
                      >Models Used</a
                    >
                  </li>
                  <li>
                    <a href="#training-data" @click="scrollTo('training-data')"
                      >Model Training Data</a
                    >
                  </li>
                  <li>
                    <a
                      href="#technical-limitations"
                      @click="scrollTo('technical-limitations')"
                      >Technical Limitations</a
                    >
                  </li>
                  <li>
                    <a
                      href="#system-limitations"
                      @click="scrollTo('system-limitations')"
                      >System Limitations and Non-Purposes</a
                    >
                  </li>
                </ol>
              </li>
              <li>
                <a href="#data-management" @click="scrollTo('data-management')"
                  >Data Management</a
                >
                <ol>
                  <li>
                    <a href="#databases" @click="scrollTo('databases')"
                      >Databases</a
                    >
                  </li>
                  <li>
                    <a href="#data-sources" @click="scrollTo('data-sources')"
                      >Data Sources and Processing</a
                    >
                  </li>
                  <li>
                    <a
                      href="#data-protection"
                      @click="scrollTo('data-protection')"
                      >Data Protection and Privacy Measures</a
                    >
                  </li>
                </ol>
              </li>
              <li>
                <a href="#transparency" @click="scrollTo('transparency')"
                  >Transparency towards User</a
                >
              </li>
              <li>
                <a href="#monitoring" @click="scrollTo('monitoring')"
                  >Monitoring, Feedback, and Incident Reporting</a
                >
              </li>
              <li>
                <a href="#publication" @click="scrollTo('publication')"
                  >Publication Status</a
                >
              </li>
              <li>
                <a href="#contact" @click="scrollTo('contact')">Contact</a>
              </li>
            </ol>
          </v-card-text>
        </v-card>

        <!-- Content Sections -->
        <div id="system-overview" class="mb-8">
          <h2 class="text-h4 mb-4">1. System Overview</h2>

          <div id="purpose" class="mb-6">
            <h3 class="text-h5 mb-3">1.1 Purpose and Intended Use</h3>
            <p class="mb-4">
              NegotiateAI offers functionality to analyse documents (statements
              and submissions) submitted during plastic treaty negotiations by
              the Intergovernmental Negotiating Committee (INC), part of the
              United Nations Environment Programme (UNEP). AI models are used to
              retrieve documents based on natural-language queries (Retrieval),
              create summaries and extract information.
            </p>

            <p class="mb-3"><strong>Core Functions:</strong></p>
            <ul class="mb-4">
              <li>
                Submission Analyser: Question and answering with AI capabilities
              </li>
              <li>
                Advanced Analyser: Analysis tool with AI-generated data and AI
                summary function
              </li>
              <li>
                Submission Browser: Document library with advanced filtering and
                search
              </li>
              <li>
                Draft Treaty Explorer: Visualisation of treaty evolution across
                negotiation sessions and Topics
              </li>
            </ul>

            <p>
              <strong>Intended Users:</strong> The application is primarily
              intended for use by delegations and observers of the negotiations
              but is also accessible to researchers and the public.
            </p>
          </div>

          <div id="risk-classification" class="mb-6">
            <h3 class="text-h5 mb-3">1.2 Risk Classification</h3>
            <p class="mb-4">
              NegotiateAI is classified as a
              <strong>Limited Risk AI System</strong> under Article 50 of the EU
              AI Act.
            </p>

            <p class="mb-4">
              <strong>Rationale:</strong> The system generates AI content that
              users interact with directly (responses, summaries, document
              analysis) and requires transparency obligations to ensure users
              understand when content is AI-generated.
            </p>

            <p class="mb-3"><strong>Risk Mitigation:</strong></p>
            <ul>
              <li>Clear AI content labeling through interface badges</li>
              <li>Comprehensive user guidance on system limitations</li>
              <li>Public technical documentation</li>
              <li>
                Explicit disclaimers that outputs require verification against
                original sources
              </li>
            </ul>
          </div>

          <div id="system-description" class="mb-6">
            <h3 class="text-h5 mb-3">1.3 Description of the System</h3>
            <p class="mb-4">
              The system utilizes Retrieval Augmented Generation (RAG)
              architecture, combining semantic search capabilities with
              generative AI responses. The application employs OpenAI GPT-4 for
              natural language generation and response synthesis, whilst
              sentence transformer models enable semantic search for document
              retrieval and similarity matching. AI-powered text analysis and
              content extraction facilitate the processing of complex treaty
              documents.
            </p>

            <p class="mb-3"><strong>AI Components:</strong></p>
            <ul class="mb-4">
              <li>Language Model: OpenAI GPT-4</li>
              <li>
                Semantic Search Model:
                sentence-transformers/distiluse-base-multilingual-cased-v1
              </li>
              <li>AI Framework: Langchain</li>
            </ul>

            <p class="mb-3"><strong>Further Components:</strong></p>
            <ul>
              <li>Web Framework: Vue.js</li>
              <li>Database: SQLite</li>
              <li>Backend Frameworks: FastAPI & Pocketbase</li>
              <li>Vector Database: Qdrant</li>
            </ul>
          </div>

          <div id="use-cases" class="mb-6">
            <h3 class="text-h5 mb-3">1.4 Intended Use Cases</h3>
            <ul>
              <li>
                Browse, access and explore official documents from treaty
                negotiations
              </li>
              <li>
                Analysis of documents and delegation/group of state positions
              </li>
              <li>
                Comparative research of positions across different parties
              </li>
              <li>
                Analysis and tracking of development of negotiation draft treaty
              </li>
              <li>
                Public access to transparent information about treaty
                negotiations
              </li>
            </ul>
          </div>
        </div>

        <div id="ai-components" class="mb-8">
          <h2 class="text-h4 mb-4">2. AI Components</h2>

          <div id="ai-features" class="mb-6">
            <h3 class="text-h5 mb-3">2.1 AI Features</h3>

            <p class="mb-3"><strong>Submission Analyser:</strong></p>
            <p class="mb-4">
              The system processes natural language queries about submitted
              documents, searches for relevant texts using sentence
              transformers, and generates context-sensitive responses using
              OpenAI GPT-4 with the user input and a predefined prompt. Users
              can ask questions about specific submissions, delegation
              positions, or contract topics and receive AI-generated responses
              with direct references to source documents. The implementation is
              based on RAG architecture.
            </p>

            <p class="mb-3"><strong>Key Element Extraction:</strong></p>
            <p class="mb-4">
              The system extracts text passages from submissions based on
              so-called Key Elements (terms that conceptually reflect the topics
              of the negotiations). The extraction is performed on a prompt
              basis using OpenAI GPT-4. The extractions are made available to
              users for reading in the Advanced Analyser feature. Users cannot
              generate their own extractions. The corresponding API is protected
              by token-based authentication.
            </p>

            <p class="mb-3"><strong>AI Summary Generation:</strong></p>
            <p>
              The system creates comparative summaries based on the text
              fragments extracted from the Key Element Extraction component.
              Users can select up to three generated document excerpts for the
              same key element. The summary is created based on the user's
              selection and a predefined prompt.
            </p>
          </div>

          <div id="models-used" class="mb-6">
            <h3 class="text-h5 mb-3">2.2 Models Used</h3>

            <v-data-table
              :headers="modelHeaders"
              :items="modelData"
              class="elevation-1 mb-4"
              density="comfortable"
            >
              <template v-slot:item.source="{ item }">
                <a v-if="item.source" :href="item.source" target="_blank">{{
                  item.sourceText
                }}</a>
                <span v-else>{{ item.sourceText }}</span>
              </template>
            </v-data-table>
          </div>

          <div id="training-data" class="mb-6">
            <h3 class="text-h5 mb-3">2.3 Model Training Data</h3>
            <p class="mb-4">
              NegotiateAI did not train or optimise any AI components other than
              through custom system prompts.
            </p>

            <p class="mb-4">
              <strong>GPT-4:</strong> GPT-4 was trained by OpenAI. The training
              data is publicly documented by the provider (see OpenAI
              documentation).
            </p>

            <p>
              <strong
                >sentence-transformers/distiluse-base-multilingual-cased-v1:</strong
              >
              This model was trained by the Sentence Transformers team based on
              the DistilBERT architecture. The model was fine-tuned using
              publicly available datasets for multilingual sentence similarity
              tasks. The training data and methodology are documented in the
              Sentence Transformers documentation.
            </p>
          </div>

          <div id="technical-limitations" class="mb-6">
            <h3 class="text-h5 mb-3">2.4 Technical Limitations</h3>
            <p class="mb-4">
              Due to model capacity constraints, not all documents can be
              processed simultaneously. Response accuracy depends upon
              appropriate use of filtering options to narrow the document scope.
              As with any AI system, errors may occur during content generation,
              and users should verify information against original sources.
            </p>

            <p class="mb-3">
              <strong>Submission Analyser:</strong> Despite employing RAG
              architecture to ground responses in source documents, AI-generated
              answers may occasionally contain hallucinations or inaccuracies.
            </p>

            <p class="mb-3">
              <strong>Key Element Extraction:</strong> The automated extraction
              process is AI-based and may produce content that is not verbatim
              from the original submissions. Extracted passages may be
              paraphrased or interpreted rather than direct quotations.
            </p>

            <p>
              <strong>AI Summary Generation:</strong> Summaries are generated
              from AI-extracted content, creating a potential error cascade
              where inaccuracies may compound through multiple layers of AI
              processing.
            </p>
          </div>

          <div id="system-limitations" class="mb-6">
            <h3 class="text-h5 mb-3">
              2.5 System Limitations and Non-Purposes
            </h3>
            <p>
              NegotiateAI does not make autonomous decisions and requires user
              input for all analytical functions. The system does not process
              personal data, concentrating exclusively on publicly accessible
              official documents. All AI-generated results, including summaries
              and responses, serve solely informational and research purposes
              and should not be regarded as legal or political advice. Users
              should verify all information through consultation of original
              source documents and seek appropriate expert guidance for
              professional applications.
            </p>
          </div>
        </div>

        <div id="data-management" class="mb-8">
          <h2 class="text-h4 mb-4">3. Data Management</h2>

          <div id="databases" class="mb-6">
            <h3 class="text-h5 mb-3">3.1 Databases</h3>
            <p>
              SQLite database containing official INC documents and Qdrant
              vector database for semantic search. Both contain publicly
              available documents with authentication-controlled access.
            </p>
          </div>

          <div id="data-sources" class="mb-6">
            <h3 class="text-h5 mb-3">3.2 Data Sources and Processing</h3>
            <p>
              All data comes from official INC sources. User requests are
              processed and sent to the OpenAI API and the Qdrant API, with
              processing taking place via our hosting server.
            </p>
          </div>

          <div id="data-protection" class="mb-6">
            <h3 class="text-h5 mb-3">
              3.3 Data Protection and Privacy Measures
            </h3>
            <p class="mb-4">
              NegotiateAI processes exclusively publicly available official
              documents from UN INC negotiations. No personal data is collected,
              processed, or stored besides technically necessary and outlined in
              the privacy statement.
            </p>

            <ul class="mb-4">
              <li>
                User queries are processed temporarily for response generation
                via OpenAI API
              </li>
              <li>
                No user queries or personal information are permanently stored
              </li>
              <li>Session data is not retained beyond technical necessity</li>
            </ul>

            <p class="mb-4">
              User queries are transmitted to OpenAI's API for processing in
              accordance with OpenAI's data usage policies. Users are informed
              of this processing through the system interface.
            </p>

            <p>
              Standard technical and organizational measures protect system
              integrity and prevent unauthorized access to the document database
              and vector embeddings.
            </p>
          </div>
        </div>

        <div id="transparency" class="mb-8">
          <h2 class="text-h4 mb-4">4. Transparency towards User</h2>
          <p>
            The application clearly indicates all AI components through
            interface badges marking AI-generated content. In addition, for all
            features detailed instructions on how to use are made available. RAG
            methodology is explained on the home page, whilst system limitations
            are communicated through this technical documentation and home
            interface. Complete technical documentation is publicly accessible,
            ensuring full transparency about system capabilities and
            constraints.
          </p>
        </div>

        <div id="monitoring" class="mb-8">
          <h2 class="text-h4 mb-4">
            5. Monitoring, Feedback, and Incident Reporting
          </h2>
          <p class="mb-4">
            Technical development and monitoring are carried out by the GIZ Data
            Lab. No automated bias detection is implemented due to the low-risk
            nature of the system, which operates exclusively with publicly
            available official documents within a restricted content domain.
            Users can report technical issues, inaccuracies, or concerns through
            the contact information provided. All reported incidents are
            reviewed and addressed by the development team to ensure system
            reliability and accuracy.
          </p>

          <p>
            <strong>Contact for Incidents:</strong> For any incidents or
            concerns, please contact:
            <a href="mailto:datalab@giz.de">datalab@giz.de</a>
          </p>
        </div>

        <div id="publication" class="mb-8">
          <h2 class="text-h4 mb-4">6. Publication Status</h2>
          <ul>
            <li>
              This technical documentation is published under the name
              AI_ACT_Annex.md in the repository.
            </li>
            <li>It is linked in the app's README.md.</li>
          </ul>
        </div>

        <div id="contact" class="mb-8">
          <h2 class="text-h4 mb-4">7. Contact</h2>
          <p>
            For any questions, please contact:
            <a href="mailto:datalab@giz.de">datalab@giz.de</a>
          </p>
        </div>

        <div class="mt-8 pt-4 border-t">
          <p class="text-body-2 text-medium-emphasis text-center">
            <em
              >Created in accordance with Annex XI of EU Regulation 2024/1689 on
              the use of Artificial Intelligence (AI Act).</em
            >
          </p>
        </div>
      </v-container>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Data for the models table
const modelHeaders = [
  { title: "Model", key: "model" },
  { title: "Provider", key: "provider" },
  { title: "Source", key: "source" },
  { title: "Architecture", key: "architecture" },
  { title: "Usage", key: "usage" },
  { title: "Access", key: "access" },
];

const modelData = [
  {
    model: "gpt-4.1-2025-04-14",
    provider: "OpenAI",
    source: "https://cdn.openai.com/papers/gpt-4-system-card.pdf",
    sourceText: "System Card",
    architecture: "Transformer",
    usage: "The model is used exclusively for inference purposes.",
    access: "OpenAI API",
  },
  {
    model: "sentence-transformers/distiluse-base-multilingual-cased-v1",
    provider: "HuggingFace",
    source:
      "https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1",
    sourceText: "Model Card",
    architecture: "DistilBert",
    usage:
      "The model is used exclusively to create document embeddings for semantic search and for semantic search.",
    access: "Self-hosted",
  },
];

// Scroll to section function
const scrollTo = (elementId: string) => {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};
</script>

<style scoped>
.toc-list {
  line-height: 1.6;
}

.toc-list a {
  text-decoration: none;
  color: rgb(var(--v-theme-primary));
}

.toc-list a:hover {
  text-decoration: underline;
}

.toc-list ol {
  margin-top: 8px;
  margin-bottom: 8px;
}

h1,
h2,
h3 {
  scroll-margin-top: 20px;
}

p {
  line-height: 1.6;
  margin-bottom: 16px;
}

ul,
ol {
  line-height: 1.6;
  margin-bottom: 16px;
  padding-left: 24px;
}

li {
  margin-bottom: 4px;
}

.underlined-header {
  text-decoration: underline;
  text-decoration-color: #09677f;
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}
</style>
