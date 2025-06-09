<template>
  <div class="main-container pulsing-background">
    <section class="about-us-container">
<div class="text-content">
<h2>
  Bet on stock price intervals<br />
  with <span class="highlight">crypto</span> stay inside to win.
</h2>
  <p>
    Predict a price range for a stock, lock your crypto, and earn rewards if you're right. 
    But if the price breaks out of your range, you’ll start getting liquidated.  
    Liquidity flows from wrong bets to those who remain in the range.
  </p>
  <button onclick="document.querySelector('.how-it-works').scrollIntoView({ behavior: 'smooth' });">
    Learn How It Works
  </button>
</div>
      <div class="image-content">
        <img src="@/assets/logo.png" alt="Logo" />
      </div>
    </section>

  <section class="how-it-works">
  <div class="prediction-explainer">
    <h2>How It's Works</h2>
    <div class="underline"></div>

    <p>
      You <strong>predict a price range</strong> for a stock and <strong>lock your funds</strong> for a chosen period.
      As long as the stock price stays within your selected range, you <strong>earn rewards</strong>.
    </p>

    <p>
      If the price moves outside your chosen range, you will <strong>gradually lose part of your stake</strong>,<br>
      depending on how long the price remains outside during the lock-in period. This is known as <strong>liquidation</strong>
    </p>

    <p>
      Rewards are <strong>redistributed</strong> from users with inaccurate predictions to those who made better ones.
      The size of your reward depends on:
    </p>

    <p>
      <strong>How accurate</strong> your prediction is (narrower range = higher reward) <br>
      <strong>How long</strong> you commit your funds (longer = higher potential returns) <br>
      <strong>How much</strong> you risk (larger stakes = bigger reward share)
    </p>

    <p>
      The better you perform compared to others in these areas, the <strong>larger your share</strong> of the reward pool will be.
    </p>

    <p>
      You may withdraw early, but this comes with a <strong>significant fee</strong>.
      These fees are also distributed among users who remain accurate in their predictions.
    </p>

    <p>
      📘 Want the full breakdown?
      <a href="https://github.com/Gere321123/Crypto_Stock_Exchange" target="_blank">Read the complete documentation here</a>.
    </p>
  </div>
</section>
<section class="contact-us">
  <h2>Contact Us</h2>
  <p class="early-note">
    🚀 Our main goal is to integrate shares as best as possible in the Crypto world.<br><br>
    We're in an early phase and actively looking for supporters and investors. Let's build the future together.
  </p>

  <div class="contact-icons">
    <a href="https://github.com/Crypto-Stock-Exchange" target="_blank" class="icon-card">
      <img src="@/assets/github.svg" alt="GitHub" />
    </a>
    <a href="https://x.com/crypto_sto81104" target="_blank" class="icon-card">
      <img src="@/assets/x.svg" alt="X" />
    </a>
    <a href="mailto:gergely.cse@gmail.com" class="icon-card">
      <img src="@/assets/email.svg" alt="Email" />
    </a>
    <a href="https://www.linkedin.com/company/crypto-stock-exchange/about/?viewAsMember=false" target="_blank" class="icon-card">
      <img src="@/assets/linkedin.svg" alt="LinkedIn" />
    </a>
  </div>

  <p class="feedback-invite">
  💡 Want to help us improve the platform or share your ideas? <br />
  Fill out our short questionnaire <a href="https://github.com/Gere321123/Crypto_Stock_Exchange" target="_blank">here</a>.
</p>

</section>
  </div>
</template>


<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  color: white;
  min-height: 100vh;
}

.about-us-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  height: calc(100vh - 80px);
  overflow: hidden;
  z-index: 2;
}

.text-content {
  flex: 1;
  max-width: 50%;
  padding-right: 2rem;
  text-align: left;
}

.text-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.text-content p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  color: #ffffff;
}

.text-content button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.8rem 1.6rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.text-content button:hover {
  background-color: #059669;
}

.highlight {
  background-color: #b2f5ea;
  border-radius: 0.3em;
  padding: 0 0.2em;
  color: #111827;
}

.image-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-content img {
  width: 70%;
  height: auto;
}
.how-it-works {
  position: relative;
  margin: 0 auto;
  text-align: center;
  color: #e5e7eb;
}

.how-it-works h2 {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #ffffff;
  z-index: 1;
  position: relative;
}

.underline {
  width: 420px;
  height: 4px;
  background-color: #10b981;
  margin: 0 auto 2rem;
  border-radius: 2px;
}


.decor-left,
.decor-right {
  position: absolute;
  top: 0;
  width: 120px;
  opacity: 0.1;
  z-index: 0;
}

.decor-left {
  left: 0;
  top: 10%;
}

.decor-right {
  right: 0;
  bottom: 10%;
}

.decor-left img,
.decor-right img {
  width: 100%;
  height: auto;
}

.prediction-explainer {
  background-color: #ffffff;
  color: #333333;
  padding: 2.5rem 3rem;
  width: 100vw;
  margin: 25rem 0 25rem 0 ;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.prediction-explainer h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #111827;
}

.prediction-explainer p {
  font-size: 1.15rem;
  line-height: 1.8;
  margin-bottom: 1.3rem;
}


.prediction-explainer li {
  font-size: 1.1rem;
  margin-bottom: 0.6rem;
}

.prediction-explainer strong {
  color: #111827;
  font-weight: 600;
}

.prediction-explainer a {
  color: #2563eb;
  text-decoration: underline;
  font-weight: 500;
}

.contact-us {
  background: #1c1c1c;
  padding: 20rem 2rem;
  text-align: center;
  color: #fff;
}

.contact-us h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.early-note {
  font-size: 1.3rem;
  background: #292929;
  padding: 1rem 2rem;
  margin-bottom: 2rem;
  border-radius: 1rem;
  display: inline-block;
  max-width: 600px;
}

.contact-icons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.2rem;
  margin-bottom: 3rem;
}

.icon-card {
  width: 60px;
  height: 60px;
  background: #969696;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.icon-card:hover {
  transform: scale(1.1);
}

.icon-card img {
  width: 28px;
  height: 28px;
}

.feedback-invite {
  margin-top: 2rem;
  font-size: 1.3rem;
  color: #ccc;
}

.feedback-invite a {
  color: #00bfff;
  font-weight: bold;
  text-decoration: none;
}

.feedback-invite a:hover {
  text-decoration: underline;
}
@media (max-width: 768px) {
  .underline {
  width: 250px;
}
 .about-us-container {
    flex-direction: column;
    height: auto;
    padding: 1.5rem 1rem;
    gap: 2rem;
    text-align: center;
    margin-top: 3rem;
  }
    .text-content {
    max-width: 100%;
    padding-right: 0;
    text-align: center;
  }
  .prediction-explainer{
  margin: 5rem 0 5rem 0 ; ;
  }
  .contact-us {
  padding: 5rem 2rem;
}
}

</style>
