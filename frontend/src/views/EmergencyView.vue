<template>
  <div class="message-create">
    <!-- Emergency Request Title -->
    <h2 class="message-title">Notfall - Hilfe anfordern</h2>

    <!-- Display a warning message if the Raspberry Pi is offline -->
    <p v-if="!isRaspberryOnline" class="status-offline">
      ❌ System funktioniert aktuell nicht - AV kann nicht benachrichtigt
      werden!!
    </p>

    <!-- Inform the user about the message that will be sent -->
    <div class="message-text">
      Du sendest zur Anzeige auf der LED-Wall folgene Nachricht an AV:
    </div>

    <div class="spaced-text">
      <strong>
        Medizinischer Notfall: Sanitäter / Arzt / Fachpersonal - bitte zum Kids
        Check-In!
      </strong>
    </div>

    <!-- Emergency button, disabled if the Raspberry Pi is offline or request is in progress -->
    <button
      @click="confirmAndSendMessage"
      :disabled="!isRaspberryOnline || isSubmitting"
      class="spaced-button"
    >
      Notfallnachricht senden
    </button>

    <!-- Display success message when the message is sent successfully -->
    <div v-if="successMessage" class="success">
      <p>Nachricht erfolgreich gesendet!</p>
    </div>

    <!-- Display error message if sending fails -->
    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      successMessage: null, // Stores success feedback when message is sent
      errorMessage: null, // Stores error messages in case of failure
      isSubmitting: false, // Flag to track if the message is being sent
      isRaspberryOnline: false, // Indicates if the Raspberry Pi is reachable
    };
  },
  methods: {
    /**
     * Checks the availability of the Raspberry Pi by making a request to the API.
     * Updates the "isRaspberryOnline" state accordingly.
     */
    async checkRaspberryStatus() {
      try {
        const response = await fetch("http://192.168.104.45/api/live/");
        this.isRaspberryOnline = response.ok;
      } catch (error) {
        this.isRaspberryOnline = false;
      }
    },

    /**
     * Sends an emergency message to the API endpoint if the Raspberry Pi is online.
     * Displays success or error messages accordingly.
     */
    async sendMessage() {
      this.isSubmitting = true; // Disable button while submitting
      try {
        const response = await fetch("http://192.168.104.45/api/emergency/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content:
              "Medizinischer Notfall: Sanitäter / Arzt / Fachpersonal - bitte zum Kids Check-In!",
            status: "sent",
          }),
        });
        if (!response.ok) throw new Error(`HTTP-Fehler: ${response.status}`);
        this.successMessage = "Nachricht erfolgreich gesendet!";
        this.errorMessage = null;
        setTimeout(() => this.$router.push("/state"), 1500);
      } catch (error) {
        this.errorMessage = `Fehler beim Senden: ${error.message}`;
      } finally {
        this.isSubmitting = false; // Re-enable button after submission
      }
    },

    /**
     * Displays a confirmation dialog before sending the emergency message.
     * Calls sendMessage() only if the user confirms.
     */
    confirmAndSendMessage() {
      if (confirm("Sicher, dass du senden möchtest?")) {
        this.sendMessage();
      }
    },
  },

  /**
   * Lifecycle hook: Checks the Raspberry Pi status when the component is mounted.
   */
  mounted() {
    this.checkRaspberryStatus();
  },
};
</script>

<style scoped>
/* Container styling */
.message-create {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Title styling */
.message-title {
  font-size: 24px;
  margin-bottom: 20px;
}

/* Button styling */
button {
  padding: 12px;
  background-color: gray;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

/* Button hover effect */
button:hover {
  background-color: green;
}

/* Disabled button styling */
button:disabled {
  background-color: lightgray;
  cursor: not-allowed;
}

/* Success message styling */
.success {
  color: green;
  font-size: 16px;
  margin-top: 10px;
}

/* Error message styling */
.error {
  color: red;
  font-size: 16px;
  margin-top: 10px;
}

/* Raspberry Pi online/offline status */
.status-online {
  color: green;
  font-size: 16px;
}

.status-offline {
  color: red;
  font-size: 16px;
}

/* Extra spacing for the button */
.spaced-button {
  margin-top: 30px;
}

.spaced-text {
  margin-top: 15px;
}
</style>
