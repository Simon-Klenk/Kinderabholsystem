<template>
  <div class="messages-container">
    <!-- Title for the messages list -->
    <h2 class="messages-title">Gesendete Nachrichten</h2>

    <!-- Display loading indicator while messages are being fetched -->
    <div v-if="loading" class="loading">⏳ Lade Nachrichten...</div>

    <!-- Display messages once they have been loaded -->
    <div v-else>
      <!-- Iterate over the messages and display each one using the MessageItem component -->
      <MessageItem
        v-for="message in messages"
        :key="message.id"
        :text="message.content"
        :date="message.created_at"
        :state="message.status"
      />
    </div>
  </div>
</template>

<script>
import MessageItem from "@/components/MessageItem.vue";

export default {
  components: { MessageItem },
  data() {
    return {
      // Array to store the list of messages
      messages: [],
      // Flag to indicate loading state
      loading: true,
      // ID of the polling interval for message updates
      intervalId: null,
    };
  },
  async created() {
    // Fetch messages when the component is created
    await this.getMessages();
    // Start polling to refresh messages periodically
    this.startPolling();
  },
  beforeUnmount() {
    // Stop polling when the component is destroyed to clean up resources
    this.stopPolling();
  },
  methods: {
    // Fetch messages from the API
    async getMessages() {
      try {
        // Make a GET request to fetch the messages
        let response = await fetch("http://192.168.104.45/api/messages/", {
          method: "GET",
        });

        // Check if the response is successful
        if (!response.ok)
          throw new Error(`HTTP-Fehler! Status: ${response.status}`);

        // Parse and store the messages, then update the loading state
        this.messages = await response.json();
        this.loading = false;
      } catch (error) {
        // Log any errors that occur during the fetch process
        console.error("Fehler beim Abrufen der Nachrichten:", error);
        this.loading = false;
      }
    },

    // Start polling to fetch new messages periodically
    startPolling() {
      // Poll every 4 seconds to get updated messages
      this.intervalId = setInterval(this.getMessages, 4000);
    },

    // Stop polling when the component is about to be unmounted
    stopPolling() {
      if (this.intervalId) clearInterval(this.intervalId);
    },
  },
};
</script>

<style scoped>
/* Styling for the container of the messages list */
.messages-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Styling for the title of the messages list */
.messages-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

/* Styling for the loading indicator */
.loading {
  text-align: center;
  font-size: 16px;
  color: #777;
}
</style>
