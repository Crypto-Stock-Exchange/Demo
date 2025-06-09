<template>
  <NavBar />
  <router-view />
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>

* {
  box-sizing: border-box;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

html,
body {
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.pulsing-background {
  position: relative;
  background: linear-gradient(-45deg, #0f0c29, #7c3aed, #020203, #3b82f6, #6366f1);
  background-size: 400% 400%;
  animation: gradientPulse 20s ease infinite;
  z-index: 0;
}

/* Pulsing gradient animation */
@keyframes gradientPulse {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
/* 
/* Diagonal moving lines overlay */
.pulsing-background::before,
.pulsing-background::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background-image: repeating-linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.05) 0,
    rgba(255, 255, 255, 0.05) 2px,
    transparent 2px,
    transparent 10px
  );
  animation: moveLines 30s linear infinite;
  pointer-events: none;
  z-index: 0;
}

.pulsing-background::after {
  animation-delay: -15s; /* offset the animation for more depth */
  opacity: 0.3;
}

/* Line movement */
@keyframes moveLines {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(100px, 100px);
  }
}

.pulsing-background,
.simple-background {
  position: relative;
  overflow: hidden; 
}

.simple-background {
  position: relative;
  overflow: hidden;
  background: linear-gradient(-45deg, #3b82f6, #08092a);
  background-size: cover; /* vagy '100% 100%' ha fix méret kell */
  z-index: 0;
}

/* Statikus vonal overlay */
.simple-background::before,
.simple-background::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background-image: repeating-linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.05) 0,
    rgba(255, 255, 255, 0.05) 2px,
    transparent 2px,
    transparent 10px
  );
  pointer-events: none;
  z-index: 0;
}

.simple-background::after {
  opacity: 0.3;
} 

</style>