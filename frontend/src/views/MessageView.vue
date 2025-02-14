<template>
  <div class="message-create">
    <!-- Title of the message creation form -->
    <h2 class="message-title">Nachricht an AV senden</h2>

    <!-- Form for creating a new message -->
    <form @submit.prevent="createMessage">
      <p class="label">Die Eltern von</p>
      <div>
        <!-- Input for the recipient's name (first name and initial) -->
        <input
          type="text"
          id="content"
          v-model="message.content"
          placeholder="Vorname N."
          @input="validateInput"
          required
        />
      </div>
      <p class="label2">bitte zum Check-in kommen</p>
      <!-- Submit button, disabled if form is not valid or if submitting -->
      <button type="submit" :disabled="!isValid || isSubmitting">
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
      message: {
        content: "",
        status: "sent",
      },
      successMessage: null,
      errorMessage: null,
      isValid: false, // Flag indicating if the input is valid
      isSubmitting: false, // Flag indicating if the message is being sent
    };
  },
  methods: {
    // Validates the input: checks format and length
    validateInput() {
      const maxLength = 25;
      const regex = /^[A-Za-zÄÖÜäöüß]+\s[A-Za-z]\.$/; // Regex for format "Vorname N."
      const isFormatValid = regex.test(this.message.content);
      const isLengthValid = this.message.content.length <= maxLength;

      // If the input length exceeds the limit, show an error message
      if (!isLengthValid) {
        this.errorMessage = `Die Eingabe darf maximal ${maxLength} Zeichen lang sein.`;
        this.isValid = false;
      } else {
        // If format is invalid, show a format-specific error
        this.errorMessage = isFormatValid
          ? null
          : "Bitte das Format 'Vorname N.' verwenden. Datenschutz!!!";
        this.isValid = isFormatValid && isLengthValid; // Set valid flag
      }
    },
    // Handles form submission and sends the message via API
    async createMessage() {
      if (!this.isValid || this.isSubmitting) return; // Prevent multiple submissions

      this.isSubmitting = true; // Set the status to 'sending'

      try {
        // Make an API request to send the message
        const response = await fetch("http://192.168.104.45/api/messages/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.message),
        });

        // Handle non-successful response
        if (!response.ok)
          throw new Error(`HTTP-Fehler! Status: ${response.status}`);

        // On success, display a success message and clear any previous errors
        this.successMessage = "Nachricht erfolgreich gesendet!";
        this.errorMessage = null;

        // Redirect to the state page after a short delay
        setTimeout(() => {
          this.$router.push("/state");
        }, 1500);

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
.label {
  margin-bottom: 5px;
  font-size: 16px;
}
.label2 {
  margin-top: 5px;
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
.error {
  color: red;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.success {
  color: green;
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
</style>
