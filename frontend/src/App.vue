<template>
  <!-- Header Component -->
  <Header></Header>

  <!-- Navigation links for the application -->
  <nav>
    <!-- Link to send a new message -->
    <router-link to="/">Nachricht senden</router-link> |
    <!-- Link to view the status page -->
    <router-link to="/state">Status</router-link>
  </nav>

  <!-- Dynamic view based on routing -->
  <router-view />
</template>

<script>
import Header from "@/components/Header.vue"; // Import the Header component

export default {
  components: {
    Header, // Register the Header component to be used in this template
  },
};
</script>

<style>
/* Global app styles */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif; /* Set the font family for the app */
  -webkit-font-smoothing: antialiased; /* Apply smoothing for webkit-based browsers */
  -moz-osx-font-smoothing: grayscale; /* Apply smoothing for Firefox on macOS */
  text-align: center; /* Center the text */
  color: #2c3e50; /* Set text color */
}

/* Styles for the navigation bar */
nav {
  padding: 20px; /* Add padding around the nav elements */
}

/* Style for the links in the navigation */
nav a {
  font-weight: bold; /* Make the text bold */
  color: #2c3e50; /* Set link color */
  cursor: pointer; /* Change the cursor to a pointer to indicate interactivity */
}

/* Active link styles (when a link is exactly active) */
nav a.router-link-exact-active {
  color: #42b983; /* Change the color when the link is active */
}
</style>
