<template>
  <div class="popup" @mousedown.self.prevent="close">
    <div class="popup-content">
      <button class="wallet-button" @click="connectWallet">
        <img src="@/assets/MetaMask_Fox.svg" alt="MetaMask" class="fox-icon" />
        Connect with MetaMask
      </button>
      <button class="cancel-button" @click="$emit('close')">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import walletService from '@/services/walletService'

async function connectWallet() {
  if (typeof window.ethereum === 'undefined' || !window.ethereum.isMetaMask) {
    const shouldInstall = confirm("MetaMask is not installed. Click OK to install it from the Chrome Web Store.");
    if (shouldInstall) {
      window.open("https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=en&pli=1", "_blank");
    }
    return;
  }

  const account = await walletService.connectMetaMask();
  if (account) {
    walletService.walletAddress.value = account;
    walletService.closeConnectPopup();
  }
}


function close() {
  walletService.closeConnectPopup()
}
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 12;
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-content {
  background: white;
  padding: 2rem;
  width: 320px;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.wallet-button,
.cancel-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  width: 100%;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.wallet-button {
  background: #111827;
  color: white;
}

.wallet-button:hover {
  transform: scale(1.05);
}

.cancel-button {
  background-color: #ccc;
  color: black;
}

.cancel-button:hover {
    transform: scale(1.05);
}

.fox-icon {
  width: 25px;
  height: 25px;
}
</style>
