import { ref, watch } from 'vue';
import walletService from './walletService';
import { ethers } from 'ethers';

const erc721Abi = [
  "function balanceOf(address owner) view returns (uint256)"
];

const showPopup = ref(false);

const tusdaddress = '0xE6a687Bd952ba5143366892fa661bfdEad036939';
const contractaddress = '0xdb6988A84356884139AC206D9d946A451f822ac1';
const nftaddress = '0x58201ECd3f23b6F8d6caf34d7bd11f00a46138d1';

const myBetsVisible = ref(false);

function setShowPopup(show) {
  showPopup.value = show;
}

function getShowPopup() {
  return showPopup.value;
}

async function hasnft() {
  if (walletService.walletAddress.value && walletService.netwokrType !== 'local') {
    const provider = new ethers.BrowserProvider(walletService.walletRowProvider.value);
    const signer = await provider.getSigner();

    const nftContract = new ethers.Contract(nftaddress, erc721Abi, signer);

    const balance = await nftContract.balanceOf(walletService.walletAddress.value);
    return balance > 0;
  } else { return false; }
}

watch(walletService.walletAddress && walletService.netwokrType, async (newAddress) => {
  if (newAddress) {
    myBetsVisible.value = await hasnft();
  } else {
    myBetsVisible.value = false;
  }
}, { immediate: true });

export default {
  setShowPopup,
  getShowPopup,
  hasnft,
  myBetsVisible,
  nftaddress,
  tusdaddress,
  contractaddress,
}