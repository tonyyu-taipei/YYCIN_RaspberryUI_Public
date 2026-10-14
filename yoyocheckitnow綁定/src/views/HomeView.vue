<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import { useRoute } from 'vue-router'
import { onMounted, watch, ref } from 'vue'
import axios from 'axios'
import { apiBaseUrl } from '../api'
const route = useRoute()
const email = ref('')
const password = ref('')
const bindingId = ref('')
const smartBoxId = ref('')
const pageNum = ref(0)
const accountType=ref('');
const patientId = ref(0);
onMounted(() => {
  bindingId.value = route.params.id
  smartBoxId.value = route.params.boxid

  console.log(route.params.id)
})

watch(
  () => route.params.id,
  (val) => {
    bindingId.value = val
  }
)
watch(()=> route.params.boxid, (val)=>{
  smartBoxId.value = val
})

const login = () => {
  pageNum.value = 1
  axios
    .post(`${apiBaseUrl}account/login`, {
      email: email.value,
      password: password.value,
    })
    .then((res) => {
      console.log(res)
      axios.get(`${apiBaseUrl}account/session`).then(resSession=>{
        accountType.value = resSession.data.accountType;
        console.log(resSession.data)
        if(accountType.value == "Caregiver"){
          //TODO: 跳轉到照護者頁面
          pageNum.value = 3;


        }
        if(accountType.value == "Patient"){
          axios
              .post(`${apiBaseUrl}smartbox/bind/${resSession.data.patient.patientID}`, {
                bindingId: bindingId.value,
                smartBoxId: smartBoxId.value,
              })
              .then(() => {
                alert('綁定成功')
                pageNum.value = 2
              })
              .catch(() => {
                alert('綁定失敗')
                pageNum.value = 0
              })
        }
      }).catch(()=>{
        alert('帳號或密碼錯誤')
        pageNum.value = 0
      })

    })
    .catch(() => {
      alert('帳號或密碼錯誤')
      pageNum.value = 0
    })
}
const caregiverBind = ()=>{
  axios
    .post(`${apiBaseUrl}smartbox/bind/${patientId.value}`, {
      bindingId: bindingId.value,
      smartBoxId: smartBoxId.value,
    })
    .then(() => {
      alert('綁定成功')
      pageNum.value = 2
    })
    .catch(() => {
      alert('綁定失敗')
      pageNum.value = 2
    })
}
</script>

<template>
  <main>
    <!-- <TheWelcome /> -->
    <div class="login" v-if="pageNum == 0">
      <div class="title">
        <h1>歡迎</h1>
        <p>請輸入病患帳戶的電子郵件以及密碼完成綁定。</p>
      </div>
      <div class="form-group">
        <label for="password" class="label">帳號：</label><br />
        <input type="text" id="email" v-model="email" required /><br />
        <label for="password" class="label">密碼：</label><br />
        <input type="password" id="password" v-model="password" required />
        <button @click="login">綁定</button>
      </div>
    </div>
    <div class="login" v-if="pageNum==1">
      <div class="title">
        <h1>請稍後</h1>
      </div>
    </div>
    <div class="login" v-if="pageNum==2">
      <div class="title">
        <h1>綁定成功</h1>
        <p>綁定成功，您可以離開本網頁了。</p>
      </div>
    </div>
    <div class="login" v-if="pageNum==3">
      <div class="title">
        <h1>藥盒綁定</h1>
        <p>請輸入您欲綁定的用藥者ID：</p>
        <input type="number" v-model="patientId" />
        <p>ID可於用藥者的手機App中查詢到。</p>
        <button @click="caregiverBind">綁定</button>

      </div>
    </div>

  </main>
</template>
<style scoped>
.login {
  /* 設定登入頁面的樣式 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100dvh;
  max-width: 100%;
  min-width: 300px;
  background-color: rgb(51, 63, 67);
  position: relative; /* 使 .bottom-container 相對於此定位 */
  padding-left: 20px;
}

.form-group {
  /* 讓標籤和輸入框在同一行 */
  align-items: center;
  margin-bottom: 20px; /* 調整間距 */
}

.label {
  /* 設定標籤(帳號：密碼：)的樣式 */
  font-size: 20px; /* 設定字體大小 */
  font-weight: bold; /* 設定字體粗體 */
  /* display: block; */
  margin-left: -10px; /* 向左移動 */
  margin-right: 10px; /* label和input調整間距 */
  margin-bottom: 10px;
  color: #f4f5ec;
}
.title {
  /* 設定標題(我的藥盒)的樣式 */
  font-size: 180%; /* 設定字體大小 */
  font-weight: bold; /* 設定字體粗體 */
  display: block;
  /* margin-bottom: 10px; */

  color: #f4f5ec;
}

button {
  /* 設定按鈕(登入按鈕)的樣式 */
  font-size: 100%; /* 設定字體大小 */
  font-weight: bold; /* 設定字體粗體 */
  display: block;
  margin-bottom: 10px;
  height: 50px;
  margin-top: 20px;
  font-size: 30px;
  background-color: #669b76;
  color: white;
  cursor: pointer;
  border-radius: 4px;
  transition:
    background-color 0.3s ease,
    transform 0.3s ease;
  padding-left: 20px;
  padding-right: 20px;
  border: none;
}
button:click {
  background-color: #dca580;
  transform: scale(1.05); /* 放大一點點 */
}

form {
  /* 將表單設置為 flex 布局，並沿著主軸方向進行排列。 */
  display: flex;
  flex-direction: column;
}

div {
  /* 每行的間距 */
  margin-bottom: 10px;
}

input {
  /* 設定輸入框的樣式 */
  display: block;
  width: 200px;
  height: 30px; /* 要比padding高 */
  margin-bottom: 20px;
  padding: 10px; /* 調整內邊距 */
  margin: 0 auto; /*置中 */
}

input[type='text'],
input[type='password'] {
  /* 設定輸入框的光暈 */
  padding: 10px;
  border: 1px solid #cccccc6c;
  border-radius: 4px;
  transition: box-shadow 0.3s ease;
}

input[type='text']:focus,
input[type='password']:focus {
  /* 設定輸入框的光暈 */
  outline: none;
  box-shadow: 0 0 10px 2px rgba(113, 109, 109, 0.584); /* 白色光暈 */
}

h1 {
  margin-top: 10px;
  margin-bottom: 60px;
  font-weight: bold;
}
p {
  font-size: 30px;
  font-weight: bold;
  margin-top: 5px;
  margin-bottom: 10px;
  color: #f4f5ec;
}
a {
  color: white;
  font-size: 19px;
  text-decoration: underline;
}
a:hover {
  color: #4977cd;
  cursor: pointer;
}
</style>
