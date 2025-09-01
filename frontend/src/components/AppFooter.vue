<template>
  <v-footer class="bg-white">
    <div class="d-flex align-center ga-2">
      <v-img
        src="@/assets/Deutsche_Gesellschaft_für_Internationale_Zusammenarbeit_Logo.svg"
        rounded="0"
        height="29"
        width="106"
      />
      <v-img
        src="@/assets/Data_Lab_Logo_BW.svg"
        rounded="0"
        height="32"
        width="32"
      />
      <v-img src="@/assets/andeffect.svg" rounded="0" height="39" width="79" />
    </div>

    <v-spacer />
    <div class="d-flex ga-4">
      <a href="/documentation" target="_blank" rel="noreferrer">
        Technical Documentation
      </a>
      <a
        href="https://www.blog-datalab.com/data-protection/"
        target="_blank"
        rel="noreferrer"
      >
        Data Protection
      </a>
      <a
        href="https://www.blog-datalab.com/legalinformation/"
        target="_blank"
        rel="noreferrer"
      >
        Legal Info
      </a>
      <a
        href="https://www.blog-datalab.com/contact/"
        target="_blank"
        rel="noreferrer"
      >
        Contact
      </a>
    </div>
  </v-footer>
</template>

<style scoped>
.v-footer {
  padding: 64px 240px;
  max-height: 160px;
  min-height: 160px;
}

/* Mobile & Tablet view */
@media (max-width: 1264px) {
  .v-footer {
    padding: 64px 32px;
    flex-direction: column;
    align-items: flex-start;
    max-height: 377px;
    min-height: auto;
  }

  .d-flex:last-child {
    flex-direction: column;
    align-items: flex-start;
    margin-top: 16px;
  }
}

/* Mobile view - allow automatic height adjustment for additional links */
@media (max-width: 768px) {
  .v-footer {
    min-height: 377px;
    max-height: none;
  }
}

a {
  color: rgb(var(--v-theme-on-surface));
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
