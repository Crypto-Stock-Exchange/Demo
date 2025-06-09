<template>
  <nav class="navbar">
  <div class="hamburger" @click="toggleMenu">
      &#9776;
    </div>
    <div v-if="isMenuOpen" class="menu-overlay" @click="toggleMenu"></div>
    <div class="menu" :class="{ open: isMenuOpen }">
      <router-link v-for="item in visibleMenuItems" :key="item.name" :to="item.path" class="menu-button" @click="isMenuOpen = false">
         <template v-if="item.name === 'Home'">
        <img src="@/assets/home.png" alt="Home" class="menu-icon" />
      </template>
      <template v-else>
        {{ item.name }}
      </template>
      </router-link>
    </div>


    <div class="connect">
      <select v-if="walletService.walletAddress.value !== null" v-model="selectedNetwork" @change="switchNetwork" class="network-select">
       
        <!--  <option value="local">Local</option> -->
        <option value="testnet">Sepolia Testnet</option>
        <!--  <option value="bnb">BNB</option> -->
        
      </select>

       <button @click="walletService.openConnectPopup()" class="connect-button">
      {{ formattedAddress }}
  </button>

      <ConnectWalletPopup 
    v-if="walletService.showPopup.value" 
    @close="walletService.closeConnectPopup" 
    @wallet-connected="onWalletConnected"
  />
    </div>
  </nav>
</template>

<script setup >
import { computed, ref } from 'vue';
import ConnectWalletPopup from './ConnectWalletPopup.vue';
import walletService from '@/services/walletService';
import makeContract from '@/services/makeContract';

const menuItems = [
  { name: 'Home', path: '/' },
  { name: 'Stocks', path: '/stocks' },
  { name: 'About Us', path: '/about-us' },
  { name: 'My Bets', path: '/my-bets',},
];

const visibleMenuItems = computed(() =>
  menuItems.filter(item => {
    if (item.name === 'My Bets') {
      return makeContract.myBetsVisible.value;
    }
    return true;
  })
);


const selectedNetwork = ref('testnet')

const formattedAddress = computed(() => {
  const addr = walletService.walletAddress.value;
  return addr ? addr.slice(0, 6) + '...' + addr.slice(-4) : 'Connect Wallet';
});

function onWalletConnected(address) {
  walletService.setWalletAddress(address);
  walletService.closeConnectPopup();
}

function switchNetwork(event) {
  const selected = event.target.value
  if (selected === 'local') walletService.switchToNetwork(31337)
  else if (selected === 'testnet') walletService.switchToNetwork(11155111)
  else if (selected === 'bnb') walletService.switchToNetwork(56)
}


const isMenuOpen = ref(false); 

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};


</script>

<style>
/* NAVBAR alap */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 2rem;
  background: linear-gradient(-45deg, #111827, #0d214e);
  /* Nagyon sötét háttér */
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

/* MENÜ */
.menu {
  display: flex;
  gap: 1rem;
  font-family: 'Courier New', Courier, monospace;
}

.menu-button {
  background: transparent;
  border: 2px solid transparent;
  color: white;
  padding: 0 1.2rem;
  border-radius: 9999px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;          /* Flexbox aktiválása */
  align-items: center;           /* Függőleges középre igazítás */
  justify-content: center;       /* Vízszintes középre igazítás */
  height: 40px;                  /* Adj neki fix magasságot, ha kell */
  gap: 0.5rem;                   /* Ha több elem lesz benne, pl. ikon + szöveg */
}

.menu-button:hover {
  transform: translateY(-2px);
}

/* CONNECT WALLET */
.connect-button {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 9999px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 0 10px #3b82f6;
}

.connect-button:hover {
  background: linear-gradient(90deg, #06b6d4, #3b82f6);
  box-shadow: 0 0 15px #06b6d4;
  transform: scale(1.05);
}

.network-select {
  margin-right: 10px;
  padding: 6px;
  border-radius: 6px;
}

.menu-icon {
  width: 74px;
  vertical-align: middle;
}


.hamburger {
  display: none;
  font-size: 2rem;
  cursor: pointer;
  color: white;
  z-index: 30;
}

/* Aktív (nyitott) állapot */
.side-menu.open {
  left: 0;
}

.network-select {
  background: #1a1a2b;
  color: #fff;
  border: 2px solid #555;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  font-size: 1rem;
  transition: 0.3s ease;
  appearance: none;

  border-color: #4facfe;
  outline: none;
  box-shadow: 0 0 8px #4facfe88;
}



@media (max-width: 768px) {
  .hamburger {
    display: block;
     z-index: 1000;    
  }
  .navbar {
    padding: 0.5rem 1rem;
  }

 .menu {
    display: flex;                /* legyen flex, hogy működjön az animáció */
    flex-direction: column;
    position: fixed;              /* fix pozíció, hogy lefedje a teljes oldal bal szélét */
    top: 0;
    left: 0;
    width: 220px;
    height: 100vh;
    background: linear-gradient(-45deg, #111827, #0d214e);
    padding-top: 60px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 999;               
  }

  .menu.open {
    transform: translateX(0);
  }

  .network-select {
  padding: 0.5rem 0.6rem;
}

.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
}


</style>