import {createApp} from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhTw from 'element-plus/es/locale/lang/zh-tw'


//import router from './router/index'
const pinia = createPinia()


const app = createApp(App)
app.use(ElementPlus,{
    locale: zhTw,
  })
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(pinia).mount("#app")