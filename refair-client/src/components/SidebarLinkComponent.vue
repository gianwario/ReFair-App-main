<template>
  <span :class="customClass">
    <a :href="href" target="_blank">
      <ion-icon :name="iconName"></ion-icon>
      {{ linkText }}
    </a>
  </span>
</template>

<script>
export default {
  name: "SidebarLinkComponent",
  props: {
    href: {
      type: String,
      required: true,
    },
    iconName: {
      type: String,
      required: true,
    },
    linkText: {
      type: String,
      required: true,
    },
    customClass: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Aggiungi qui i tuoi stili per il link della sidebar se necessario */
</style>
