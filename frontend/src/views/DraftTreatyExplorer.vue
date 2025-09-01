<template>
  <v-row class="bg-white">
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto">
      <v-container class="py-12">
        <div class="mb-6">
          <h1 class="fontsize-h2 mt-12 mb-10 underlined-header">
            Draft Treaty Explorer
          </h1>
        </div>
        <v-row>
          <v-col cols="12" md="6">
            <v-card
              color="primary"
              variant="tonal"
              class="text-white"
              height="100%"
            >
              <v-card-title>Topics</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6" class="d-flex flex-column">
                    <p>
                      Explore the topics based on the treaty. Click on a topic
                      to see its Key Elements.
                    </p>
                    <v-spacer></v-spacer>
                    <v-btn
                      variant="outlined"
                      @click="scrollToSection('taxonomy')"
                      >Go to section</v-btn
                    >
                  </v-col>
                  <v-col>
                    <example-tree />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card color="primary" variant="tonal" class="text-white">
              <v-card-title>Draft Treaty Evolution</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6" class="d-flex flex-column">
                    <p>
                      Explore the evolution of treaty articles across different
                      draft versions. Click on an article to see its history and
                      changes.
                    </p>
                    <v-spacer></v-spacer>
                    <v-btn
                      variant="outlined"
                      @click="scrollToSection('evolution')"
                      >Go to section</v-btn
                    >
                  </v-col>
                  <v-col cols="12" md="6" class="d-flex justify-center">
                    <v-timeline
                      density="compact"
                      dot-color="primary"
                      line-color="primary"
                      truncate-line="both"
                      size="15"
                      line-inset="1"
                    >
                      <v-timeline-item
                        v-for="(version, index) in [
                          'Zero draft',
                          'Revised draft',
                          'Compilation text',
                          'Chair\'s text',
                        ]"
                        :key="index"
                        icon-color="secondary"
                      >
                        <div class="text-caption">
                          {{ version }}
                        </div>
                      </v-timeline-item>
                    </v-timeline>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto" id="taxonomy">
      <v-container>
        <div class="py-12">
          <h2 class="fontsize-h4 py-2">Topics</h2>
          <topics-taxonomy-chart></topics-taxonomy-chart>
        </div>
      </v-container>
    </v-col>
  </v-row>

  <v-row class="bg-white">
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto" id="evolution">
      <v-container>
        <div class="py-12">
          <v-tooltip max-width="400px">
            <template v-slot:activator="{ props }">
              <div class="d-flex align-center mb-4">
                <h2 class="fontsize-h4 py-2">Draft Treaty Evolution</h2>
                <v-btn
                  target="_blank"
                  color="primary"
                  size="x-small"
                  variant="text"
                  v-bind="props"
                  icon="mdi-information-outline"
                  class="ml-2"
                >
                </v-btn>
              </div>
            </template>
            <p class="text-body-1">
              <strong><u>How It Works</u></strong>
              <br />
            </p>
            <ol class="ml-4">
              <li>
                Select treaty version: Choose any draft from the timeline to
                view its structure.
              </li>
              <li>
                Review article status: See the status of each article within the
                selected draft.
              </li>
              <li>
                Track article evolution: Click on any article to view its
                development history across all treaty versions and see what
                changes occurred in each round. The timeline spans from early
                drafts to the current chair text, showing the complete
                negotiation journey.
              </li>
            </ol>
          </v-tooltip>
          <draft-treaty-evolution></draft-treaty-evolution>
        </div>
      </v-container>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
const scrollToSection = (section: string) => {
  // Logic to scroll to a specific section
  // This can be implemented based on your application's routing or section IDs
  const sectionElement = document.getElementById(section);
  if (sectionElement) {
    sectionElement.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

<style>
.underlined-header {
  text-decoration: underline;
  text-decoration-color: #09677f;
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}
</style>
