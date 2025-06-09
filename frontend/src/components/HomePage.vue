<template>
  <div class="home-container pulsing-background">
    <h1 class="home-title">Welcome to Crypto Stock Exchange</h1>
    <p class="home-subtitle">Predict stock price ranges, stake your funds, and earn rewards based on accuracy.</p>

<router-link to="/about-us" class="home-button">
  Explore
</router-link>
  </div>
</template>

<script setup>
// Nem kell most ide script, mert csak statikus szép oldal
</script>

<style scoped>
.home-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 80px);
  padding: 2rem;
  text-align: center;
  color: white;
  overflow: hidden;
  z-index: 2;
}

.home-title {
  font-size: 7rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.home-subtitle {
  font-size: 1.25rem;
  max-width: 600px;
  margin-bottom: 2rem;
  color: #ffffff;
  /* világosabb szürke szöveg */
}

.home-button {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  border: none;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  border-radius: 9999px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  text-decoration: none;
}

.home-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(59, 130, 246, 0.6);
  background: linear-gradient(90deg, #06b6d4, #3b82f6);
}

@media (max-width: 768px) {
  .home-title {
  font-size: 4rem;
}
}
</style>