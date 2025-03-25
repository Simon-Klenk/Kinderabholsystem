<template>
  <div class="message-create">
    <!-- Title of the message creation form -->
    <h2 class="message-title">Notfall - Hilfe anfordern</h2>

    <!-- Raspberry Pi Status -->
    <p v-if="isRaspberryOnline" class="status-online"></p>
    <p v-else class="status-offline">
      ❌ System funktioniert aktuell nicht - AV kann nicht benachrichtigt
      werden!!
    </p>

    <!-- Form for creating a new emergency message -->
    <form @submit.prevent="createMessage">
      <p class="label">NOTFALL</p>
      <div>
        <!-- Input the emergeny person -->
        <input
          type="text"
          id="content"
          v-model="message.content"
          placeholder="Wer wird benötigt?"
          @input="validateInput"
          required
        />
      </div>

      <!-- Submit button, disabled if form is not valid, submitting, or Raspberry Pi is offline -->
      <button
        type="submit"
        :disabled="!isValid || isSubmitting || !isRaspberryOnline"
      >
        Nachricht senden
      </button>
    </form>

    <!-- Success message displayed when the message is successfully sent -->
    <div v-if="successMessage" class="success">
      <p>Nachricht erfolgreich gesendet!</p>
    </div>

    <!-- Error message displayed if there is an issue with the submission -->
    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Message object containing the content and status of the message
      message: { content: "", status: "sent" },
      successMessage: null, // Stores success message when the message is sent
      errorMessage: null, // Stores error message in case of an issue
      isValid: false, // Flag indicating if the input is valid
      isSubmitting: false, // Flag indicating if the message is being sent
      isRaspberryOnline: false, // Flag to check if Raspberry Pi is available
    };
  },
  methods: {
    /**
     * Checks if the Raspberry Pi is running by making a GET request to the Django API.
     * Updates `isRaspberryOnline` based on the response.
     */
    async checkRaspberryStatus() {
      try {
        console.log("Prüfe Raspberry Pi Status...");
        const response = await fetch("http://192.168.104.45/api/live/", {
          method: "GET",
        });

        this.isRaspberryOnline = response.ok;

        console.log("Raspberry Online Status:", this.isRaspberryOnline);
      } catch (error) {
        this.isRaspberryOnline = false;
        console.log("Fehler beim Abrufen des Status:", error);
      }
    },

    /**
     * Validates the input: checks format and length.
     * The input must follow the format "Vorname N." (first name + initial).
     */
    validateInput() {
      const maxLength = 35;
      const isLengthValid = this.message.content.length <= maxLength;

      // If the input length exceeds the limit, show an error message
      if (!isLengthValid) {
        this.errorMessage = `Die Eingabe darf maximal ${maxLength} Zeichen lang sein.`;
        this.isValid = false;
        this.isValid = isLengthValid; // Set valid flag
      }
    },

    /**
     * Handles form submission and sends the message via API.
     * Ensures the Raspberry Pi is online before sending.
     */
    async createMessage() {
      if (!this.isValid || this.isSubmitting || !this.isRaspberryOnline) return; // Prevent multiple submissions

      this.isSubmitting = true; // Set the status to 'sending'

      try {
        // Add the word Notfall to message
        const messageToSend = {
          content: `Notfall: ${this.message.content}`,
          status: "sent",
        };

        // Make an API request to send the message
        const response = await fetch("http://192.168.104.45/api/emergency/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(messageToSend),
        });

        // Handle non-successful response
        if (!response.ok)
          throw new Error(`HTTP-Fehler! Status: ${response.status}`);

        // On success, display a success message and clear any previous errors
        this.successMessage = "Nachricht erfolgreich gesendet!";
        this.errorMessage = null;

        // Redirect to the state page after a short delay
        setTimeout(() => this.$router.push("/state"), 1500);

        // Reset the form and disable the submit button
        this.message.content = "";
        this.message.status = "sent";
        this.isValid = false;
      } catch (error) {
        // If an error occurs, display an error message
        this.errorMessage = `Fehler beim Senden der Nachricht: ${error.message}`;
        this.successMessage = null;
      } finally {
        // Reset the submitting flag after the process is complete
        this.isSubmitting = false;
      }
    },
  },

  /**
   * Lifecycle hook: Runs when the component is mounted.
   * Checks the Raspberry Pi status immediately and every 2 seconds.
   */
  mounted() {
    this.checkRaspberryStatus(); // Initial check
    // setInterval(this.checkRaspberryStatus, 2000); // Check every 2 seconds
  },
};
</script>

<style scoped>
/* Styling for the message creation form container */
.message-create {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Title styling */
.message-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

/* Styling for the labels */
.label,
.label2 {
  font-size: 16px;
}

/* Styling for the input field */
input {
  width: 50%;
  max-width: 400px;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 5px;
}

/* Styling for error and success messages */
.success {
  color: green;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.error {
  color: red;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

/* Styling for the submit button */
button {
  padding: 12px;
  background-color: gray;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* Hover effect for the submit button */
button:hover {
  background-color: rgba(36, 72, 36, 0.89);
}

/* Disabled button state */
button:disabled {
  background-color: lightgray;
  cursor: not-allowed;
}

/* Raspberry Pi online/offline status messages */
.status-online {
  color: green;
  font-size: 16px;
  text-align: center;
}

.status-offline {
  color: red;
  font-size: 16px;
  text-align: center;
}
</style>
