<template>
  <div class="chart-wrapper"  v-if="prices.length">
    <div class="buttons">
      <button
        v-for="range in ranges"
        :key="range"
        :class="{ active: selectedRange === range }"
        @click="changeRange(range)"
      >
        {{ range }}
      </button>
    </div>

    <div class="chart-container">
      <svg :width="width" :height="height">
        <!-- Háttér -->
        <rect
          :width="width"
          :height="height"
          fill="rgba(255, 255, 255, 0.1)"
        />

        <!-- Rácsvonalak és számok -->
        <g v-for="(lineY, index) in gridLines" :key="index">
          <line
            :x1="0"
            :y1="lineY.y"
            :x2="width"
            :y2="lineY.y"
            stroke="#ccc"
            stroke-dasharray="4"
            opacity="0.3"
          />
          <text
            :x="5"
            :y="lineY.y - 5"
            font-size="15"
            fill="#ccc"
          >
            {{ lineY.value }}
          </text>
        </g>

        <!-- Vonaldiagram -->
        <polyline
          :points="points"
          fill="none"
          stroke="url(#lineGradient)"
          stroke-width="2"
        />

        <!-- Szép színátmenetes vonal -->
        <defs>
          <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#00c6ff" />
            <stop offset="100%" stop-color="#0072ff" />
          </linearGradient>
        </defs>
      </svg>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    stockId: {
      type: Number,
      required: true
    },
  },
  data() {
    return {
      prices: [],
      isRendered: false,
      selectedRange: '1m',
      ranges: ['24h', '5d', '1m', '6m', '1y', '5y', 'all'],
      width: 800,
      height: 500
    };
  },
  computed: {
      points() {
    if (!this.prices.length) return "";

    const maxPrice = Math.max(...this.prices);
    const minPrice = Math.min(...this.prices);
    
    const paddingTopBottom = 30;
    const paddingLeft = 70;
    const paddingRight = 30; 

    const dx = (this.width - paddingLeft - paddingRight) / (this.prices.length - 1 || 1);
    const dy = maxPrice === minPrice ? 0 : 
      (this.height - 2 * paddingTopBottom) / (maxPrice - minPrice);

    return this.prices
      .map((price, i) => {
        const x = paddingLeft + i * dx;
        const y = this.height - paddingTopBottom - ((price - minPrice) * dy);
        return `${x},${y}`;
      })
      .join(" ");
  },

  gridLines() {
  if (!this.prices.length) return [];

  const lines = [];
  const maxPrice = Math.max(...this.prices);
  const minPrice = Math.min(...this.prices);
  const paddingTopBottom = 30;
  const step = (maxPrice - minPrice) / 5;

  for (let i = 0; i <= 5; i++) {
    const value = minPrice + i * step;
    const y = this.height - paddingTopBottom - ((value - minPrice) * 
      (this.height - 2 * paddingTopBottom) / (maxPrice - minPrice));
    
    lines.push({
      y,
      value: value.toFixed(2)
    });
  }

  return lines;
}


  },
  mounted() {
    this.fetchPrices();
  },
  methods: {
    async fetchPrices() {
      try {
        axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL
        const response = await axios.get(`/api/stocks/${this.stockId}/pricehistory${this.selectedRange}`);
        const data = await response.data;
        if (Array.isArray(data)) {
          this.prices = data;
        } else {
          console.error("Nem megfelelő adat:", data);
        }
      } catch (error) {
        console.error("Hiba az adatok lekérdezésekor:", error);
      }
    },
    changeRange(range) {
      this.selectedRange = range;
      this.fetchPrices();
    }
  }
};
</script>

<style scoped>
.chart-wrapper {
  background: linear-gradient(to bottom right, #1f1f1f, #2c2c2c);
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  color: white;
  font-family: 'Segoe UI', sans-serif;
  margin: auto;
  z-index: 10;
}

.buttons {
  margin-bottom: 15px;
  text-align: center;
}

button {
  margin: 0 4px;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 8px;
  border: none;
  background: #444;
  color: white;
  transition: background 0.3s;
}
button:hover {
  background: #666;
}
button.active {
  background: #0072ff;
  color: white;
  font-weight: bold;
}
.chart-container {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
}
</style>
