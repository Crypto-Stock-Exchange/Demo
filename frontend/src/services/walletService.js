import { ref } from 'vue';

const walletAddress = ref(null);
const showPopup = ref(false);
const walletRowProvider = ref(null);
const walletType = ref(null);
const netwokrType = ref("local");

async function getMetaMaskProvider() {
  if (window.ethereum?.providers) {
    return window.ethereum.providers.find((p) => p.isMetaMask);
  } else if (window.ethereum?.isMetaMask) {
    return window.ethereum;
  }
  return null;
}

async function connectMetaMask() {
  const provider = await getMetaMaskProvider();

  if (!provider) {
    alert("MetaMask not detected. Please install it.");
    return;
  }

  try {
    const accounts = await provider.request({ method: 'eth_requestAccounts' });
    walletAddress.value = accounts[0];

    walletRowProvider.value = provider;

    walletType.value = 'MetaMask';

    switchToNetwork(11155111);

    return accounts[0];
  } catch (error) {
    console.error("Connection rejected or failed", error);
    return null;
  }
}

async function switchToNetwork(chainId) {
  if (!walletRowProvider.value) {
    console.warn("No wallet provider available.");
    return;
  }

  try {
    await walletRowProvider.value.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0x' + chainId.toString(16) }],
    });
    if (chainId == 31337) {
      netwokrType.value = "local";
    }
    if (chainId == 11155111) {
      netwokrType.value = "test";
    } if (chainId == 56) {
      netwokrType.value = "bnb";
    }
  } catch (err) {
    console.error('Failed to switch network:', err);
  }
}

function openConnectPopup() {
  showPopup.value = true;
}

function closeConnectPopup() {
  showPopup.value = false;
}

// Optionally expose formatted address
function getFormattedAddress() {
  if (!walletAddress.value) return 'Connect Wallet';
  return `${walletAddress.value.slice(0, 6)}...${walletAddress.value.slice(-4)}`;
}

export default {
  walletAddress,
  walletType,
  walletRowProvider,
  showPopup,
  netwokrType,
  connectMetaMask,
  switchToNetwork,
  openConnectPopup,
  closeConnectPopup,
  getFormattedAddress,
};
