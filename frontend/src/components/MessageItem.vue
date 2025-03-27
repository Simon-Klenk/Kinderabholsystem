<template>
  <div class="message-item">
    <!-- Message text displaying the formatted message with dynamic user input -->
    <div v-if="text.includes('Medizinischer Notfall:')">
      <strong>{{ text }}</strong>
    </div>

    <div class="message-text" v-else>
      Die Eltern von <strong>{{ text }}</strong> bitte zum Check-in kommen
    </div>

    <div class="message-meta">
      <!-- Formatted date of the message -->
      <span class="message-date">{{ formattedDate }}</span>

      <div class="message-state">
        <!-- Display the message's current state with corresponding class styling -->
        <span :class="statusClass"> {{ translatedState }} </span>

        <!-- Tooltip info icon that toggles visibility of the message's status explanation -->
        <span class="info-icon" @click="toggleTooltip">❓</span>

        <!-- Tooltip providing more details about the current message state -->
        <div v-if="showTooltip" class="tooltip">
          {{ statusExplanation }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MessageItem",
  props: {
    // Prop for the message text
    text: String,
    // Prop for the message date
    date: String,
    // Prop for the message state (status)
    state: String,
  },
  data() {
    return {
      // State to toggle the visibility of the tooltip
      showTooltip: false,
    };
  },
  computed: {
    // Computed property to format the date using toLocaleString
    formattedDate() {
      return new Date(this.date).toLocaleString();
    },

    // Translates the state to a human-readable format
    translatedState() {
      const statusTranslations = {
        received: "Wartet auf Freigabe",
        approved: "Wird angezeigt",
        rejected: "Wurde abgelehnt",
        sent: "An AV Gesendet",
        displayed: "Wurde angezeigt",
      };
      return statusTranslations[this.state] || this.state;
    },

    // Provides a detailed explanation of the message's status
    statusExplanation() {
      const explanations = {
        received:
          "Das AV-Team hat deine Nachricht erhalten. Es entscheidet jetzt wann und ob es deine Nachricht auf der LED-Wall anzeigt. Du wirst hier informiert, sobald es eine Entscheidung trifft",
        approved:
          "Das AV-Team zeigt deine Nachricht gerade auf der LED-Wall an.",
        rejected:
          "Das AV-Team hat entschieden deine Nachricht nicht auf der LED-Wall anzuzeigen.",
        sent: "Deine Nachricht wird gerade an das AV-Team gesendet, ist aber noch nicht dort angekommen.",
        displayed:
          "Deine Nachricht ist jetzt nicht mehr auf der LED-Wall zu sehen. Sie wurde aber angezeigt.",
      };
      return explanations[this.state] || "";
    },
  },
  methods: {
    // Toggles the visibility of the tooltip when the info icon is clicked
    toggleTooltip() {
      this.showTooltip = !this.showTooltip;
    },

    // Returns the appropriate CSS class based on the current message state
    statusClass() {
      return {
        "status-pending": this.state === "received",
        "status-success": this.state === "approved",
        "status-error": this.state === "rejected",
        "status-sent": this.state === "sent",
        "status-displayed": this.state === "displayed",
      };
    },
  },
};
</script>

<style scoped>
/* Styling for the overall message item container */
.message-item {
  display: flex;
  flex-direction: column;
  background: white;
  padding: 25px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* Styling for the message text */
.message-text {
  font-size: 16px;
  color: #333;
}

/* Styling for the metadata section (date and status) */
.message-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

/* Container for the message state (status) and the tooltip icon */
.message-state {
  display: flex;
  align-items: center;
  position: relative;
}

/* Margin between the status text and the tooltip icon */
.message-state span {
  margin-right: 8px;
}

/* Styling for the tooltip info icon */
.info-icon {
  cursor: pointer;
  font-size: 18px;
  color: black;
  margin-left: 8px;
}

/* Tooltip styling for displaying detailed status information */
.tooltip {
  position: absolute;
  top: -75px;
  transform: translateX(-50%);
  background-color: #f8f9fa;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px;
  z-index: 10;
}

/* Styling for each message state (status) */
.status-pending {
  background: #f0ad4e;
  color: white;
}

.status-success {
  background: #5cb85c;
  color: white;
}

.status-error {
  background: #d9534f;
  color: white;
}

.status-sent {
  background: #5bc0de;
  color: white;
}

.status-displayed {
  background: #ffc107;
  color: white;
}
</style>
