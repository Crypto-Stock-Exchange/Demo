<template>
  <div class="popup-overlay" @click.self="cancel">
    <div class="popup-box">
      <h3>⚠️ Attention!</h3>
      <p>{{ props.message }}</p>
      <div class="popup-actions">
        <button class="confirm-btn" @click="confirm">Continue</button>
        <button class="cancel-btn" @click="cancel">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue'
const props = defineProps({
  message: String,
})

const emit = defineEmits(['confirm', 'cancel'])

const confirm = () => emit('confirm')
const cancel = () => emit('cancel')
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}

.popup-box {
  background: #1f2937;
  padding: 2rem;
  border-radius: 10px;
  color: white;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.popup-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: space-around;
}

.confirm-btn, .cancel-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.confirm-btn {
  background: #10b981;
  color: white;
}

.cancel-btn {
  background: #ef4444;
  color: white;
}
p {
  font-family: 'Courier New', Courier, monospace;
}
</style>
