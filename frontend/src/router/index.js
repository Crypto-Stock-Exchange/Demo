import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/components/HomePage.vue'
import StocksPage from '@/components/StocksPage.vue'
import StockDetails from '@/components/StockDetails.vue'
import AboutUs from '@/components/AboutUs.vue'
import MyBets from '@/components/MyBets.vue'

import makeContract from '@/services/makeContract';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/stocks', name: 'Stocks', component: StocksPage },
  { path: '/about-us', name: 'About Us', component: AboutUs },
  { path: '/my-bets', component: MyBets, meta: { requiresNFT: true } },
  { path: '/stock/:id', name: 'StockDetails', component: StockDetails, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresNFT) {
    if (makeContract.myBetsVisible.value) {
      next();
    } else {
      next('/');
    }
  } else {
    next();
  }
});

export default router;
