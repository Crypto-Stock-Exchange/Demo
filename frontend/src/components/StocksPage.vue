<template>
  <div class="home-container simple-background">
    <div class="content-wrapper">
      <h2 class="page-title">Stocks</h2>

      <div class="stock-grid">
        <div 
          class="stock-card" 
          v-for="stock in stocks" 
          :key="stock.name"
        >
          <router-link 
            :to="{ name: 'StockDetails', params: { id: stock.id } }" 
            class="stock-link"
          >
            <h3>{{ stock.name }}</h3>
            <p>Stock Prices: {{  Number(stock.price  || 0).toFixed(2) }} USD</p>
            <p>Total Bet Volume: {{  Number(stock.total_bet_amount  || 0).toFixed(2) }} USD</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const stocks = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/stocks')
    stocks.value = response.data
  } catch (error) {
    console.error("Nem sikerült lekérni az adatokat:", error)
  }
})
</script>

<style scoped>
.home-container {
  flex: 1;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  height: calc(100vh - 80px);
  padding: 2rem;
  color: white;
  overflow: hidden;
   z-index: 2;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: left;
  font-weight: bold;
}

.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stock-card {
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
   z-index: 2;
}

.stock-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.stock-link {
  text-decoration: none;
  color: white;
  display: block;
}

.stock-link h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.stock-link p {
  font-size: 1.1rem;
  opacity: 0.9;
}
</style>
