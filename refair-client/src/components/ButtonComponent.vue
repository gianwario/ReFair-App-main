<template>
  <button
    :type="buttonType"
    :class="buttonClass"
    :id="buttonId"
    :data-dismiss="dataDismiss"
    @click="handleClick"
    :style="buttonStyle"
  >
    <ion-icon :name="iconName"></ion-icon>
    <label :class="labelClass">{{ labelText }}</label>
    <i></i>
  </button>
</template>

<script>
export default {
  name: "ButtonComponent",
  props: {
    buttonType: {
      type: String,
      required: true,
      default: "button",
    },
    buttonClass: {
      type: String,
      required: true,
    },
    buttonId: {
      type: String,
      required: false,
    },
    dataDismiss: {
      type: String,
      required: false,
    },
    clickHandler: {
      type: Function,
      required: true,
    },
    buttonStyle: {
      type: String,
      required: false,
    },
    iconName: {
      type: String,
      required: true,
    },
    labelClass: {
      type: String,
      required: true,
      default: "button__text",
    },
    labelText: {
      type: String,
      required: true,
    },
  },
  methods: {
    handleClick() {
      if (this.clickHandler) {
        this.clickHandler();
      }
    },
  },
};
</script>
