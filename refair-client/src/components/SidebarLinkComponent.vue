<template>
  <span :class="customClass">
    <a :href="safeHref" target="_blank">
      <ion-icon :name="iconName"></ion-icon>
      {{ linkText }}
    </a>
  </span>
</template>

<script>
export default {
  name: "SidebarLinkComponent",
  props: {
    sidebarHref: {
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
  computed: {
    safeHref() {
      return this.sidebarHref;
    },
  },
};
</script>
