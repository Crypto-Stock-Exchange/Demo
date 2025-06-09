<template>
  <div class="home-container simple-background">
    <div class="left-panel" v-if="stock">
      <div class="stock-details">
        <h2>{{ stock.name }}</h2>
        <p class="price">Price: {{  Number(stock.price  || 0).toFixed(2) }} USD</p>
        <div class="metric">
          <div class="metric-label">Market Cap</div>
          <div class="metric-value">${{ formatValue(stock.market_cap) }}</div>
        </div>

        <div class="metric">
          <div class="metric-label">Volume</div>
          <div class="metric-value">${{ formatValue(stock.volume) }}</div>
        </div>

        <div class="metric">
          <div class="metric-label">52 Week range</div>
          <div class="metric-value">${{ stock.week_52_range }}</div>
        </div>

        <div class="average-section">
          <p>Bet informacion:</p>
          <p>Average Interval: ${{  Number(stock.avgintervalum || 0).toFixed(2) }}</p>
          <p>Average Time: {{ secondsToDays(stock.avgtime) }} day</p>
          <p>Average Bet Volume: {{ Number(stock.avgvolume || 0).toFixed(2) }} USDT</p>
          <p>Total Bet Volume: {{ Number(stock.total_bet_amount || 0).toFixed(0) }} USDT</p>
        </div>
        <button class="connect-button" @click="handleMakeContractClick">Make Contract</button>
      </div>
    </div>

    <MakeContract v-if="makeContract.getShowPopup()" :price="Number(stock.price)" :symbol="String(stock.link)" />

    <div class="right-panel" v-if="stock">
      <DrowPrice :stock-id="stock.id" />
    </div>

  </div>
</template>

<script setup>
import DrowPrice from './DrowPrice.vue';
import { ref, onMounted, defineAsyncComponent } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import walletService from '@/services/walletService.js';
//import MakeContract from './MakeContract.vue';
import makeContract from '@/services/makeContract';

const MakeContract = defineAsyncComponent(() => import('./MakeContract.vue'));

const route = useRoute();
const stock = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(`/api/stocks/${route.params.id}`);
    stock.value = response.data;
  } catch (error) {
    console.error('Nem sikerült lekérni az adatokat:', error);
  }
});

function handleMakeContractClick() {
  if (walletService.walletAddress.value === null) {
    walletService.openConnectPopup();
    if (walletService.walletAddress.value !== null){
      makeContract.setShowPopup(true);
    }
  } else {
    makeContract.setShowPopup(true);
  }
}

function secondsToDays(seconds) {
  const days = seconds / (60 * 60 * 24);
  return days.toFixed(2);
}

const formatValue = (value) => {
  if (value >= 1_000_000_000_000) {
    return (value / 1_000_000_000_000).toFixed(2) + 'T';
  } else if (value >= 1_000_000_000) {
    return (value / 1_000_000_000).toFixed(2) + 'B';
  } else if (value >= 1_000_000) {
    return (value / 1_000_000).toFixed(2) + 'M';
  } else if (value === 0) {
    return '-';
  } else {
    return value.toLocaleString();
  }
};

</script>

<style scoped>
.home-container {
  flex: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  height: calc(100vh - 80px);
  color: white;
  overflow: hidden;
  padding: 1.25rem 0 0 0;
  z-index: 2;

}

.left-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stock-details {
  background: #111827;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  max-width: 500px;
  width: 100%;
  z-index: 2;
}

.stock-details h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.stock-details p {
  font-size: 1.3rem;
  margin: 1rem 0;
}

.stock-details .price {
  font-size: 1.6rem;
  font-weight: bold;
  color: #22d3ee;
  margin: 1rem 0;
}

.average-section {
  background-color: rgba(255, 255, 255, 0.08);
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 0.75rem;
}


.right-panel {
  flex: 1;
  padding: 1rem, 0rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.connect-button {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 9999px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 0 10px #3b82f6;
  margin-top: 1.5rem;
}

.connect-button:hover {
  background: linear-gradient(90deg, #06b6d4, #3b82f6);
  box-shadow: 0 0 15px #06b6d4;
  transform: scale(1.05);
}

.metric {
  margin: 1.5rem 0;
}

.metric-label {
  font-size: 0.95rem;
  color: #9ca3af; 
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-size: 2rem;
  font-weight: 600;
  color: white;
}
@media (max-width: 768px) {
  .home-container {
    flex-direction: column;
    padding: 1rem;
    height: auto;
  }

  .left-panel{
    width: 100%;
    justify-content: center;
    align-items: center;
    padding: 0;
    margin: 0, 1rem;
  }
  .right-panel{
    display: none;
  }

  .stock-details {
    max-width: 100%;
    padding: 1.5rem;
    padding: 0.9rem;
  }

  .stock-details h2 {
    font-size: 1.6rem;
  }

  .stock-details p {
    font-size: 1rem;
  }

  .metric-value {
    font-size: 1.5rem;
  }

  .connect-button {
    width: 100%;
    padding: 0.8rem;
    font-size: 1rem;
  }

  .right-panel {
    margin-top: 2rem;
  }
}

</style>
