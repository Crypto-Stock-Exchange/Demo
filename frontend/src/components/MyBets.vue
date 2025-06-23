<template>
  <div class="home-container pulsing-background">
    <div class="content-wrapper">
      <h2 class="page-title">My Bets</h2>

      <div class="bet-grid">
        <div class="bet-card" v-for="bet in userBets" :key="bet.id">

          <!-- EXPIRED: ready to collect -->
          <div v-if="daysLeft(bet.deadline) === 0">
            <h3>{{ bet.symbol }}</h3>
            <p><strong>Total Amount:</strong> {{ (bet.amount + profit(bet)).toFixed(2) }} USDT</p>
            <div v-if="hasProfit(bet)">
              <p class="profit">
                <strong>Profit:</strong> +{{ profit(bet).toFixed(2) }} USDT ({{ profitPercent(bet) }}%)
              </p>
            </div>
            <div v-else>
              <p class="loss">
                <strong>Loss:</strong> -{{ Math.abs(profit(bet).toFixed(2)) }} USDT ({{ profitPercent(bet) }}%)
              </p>
            </div>

            <button class="collect-button" @click="collectExpiredBet(bet)">
              Collect
            </button>
          </div>
          
          <!-- ACTIVE: still ongoing -->
          <div v-else>
            <router-link 
            :to="{ name: 'StockDetails', params: { id: bet.stockid || 1} }" 
             class="stock-link"
            >
            <h3>{{ bet.symbol }}</h3>
          </router-link>
            <p><strong>Range:</strong> {{ bet.lower }}$ - {{ bet.upper }}$</p>
            <p><strong>Aktiv:</strong> {{ daysActive(bet.datenow) }} day</p>
            <p><strong>Time left:</strong> {{ daysLeft(bet.deadline) }} day</p>
            
            <h2><strong>Total Amount: {{ (bet.amount + profit(bet)).toFixed(2) }} USDT</strong> </h2>
            <div v-if="hasProfit(bet)">
            <p class="profit">
                <strong>Profit:</strong> +{{ profit(bet).toFixed(2) }} USDT ({{ profitPercent(bet) }}%)
            </p>
            </div>
            <div v-else>
              <p class="loss">
                <strong>Loss:</strong> -{{ Math.abs(profit(bet).toFixed(2)) }} USDT ({{ profitPercent(bet) }}%)
              </p>
            </div>

            <button class="collect-button" @click="collectActiveBet(bet)">
              Collect Early
            </button>
          </div>

        </div>
      </div>
    </div>
        <ConfirmDialog
    v-if="showConfirmPopup"
    :message="popupMessage"
    @confirm="onPopupConfirm"
    @cancel="onPopupCancel"
  />
  </div>
</template>


<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import walletService from '@/services/walletService';
import makeContract from '@/services/makeContract';
import { ethers } from 'ethers'
import ConfirmDialog from '@/components/ConfirmDialog.vue';

const userBets = ref([]);
const showConfirmPopup = ref(false)
const confirmCallback = ref(null)
const popupMessage = ref("")


const daysActive = (start) => {
  const now = Date.now();
  const startDate = new Date(start * 1000);
  const diffMs = now - startDate.getTime();
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
};

const daysLeft = (end) => {
  const now = Date.now();
  const endDate = new Date(end * 1000);
  const diffMs = endDate.getTime() - now;
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  return days > 0 ? days : 0;
};

const profit = (bet) => {
  const fee = Number(bet.ownerfee || 0);
  const win = Number(bet.winamount || 0);
  return (-fee + win);
};

const hasProfit = (bet) => profit(bet) >= 0;

const profitPercent = (bet) => {
  const amount = Number(bet.amount);
  if (amount === 0) return '0';
  const pct = (profit(bet) / amount) * 100 ;
  return pct.toFixed(2);
};

onMounted( () => {
loadmybets();
});

const loadmybets = async () =>{
  try {
    if (walletService.walletAddress.value) {
      axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL
      const response = await axios.get(`/api/bets/${walletService.walletAddress.value}`);
      userBets.value = response.data;
    }
  } catch (error) {
    console.error('Hiba a tétek lekérésekor:', error);
    userBets.value = [];
  }
}

const onPopupConfirm = () => {
  showConfirmPopup.value = false
  if (confirmCallback.value) confirmCallback.value()
}

const onPopupCancel = () => {
  showConfirmPopup.value = false
  confirmCallback.value = null
}

 const collectExpiredBet = async (bet) => {
    const provider = new ethers.BrowserProvider(walletService.walletRowProvider.value);
    const signer = await provider.getSigner();
    const exchangeAbi = [
  "function sellNFT(uint256 tokenId, address buyer, uint256 price, address owner, uint256 ownerfee, bytes signature) external"
];

    const contract = new ethers.Contract(
      makeContract.contractaddress,  
      exchangeAbi,
      signer
    );
    const now = new Date();
    const timestamp = now.toISOString(); 
    const message = `Login to CryptoStockExchange at ${timestamp}`;

    const signature = await signer.signMessage(message);

    try {
 if (!walletService.walletAddress.value) {
    throw new Error('Wallet address is not available');
  }
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL
  const { data: result } = await axios.post("/api/sell", { 
    tokenId: bet.bet_id,
    signature: signature,
    message: message
  });

    const signaturetoSend = `0x${result.signature}`;

    const tx = await contract.sellNFT(
      bet.bet_id,
      result.owner,
      result.price,
      walletService.walletAddress.value,  
      result.ownerfee,
      signaturetoSend
    );

     await tx.wait(); 

     loadmybets();

    }
   catch (error) {
    console.error('Hiba a tétek lekérésekor:', error);
    userBets.value = [];
  }
  };
 const collectActiveBet = (bet) => {
  const now = Date.now() / 1000;
  const datenow = bet.datenow;
  const deadline = bet.deadline;
  const price = bet.amount + bet.winamount - bet.ownerfee;

  const totalDuration = Math.abs(deadline - datenow);
  const timeElapsed = now - datenow;

  if (now < deadline && totalDuration > 0) {
    const ratio = timeElapsed / totalDuration;
    const penaltyFeePercent = 0.5 * (1 - ratio);
    const penaltyFee = price * penaltyFeePercent;

    popupMessage.value = `This bet has not yet expired.\nThe penalty: ${penaltyFee.toFixed(2)} USDT\nYou will get ${(price - penaltyFee).toFixed(2)} USDT instead of ${price.toFixed(2)} USDT.\n\nDo you want to continue?`;
    confirmCallback.value = () => {
      collectExpiredBet(bet);
    }
    showConfirmPopup.value = true;
    return;
  }

  collectExpiredBet(bet);
};
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
}

.stock-link {
  text-decoration: none;
  color: white;
  display: block;
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

.empty-state {
  font-size: 1.2rem;
  opacity: 0.8;
  margin-top: 2rem;
}

.bet-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.bet-card {
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  z-index: 2;
}


.bet-card h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.bet-card p {
  font-size: 1.05rem;
  line-height: 1.5;
}

.profit {
  color: #00ff77;
  font-weight: bold;
  font-size: 1.3rem !important;
}

.loss {
  color: #ff5f5f;
  font-weight: bold;
  font-size: 1.3rem !important;
}

.collect-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem; 
  background-color: #4caf50;
  color: white;
  font-size: 0.94rem;      
  font-weight: 600;        
  border: none;
  border-radius: 8px;     
  cursor: pointer;
  transition: transform 0.2s ease;
}

.collect-button:hover {
  background-color: #388e3c;
}

</style>
