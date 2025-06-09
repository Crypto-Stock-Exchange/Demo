<template>
  <div class="modal-overlay" @mousedown.self.prevent="close">
    <div class="modal-content">
      <h2>Create Contract</h2>
<div class="wallet-info">
  <div class="wallet-row">
    <span class="label">Your address:</span>
    <span class="value">{{ walletService.walletAddress.value }}</span>
  </div>
  <div class="wallet-row">
    <span class="label">Network:</span>
    <span class="value">{{ walletService.netwokrType.value }} network</span>
  </div>
  <div class="wallet-row">
    <span class="label">Your balance:</span>
    <span class="value">
      {{ tusdbalencee === -1 ? 'Loading...' : tusdbalencee + ' USDT' }}
    </span>
  </div>
</div>

<!-- Sepolia Test TUSD Section -->
<div v-if="walletService.netwokrType.value === 'test'" class="test-funds-section">
  <h3>Buy test USDT for (Sepolia)</h3>
  <div class="test-funds-inputs">
    <input
      v-model="amountfortest"
      type="number"
      placeholder="Amount in Sepolia"
      class="eth-input"
    />
    <button @click="sendEthToContract" class="send-button">Send</button>
  </div>
  <div class="faucet-link" style="margin-top: 10px;">
    <small>
      Don't have Sepolia ETH? 
      <a href="https://cloud.google.com/application/web3/faucet/ethereum/sepolia" target="_blank" rel="noopener noreferrer">
        Get Sepolia here
      </a>
    </small>
  </div>
</div>

      <!-- Interval Down and Up inputs -->
      <div class="form-group interval-group">
        <label>Interval in USD</label>
        <div class="interval-inputs">
          <input
            type="number"
            min="1"
            v-model.number="intervalDown"
            placeholder="Down"
            @input="validateInterval"
          />
          <span class="separator">to</span>
          <input
            type="number"
            :min="intervalDown + 1"
            v-model.number="intervalUp"
            placeholder="Up"
            @input="validateInterval"
          />
        </div>
        <p v-if="intervalError" class="error">{{ intervalError }}</p>
      </div>

      <!-- Amount input -->
      <div class="form-group">
        <label for="amount">Amount (TUSD)</label>
        <input
          id="amount"
          type="number"
          step="0.01"
          v-model.number="amount"
          :placeholder="`Max: ${ Number(tusdbalencee || 0).toFixed(2) } TUSD`"
          class="amount-input"
          @input="enforceTwoDecimals"
        />
      </div>


      <!-- Lockout period date input -->
  <div class="form-group">
    <label for="lockout">Lockout Period</label>
    <Datepicker
      v-model="lockoutPeriod"
      :min-date="new Date()"
      :enable-time-picker="false"
      placeholder="Select date"
      dark
      class="amount-input"
    />
  </div>

      <div class="buttons">
        <button class="confirm-btn" @click="confirmContract">Confirm</button>
        <button class="cancel-btn" @click="close">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watchEffect, defineProps} from 'vue';
import { ethers, BrowserProvider } from 'ethers'
import makeContract from '@/services/makeContract';
import walletService from '@/services/walletService';
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
// import { keccak256, toUtf8Bytes } from "ethers";

const intervalDown = ref(1);
const intervalUp = ref(2);
const amount = ref(0);
const lockoutPeriod = ref(null);
const intervalError = ref(null);
const amountfortest = ref(null);
const tusdbalencee = ref(-1);

const erc20Abi = [
  "function balanceOf(address owner) view returns (uint256)",
  "function approve(address spender, uint256 amount) public returns (bool)"
];


const exchangeAbi = [
  "function placeBet(string symbol, uint256 lower, uint256 upper, uint256 amount, uint256 deadline, address owner, uint256 ownerfee, bytes signature) external"
];


const props = defineProps({
  price: {
    type: Number,
    required: true,
  },
    symbol: {
    type: String,
    required: true,
  }
});

function enforceTwoDecimals(event) {
  const val = event.target.value;
  const match = val.match(/^\d+(\.\d{0,2})?/);
  if (match) {
    amount.value = parseFloat(match[0]);
  } else {
    amount.value = null;
  }
}

function validateInterval() {
  if (intervalUp.value <= intervalDown.value) {
    intervalError.value = 'Interval "Up" must be greater than "Down"';
  } else {
    intervalError.value = null;
  }
}

function close() {
  makeContract.setShowPopup(false);
}

async function confirmContract() {
  validateInterval();

  if (intervalError.value) {
    alert(intervalError.value);
    return;
  }
  if (amount.value <= 0) {
    alert('Please enter a valid amount greater than 0');
    return;
  }
  if (!lockoutPeriod.value) {
    alert('Please select a lockout period date');
    return;
  }

  try {
    const provider = new ethers.BrowserProvider(walletService.walletRowProvider.value);
    const signer = await provider.getSigner();

    const contract = new ethers.Contract(
      makeContract.contractaddress,  
      exchangeAbi,
      signer
    );

    const tusddcontract = new ethers.Contract(
      makeContract.tusdaddress,  
      erc20Abi,
      signer
    );

    const symbol = props.symbol;
    const lower = Math.floor(intervalDown.value * 100);  
    const upper = Math.floor(intervalUp.value * 100);
    const amountInWei = ethers.parseUnits(amount.value.toString(), 18);
    const deadline = Math.floor(new Date(lockoutPeriod.value).getTime() / 1000);
    const senderAddress = walletService.walletAddress.value;

    // 🔹 Kérés a Flask backendhez aláírásért
    const response = await fetch("/api/sign", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender: senderAddress,
        amountInWei: amountInWei.toString(),
        deadline: deadline
      })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Failed to get signature from backend");
    }

    const { signature, owner, ownerfee } = result;
    const signaturetoSend = `0x${signature}`;
    //const buffer = BigInt(10n ** 15n);

    // 🔹 Token jóváhagyás
    const approveTx = await tusddcontract.approve(makeContract.contractaddress, amountInWei.toString());
    await approveTx.wait();

const amountwei = BigInt(amountInWei);
const ownerFee = BigInt(ownerfee);
const amountToSend = amountwei - ownerFee;


// console.log("symbol:", symbol);
// console.log("lower:", lower);
// console.log("upper:", upper);
// console.log("amountInWei:",  amountToSend.toString());
// console.log("deadline:", deadline);
// console.log("owner:", owner);
// console.log("ownerfee:", ownerFee.toString());
// console.log("signaturetoSend:", signaturetoSend);

    // 🔹 Szerződéshívás új metódussal
const tx = await contract.placeBet(
  symbol,
  lower,
  upper,
  amountToSend.toString(),  
  deadline,
  owner,
  ownerFee.toString(), 
  signaturetoSend
);

    await tx.wait(); 

try {
  const res = await fetch("/api/emit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_address: walletService.walletAddress.value })
  });

  if (!res.ok) {
    console.warn("⛔ Backend Is not working:", await res.text());
  }

} catch (e) {
  console.error("❌ We can't call the bacend server:", e);
}

  makeContract.hasnft();

    alert("Bet placed successfully!");
    makeContract.setShowPopup(false);

  } catch (error) {
    console.error("Contract call failed:", error);
    alert("Failed to place bet. See console for details.");
  }

  makeContract.setShowPopup(false);
}


const getTokenBalance = async () => {
  try {

    const provider = new ethers.BrowserProvider(walletService.walletRowProvider.value);
    const signer = await provider.getSigner();
    const userAddress = await signer.getAddress();


    const contractAddress = makeContract.tusdaddress;
    const tokenContract = new ethers.Contract(contractAddress, erc20Abi, provider);

    const rawBalance = await tokenContract.balanceOf(userAddress);

    const formattedBalance = ethers.formatUnits(rawBalance, 18);

    return formattedBalance;
  } catch (err) {
    console.error("Failed to fetch token balance:", err);
  }
};

const sendEthToContract = async () => {
  try {
    if (!window.ethereum) {
      alert("MetaMask not found.")
      return
    }
    // Ensure provider is correctly set
    const provider = new BrowserProvider(walletService.walletRowProvider.value);
    if (!provider) {
      alert("Wallet not connected.")
      return;
    }
    const contractAddress = makeContract.tusdaddress;

    const signer = await provider.getSigner();

    const tx = await signer.sendTransaction({
      to: contractAddress,
      value: ethers.parseEther(amountfortest.value.toString()), 
    });

    await tx.wait();

    alert("Transaction successful!");
  } catch (err) {
    console.error("Transaction failed:", err);
    alert("Transaction failed");
  }
};
// function getSelector(errorSignature) {
//   return keccak256(toUtf8Bytes(errorSignature)).slice(0, 10); // 0x + első 4 byte (8 hex karakter)
// }

onMounted(async () => {
tusdbalencee.value = await getTokenBalance();
tusdbalencee.value = parseFloat(tusdbalencee.value).toFixed(2);
intervalDown.value = parseFloat((props.price * 0.9).toFixed(2));
intervalUp.value = parseFloat((props.price * 1.1).toFixed(2));

// const errors = [
//   "Crypto_Stock_Exchange__InvalidInterval()",
//   "Crypto_Stock_Exchange__ZeroAmount()",
//   "Crypto_Stock_Exchange__TransferFailed()",
//   "Crypto_Stock_Exchange__NotAuthorized()",
//   "Crypto_Stock_Exchange__NotEnoughAllowance()",
//   "Crypto_Stock_Exchange__InvalidSignature()"
// ];

// errors.forEach(err => {
//   console.log(`${err} => ${getSelector(err)}`);
// });

 });

watchEffect(() => {
  if (tusdbalencee.value !== -1 && amount.value === 0) {
    amount.value = tusdbalencee.value;
  }
});

</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.modal-content {
  background: linear-gradient(145deg, #1e1e2f, #2c2c3d);
  color: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  width: 620px;
  max-width: 95%;
  max-height: 90vh; /* új: max magasság */
  overflow-y: auto;  /* új: görgethető, ha túl hosszú */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  text-align: center;
  margin-top: 60px;
}


h2 {
  margin-bottom: 2rem;
  font-size: 1.8rem;
  font-weight: 700;
}

h3 {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #e0e0e0;
  user-select: none;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

input[type='number'],
input[type='date'],
.eth-input {
  background: #1a1a2b;
  color: #fff;
  border: 2px solid #555;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  transition: 0.3s ease;
}

input[type='number']:focus,
input[type='date']:focus,
.eth-input:focus {
  border-color: #4facfe;
  outline: none;
  box-shadow: 0 0 8px #4facfe88;
}
small a{
  color: white;
}

.interval-group .interval-inputs {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.interval-inputs input {
  width: 110px;
}

.separator {
  color: #bbb;
  font-weight: bold;
}

.send-button {
  padding: 8px 16px;
  background: linear-gradient(to right, #43cea2, #185a9d);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s ease;
}

.send-button:hover {
  background: linear-gradient(to right, #36d1dc, #5b86e5);
}

.error {
  margin-top: 0.3rem;
  font-size: 0.875rem;
  color: #ff6b6b;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.confirm-btn,
.cancel-btn {
  padding: 0.75rem 2rem;
  font-weight: 700;
  border-radius: 10px;
  border: none;
  color: white;
  cursor: pointer;
  transition: 0.3s ease;
  font-size: 1rem;
}

.confirm-btn {
  background: linear-gradient(to right, #00c853, #64dd17);
}

.confirm-btn:hover {
  background: linear-gradient(to right, #00e676, #76ff03);
}

.cancel-btn {
  background: linear-gradient(to right, #ff1744, #d50000);
}

.cancel-btn:hover {
  background: linear-gradient(to right, #ff5252, #ff1744);
}

.wallet-info {
  background: linear-gradient(145deg, #1c1c1c, #2b2b2b);
  padding: 1.2rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  color: #f4f4f4;
  font-size: 1.1rem;
}

.wallet-row {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
}

.wallet-row .label {
  font-weight: 600;
  color: #c0c0c0;
}

.wallet-row .value {
  font-family: 'Courier New', Courier, monospace;
  color: #ffffff;
  word-break: break-all; /* ✅ kulcs a megoldáshoz */
  overflow-wrap: anywhere; /* alternatíva */
  padding: 0 0.3rem 0 0.3rem;
}

.test-funds-section {
  background: linear-gradient(145deg, #1c1c1c, #2b2b2b);
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  color: #fff;
  text-align: center;
}

.test-funds-section h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.test-funds-inputs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

input::-webkit-inner-spin-button,
input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

@media (max-width: 768px) {
.modal-content{
  margin-top: 0px;
}

}

</style>