<template>
  <header>
    <!-- Logo image for the header, providing an alt description for accessibility -->
    <img alt="icf" src="../assets/icf-kids-logo_v2_black.png" class="logo" />
  </header>
</template>

<script>
export default {
  // Component name: "Header"
  // eslint-disable-next-line
  name: "Header",
};
</script>

<style scoped>
/* Styling for the logo image in the header */
.logo {
  /* Set logo width to 100% but with a maximum of 700px for responsiveness */
  width: 100%;
  max-width: 700px;

  /* Ensure the logo maintains its aspect ratio */
  height: auto;

  /* Add top margin for spacing from other elements */
  margin-top: 20px;
}
</style>
