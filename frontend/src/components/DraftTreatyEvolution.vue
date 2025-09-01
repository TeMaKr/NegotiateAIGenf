<template>
  <v-row>
    <v-col cols="12" md="6">
      <div class="text-body-1">
        Explore the evolution of treaty articles across different draft
        versions. Click on an article to see its history and changes.
      </div>
      <v-timeline
        density="compact"
        :direction="display.mdAndUp ? 'horizontal' : 'vertical'"
        dot-color="surface-light"
        truncate-line="both"
        class="my-8"
      >
        <v-timeline-item
          v-for="(version, index) in availableVersions"
          :key="index"
          class="text-center cursor-pointer"
          :icon="index === selectedVersionIndex ? 'mdi-circle' : ''"
          @click="selectedVersionIndex = index"
          icon-color="primary"
        >
          <div class="text-caption">
            {{ version.label }}
          </div>
        </v-timeline-item>
      </v-timeline>

      <v-divider class="my-8" />

      <div class="my-4">
        <h2 class="fontsize-h5">{{ currentVersion?.label }}</h2>

        <em>{{ getVersionDate(currentVersion?.key || "") }}</em>

        <p class="py-2">
          {{ getVersionDescription(currentVersion?.key || "") }} It contains
          {{ getVersionArticleCount(currentVersion?.key || "") }}
          articles.
        </p>
      </div>
    </v-col>
    <v-col cols="12" md="6">
      <div class="pdf-preview-container">
        <div class="text-subtitle-2 mb-2 d-flex align-center">
          <v-icon class="mr-2" size="small">mdi-file-pdf-box</v-icon>
          Document Preview
        </div>
        <div class="pdf-viewer-compact">
          <iframe
            :src="getPdfPath(currentVersion?.key) || ''"
            width="100%"
            height="300"
            style="border: none; border-radius: 4px; background: white"
            @error="handlePdfError(currentVersion?.key)"
          ></iframe>
        </div>
        <div class="mt-2 d-flex gap-2">
          <v-btn
            size="small"
            variant="outlined"
            @click="openPdfFullscreen(currentVersion?.key)"
            block
          >
            <v-icon start size="small">mdi-fullscreen</v-icon>
            Open Full PDF
          </v-btn>
        </div>
      </div>
    </v-col>
  </v-row>
  <!-- Document Structure -->
  <v-row>
    <v-col cols="12">
      <div class="d-flex align-center">
        <v-switch
          v-model="showChanges"
          label="Show Changes from previous version"
          inset
          density="compact"
          color="primary"
        ></v-switch>
        <v-spacer></v-spacer>
        <!--Legend Tooltip-->
        <v-tooltip>
          <template #activator="{ props }">
            <v-chip
              color="primary"
              v-bind="props"
              prepend-icon="mdi-help-circle"
              >Legend</v-chip
            >
          </template>
          <div>
            <!-- Table with all chips-->
            Meaning of each indicator
            <ul class="ml-4">
              <li>
                First Appearance: The article first appeared in the draft treaty
              </li>
              <li>
                Placeholder: Temporary text noted in original drafts article
              </li>
              <li>Contested: Text contains brackets and is under discussion</li>
              <li>
                Settled: Article is finalised with no brackets or disputes
              </li>
              <li>
                Modified: Article text has been amended from previous version
              </li>
              <li>
                Not present: Article does not exist in this treaty version
              </li>
              <li>Removed: Article was deleted from previous version</li>
              <li>Not existing: Article did not exist in previous version</li>
            </ul>
          </div>
        </v-tooltip>
      </div>
      <v-expansion-panels>
        <v-expansion-panel
          v-for="(item, index) in currentStructure"
          :key="`${item.type}-${item.id || index}`"
          :hide-actions="item.type === 'part'"
          :disabled="item.type === 'part'"
          :elevation="item.type === 'part' ? 0 : 0"
          rounded="lg"
          bg-color="transparent"
        >
          <v-expansion-panel-title>
            <div
              :class="[
                'ma-1',
                item.level === 0
                  ? ''
                  : item.level === 1
                    ? 'ml-0'
                    : item.level === 2
                      ? 'ml-8'
                      : item.level === 3
                        ? 'ml-12'
                        : 'ml-16',
                'd-flex d-inline align-center',
              ]"
            >
              <span
                v-if="item.number"
                class="text-caption text-grey font-mono mr-2"
                style="min-width: 3rem"
              >
                {{ item.number }}
              </span>
              <span>{{ item.title }}</span>
            </div>
            <v-spacer></v-spacer>
            <div class="mr-2" v-if="item.id">
              <!-- Current status badge -->
              <v-tooltip location="bottom">
                <template #activator="{ props }">
                  <v-chip
                    v-if="getVersionData(item.id)?.status?.[0] && !showChanges"
                    density="compact"
                    v-bind="props"
                    variant="outlined"
                    prepend-icon="mdi-list-status"
                    :color="
                      getStatusChipColor(
                        getVersionData(item.id)?.status?.[0] || 'normal',
                      )
                    "
                  >
                    {{ getVersionData(item.id)?.status?.[0] }}
                  </v-chip>
                </template>
                <div>Status of article in {{ currentVersion?.label }}</div>
              </v-tooltip>
              <v-chip
                v-if="
                  getVersionData(item.id)?.status?.[0] &&
                  getEvolutionDescription(
                    item.id || '',
                    currentVersion?.key || '',
                  ) !== 'No changes' &&
                  showChanges
                "
                density="compact"
                variant="outlined"
                prepend-icon="mdi-set-right"
              >
                {{
                  getEvolutionDescription(
                    item.id || "",
                    currentVersion?.key || "",
                  )
                }}
              </v-chip>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text v-if="item.type !== 'part' && item.id">
            <!-- Table format for article evolution -->
            <div class="mx-auto" style="max-width: 900px">
              <h3 class="text-overline mb-1">
                <v-icon class="mr-1">mdi-history</v-icon>
                Article Evolution
              </h3>

              <v-table density="compact">
                <thead>
                  <tr>
                    <th class="text-left">Version</th>
                    <th class="text-left">Content</th>
                    <th class="text-left">Current Status</th>
                    <th class="text-left">Changes from Previous</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(version, index) in availableVersions"
                    :key="version.key"
                  >
                    <!-- Version column -->
                    <td class="py-2" width="150">
                      <div class="d-flex align-center">
                        <v-icon
                          :color="
                            getVersionData(item.id, version.key)
                              ? 'primary'
                              : 'grey'
                          "
                          size="small"
                          class="mr-2"
                        >
                          {{
                            getVersionData(item.id, version.key)
                              ? "mdi-check-circle"
                              : "mdi-cancel"
                          }}
                        </v-icon>
                        <span class="font-weight-medium">{{
                          version.label
                        }}</span>
                      </div>
                    </td>

                    <!-- Content column -->
                    <td class="py-2">
                      <div
                        v-if="getVersionData(item.id, version.key)"
                        class="text-body-2"
                      >
                        <div
                          class="pa-2 rounded"
                          style="
                            background-color: rgba(
                              var(--v-theme-on-surface),
                              0.05
                            );
                            font-family: monospace;
                            max-height: 150px;
                            overflow-y: auto;
                          "
                        >
                          {{ getVersionData(item.id, version.key).content }}
                        </div>
                      </div>
                      <div v-else class="text-caption text-medium-emphasis">
                        Not present in this version
                      </div>
                    </td>

                    <!-- Current Status column -->
                    <td class="py-2" width="150">
                      <div v-if="getVersionData(item.id, version.key)">
                        <!-- Use the same chip style as in the panel headers -->
                        <div class="status-pill-container">
                          <v-chip
                            v-if="
                              getVersionData(item.id, version.key)
                                ?.status?.[0] && !showChanges
                            "
                            density="compact"
                            variant="outlined"
                            prepend-icon="mdi-list-status"
                            :color="
                              getStatusChipColor(
                                getVersionData(item.id, version.key)
                                  ?.status?.[0] || 'normal',
                              )
                            "
                          >
                            {{
                              getVersionData(item.id, version.key)?.status?.[0]
                            }}
                          </v-chip>
                        </div>
                      </div>
                      <div v-else>
                        <v-chip
                          density="compact"
                          color="error"
                          variant="outlined"
                          prepend-icon="mdi-minus-circle-outline"
                        >
                          not present
                        </v-chip>
                      </div>
                    </td>

                    <!-- Changes column -->
                    <td class="py-2" width="180">
                      <!-- Change indicator for other versions -->

                      <div class="d-flex align-center mb-1 flex-wrap gap-1">
                        <v-chip
                          v-if="
                            getVersionData(item.id)?.status?.[0] &&
                            getEvolutionDescription(
                              item.id || '',
                              version.key || '',
                            ) !== 'No changes'
                          "
                          density="compact"
                          variant="outlined"
                          prepend-icon="mdi-set-right"
                        >
                          {{
                            getEvolutionDescription(
                              item.id || "",
                              version?.key || "",
                            )
                          }}
                        </v-chip>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import compilation_draft from "../../data/compilation_draft.json";
import chair_text_draft from "../../data/chair_text_draft.json";
import revised_draft from "../../data/revised_draft.json";
import zero_draft from "../../data/zero_draft.json";

const display = useDisplay();

// Types
interface ArticleData {
  title: string;
  [versionKey: string]: any;
}

interface ArticleWithEvolution {
  status: string[];
  content: string;
  brackets: boolean;
  evolution?: {
    status_progression: string[];
    version_order: string[];
    change_descriptions: string[];
  };
}

interface TreatyData {
  metadata: {
    versions: string[];
    baseline: string;
  };
  structure: {
    [versionKey: string]: Array<{
      type: "part" | "article";
      id?: string;
      title: string;
      level: number;
      number?: string;
    }>;
  };
  articles: {
    [articleId: string]: ArticleData;
  };
}

// Reactive data
const selectedVersionIndex = ref(0);
const selectedArticle = ref<string | null>(null);
const treatyData = ref<TreatyData | null>(null);
const rawDataMap = ref<{ [key: string]: any }>({});
const showChanges = ref(false);
// Load and process JSON files
const loadTreatyData = () => {
  // Store raw data for evolution access
  rawDataMap.value = {
    zero_draft: zero_draft,
    compilation_text: compilation_draft,
    chairs_text: chair_text_draft,
    revised_draft: revised_draft,
  };

  // Process the loaded data
  const versions = [
    "zero_draft",
    "revised_draft",
    "compilation_text",
    "chairs_text",
  ];

  // Extract articles from all versions
  const allArticles: { [key: string]: ArticleData } = {};
  const structures: { [key: string]: any[] } = {};

  versions.forEach((versionKey) => {
    const data = rawDataMap.value[versionKey];

    // Use the actual structure from the JSON file
    structures[versionKey] = data.structure || [];

    if (data && data.articles) {
      // Process articles for this version
      Object.entries(data.articles).forEach(
        ([articleId, articleContent]: [string, any]) => {
          // Initialize article if not exists
          if (!allArticles[articleId]) {
            allArticles[articleId] = {
              title: articleContent.title || `Article ${articleId}`,
            };
          }

          // Add version-specific data
          allArticles[articleId][versionKey] = {
            content: articleContent.content || articleContent.title || "",
            status: articleContent.status || ["normal"],
            brackets: articleContent.brackets || false,
          };
        },
      );
    }
  });

  // Set the processed data
  treatyData.value = {
    metadata: {
      versions: versions,
      baseline: "chairs_text",
    },
    structure: structures,
    articles: allArticles,
  };
};

// Computed properties
const availableVersions = computed(() => {
  if (!treatyData.value) return [];
  return treatyData.value.metadata.versions.map((version) => ({
    key: version,
    label:
      version === "zero_draft"
        ? "Zero Draft"
        : version === "compilation_text"
          ? "Compilation Text"
          : version === "chairs_text"
            ? "Chair's Text"
            : version === "revised_draft"
              ? "Revised Draft"
              : version
                  .replace(/_/g, " ")
                  .replace(/\b\w/g, (l) => l.toUpperCase()),
  }));
});

const currentVersion = computed(
  () => availableVersions.value[selectedVersionIndex.value],
);

const currentStructure = computed(() => {
  if (!treatyData.value || !currentVersion.value) return [];
  return treatyData.value.structure[currentVersion.value.key] || [];
});

// Methods
const getVersionData = (articleId: string, versionKey?: string) => {
  const version = versionKey || currentVersion.value?.key;
  if (!version || !treatyData.value?.articles[articleId]) return null;
  return treatyData.value.articles[articleId][version] || null;
};

// Evolution functions (using embedded evolution data from raw JSON)
const getArticleEvolution = (articleId: string) => {
  try {
    // Get evolution data from the first version that has it (usually zero_draft)
    for (const versionKey of [
      "zero_draft",
      "revised_draft",
      "compilation_text",
      "chairs_text",
    ]) {
      const rawData = rawDataMap.value[versionKey];
      if (rawData?.articles?.[articleId]?.evolution) {
        return rawData.articles[articleId].evolution;
      }
    }
    return null;
  } catch (error) {
    console.warn("Error getting article evolution for", articleId, error);
    return null;
  }
};

const getEvolutionStatusForVersion = (
  articleId: string,
  versionKey: string,
): string[] => {
  try {
    const evolution = getArticleEvolution(articleId);
    if (!evolution) {
      return ["same"];
    }

    const versionIndex = evolution.version_order.indexOf(versionKey);
    if (versionIndex === -1) {
      return ["same"];
    }

    const statusProgression = evolution.status_progression[versionIndex];
    if (!statusProgression) {
      return ["same"];
    }

    // Handle comma-separated values using simple approach
    let result: string[] = [];
    if (statusProgression) {
      // @ts-ignore - bypassing TypeScript issue
      const statusStr = String(statusProgression);
      if (statusStr.includes(",")) {
        // @ts-ignore - bypassing TypeScript issue
        result = statusStr
          .split(",")
          .map((s) => s.trim())
          .filter((s) => s.length > 0);
      } else {
        result = [statusStr.trim()];
      }
    }

    if (result.length === 0) {
      return ["same"];
    }

    return result;
  } catch (error) {
    console.warn(
      "Error getting evolution status for",
      articleId,
      versionKey,
      error,
    );
    return ["same"];
  }
};

const getEvolutionDescription = (
  articleId: string,
  versionKey: string,
): string => {
  try {
    const statuses = getEvolutionStatusForVersion(articleId, versionKey);

    // Create a human-readable description from the evolution statuses
    const descriptions = statuses.map((status: string) => {
      switch (status) {
        case "original":
          return "First appearance";
        case "became_settled":
          return "Became settled";
        case "became_contested":
          return "Became contested";
        case "same":
          return "No changes";
        case "contested":
          return "Contested";
        case "settled":
          return "Settled";
        case "new":
          return "New";
        case "removed":
          return "Removed";
        case "modified":
          return "Modified";
        default:
          return status.replace(/_/g, " ");
      }
    });

    return descriptions.join(", ");
  } catch (error) {
    console.warn(
      "Error getting evolution description for",
      articleId,
      versionKey,
      error,
    );
    return "No evolution data";
  }
};

const getStatusChipColor = (status: string) => {
  switch (status) {
    case "contested":
      return "warning";
    case "placeholder":
      return "darkgrey";
    case "normal":
      return "secondary";
    case "settled":
      return "primary";
    case "removed":
      return "error";
    case "new":
      return "success";
    default:
      return "default";
  }
};

// Timeline and PDF functions
const getPdfPath = (versionKey: string): string | null => {
  // Map version keys to actual PDF files in the public folder
  const pdfPaths: { [key: string]: string } = {
    zero_draft: "/drafts/03_zerodraft.pdf",
    revised_draft: "/drafts/04_revised_zero_draft.pdf",
    compilation_text: "/drafts/05_compilation_text.pdf",
    chairs_text: "/drafts/06_chair_text.pdf",
  };
  return pdfPaths[versionKey] || null;
};

const getTimelineIcon = (index: number): string => {
  const icons = [
    "mdi-numeric-1-circle",
    "mdi-numeric-2-circle",
    "mdi-numeric-3-circle",
    "mdi-numeric-4-circle",
  ];
  return icons[index] || "mdi-circle";
};

const getVersionDescription = (versionKey: string): string => {
  const descriptions: { [key: string]: string } = {
    zero_draft:
      "Initial draft text establishing the foundational framework for the plastic pollution treaty.",
    revised_draft:
      "Updated version incorporating feedback and refinements from the zero draft consultations.",
    compilation_text:
      "Consolidated text bringing together various proposals and amendments from negotiations.",
    chairs_text:
      "Chair's streamlined text representing a balanced approach for final negotiations.",
  };
  return descriptions[versionKey] || "Treaty version document";
};

const getVersionDate = (versionKey: string): string => {
  const descriptions: { [key: string]: string } = {
    zero_draft: "4. September 2023",
    revised_draft: "28. December 2023",
    compilation_text: "9. July 2024",
    chairs_text: "1. December 2024",
  };
  return descriptions[versionKey] || "Treaty version document";
};

const getVersionArticleCount = (versionKey: string): number => {
  const data = rawDataMap.value[versionKey];
  return data?.articles ? Object.keys(data.articles).length : 0;
};

const handlePdfError = (versionKey: string) => {
  console.warn(`PDF not found for version: ${versionKey}`);
};

const openPdfFullscreen = (versionKey: string) => {
  const pdfPath = getPdfPath(versionKey);
  if (pdfPath) {
    window.open(pdfPath, "_blank");
  }
};

// Lifecycle
onMounted(() => {
  loadTreatyData();
});
</script>

<style scoped>
.timeline-details {
  min-height: 400px;
}

.pdf-viewer-compact {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white;
}

/* Highlight current version in the table */
tr.current-version {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

/* Improve table appearance */
.evolution-table th {
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.8);
  font-size: 0.85rem;
}

.evolution-table tr:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.03);
}
</style>
