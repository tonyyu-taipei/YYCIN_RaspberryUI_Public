<template>
    <div class="login">
      <div v-if="pageNum == 0">
        <div class="title">
          <h1>歡迎</h1>
        </div>
        <p>請點擊下方按鈕以向我們註冊此藥盒</p>
        <button @click="registerMedBox">註冊藥盒</button>
      </div>
      <div v-if="pageNum == 2">
        <div class="title">
        <h1>綁定帳號</h1>
        </div>
        <p>請使用手機App掃描下方QR Code</p>
        <div class="center">
        <qrcode-vue :value="qrcode" size="200" level="H" />
        </div>


      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, watch } from 'vue';
  import {ElLoading, ElNotification} from 'element-plus';
  import axios from 'axios';
  import QrcodeVue from 'qrcode.vue';


  const pageNum = ref(0);
  const qrcode = ref('');

  const {medbox, serverURL, bindingMode} = defineProps(['medbox',"serverURL","bindingMode"]);
  const loading =  ElLoading.service({
      lock: true,
      text: '載入中',
      background: 'rgba(0, 0, 0, 0.7)'
    })


  // Loading畫面
  onMounted(()=>{
    loading.close();
    if(bindingMode == 1){
      pageNum.value = 2;
    }
    if(bindingMode == 0){
      pageNum.value = 0;
    }

  })
  watch(()=>medbox.bindingID,(val)=>{
    loading.close();
    qrcode.value = serverURL+medbox.bindingID+"/"+medbox.smartBoxID;
  })
  watch(()=>bindingMode, val=>{
    if(val == 1){
      pageNum.value = 2;
    }
    if(val == 0){
      pageNum.value = 0;
    }
  })
  const registerMedBox = ()=>{
    console.log(medbox)
    loading;
    axios.post(serverURL+"smartbox/registerbox",{
      "smartBoxID": medbox.smartBoxID,
      "location":""
    }).then((res)=>{
      console.log(res)
      pageNum.value = 2;
      loading.close();
    }).catch((e)=>{
      console.error(e);
      loading.close();

      ElNotification({
        title: '錯誤',
        message: '註冊失敗，請稍候重試或告知管理員',
        type: 'error'
      })
    })
  }


  </script>
  

  <style scoped>
  .login { /* 設定登入頁面的樣式 */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100dvh;
    width:100dvw;
    background-color:rgb(51, 63, 67);
    position: relative; /* 使 .bottom-container 相對於此定位 */
  }

  .form-group { /* 讓標籤和輸入框在同一行 */
    display: flex;
    align-items: center;
    margin-bottom: 20px; /* 調整間距 */
  }

  .label {  /* 設定標籤(帳號：密碼：)的樣式 */
    font-size: 100%; /* 設定字體大小 */
    font-weight: bold; /* 設定字體粗體 */
    /* display: block; */
    margin-left: -10px; /* 向左移動 */
    margin-right: 10px; /* label和input調整間距 */
    margin-bottom: 10px;
  }
  .title {  /* 設定標題(我的藥盒)的樣式 */
    font-size: 180%; /* 設定字體大小 */
    font-weight: bold; /* 設定字體粗體 */
    display: block;
    /* margin-bottom: 10px; */

    color: #F4F5EC;
  }

  button {   /* 設定按鈕(登入按鈕)的樣式 */
    font-size: 100%; /* 設定字體大小 */
    font-weight: bold; /* 設定字體粗體 */
    display: block;
    margin-bottom: 10px;
    height:50px;
    margin-left:20px;
    margin-right:20px;
    font-size:30px;
    background-color: #669b76;
    color: white;
    cursor: pointer;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }
  button:click {
    background-color: #dca580;
    transform: scale(1.05); /* 放大一點點 */
  }

  form {  /* 將表單設置為 flex 布局，並沿著主軸方向進行排列。 */
    display: flex;
    flex-direction: column;
  } 
  
  div { /* 每行的間距 */
    margin-bottom: 10px;
  }


  input {   /* 設定輸入框的樣式 */
    /* display: block; */
    width: 200px;
    height: 30px;  /* 要比padding高 */
    margin-bottom: 20px;
    padding: 10px; /* 調整內邊距 */
    margin: 0 auto;  /*置中 */
  }

  input[type="text"], input[type="password"] { /* 設定輸入框的光暈 */
    padding: 10px;
    border: 1px solid #cccccc6c;
    border-radius: 4px;
    transition: box-shadow 0.3s ease;
  }

  input[type="text"]:focus, input[type="password"]:focus { /* 設定輸入框的光暈 */
    outline: none;
    box-shadow: 0 0 10px 2px rgba(113, 109, 109, 0.584); /* 白色光暈 */
  }

  button {  /* 設定按鈕的樣式 */
    width: 30%;
    padding: 0.8px;
    margin: 0 auto;  /*置中 */
    border: none; /* 移除框線 */


  }
  h1{
    margin-top:10px;
    margin-bottom:60px;
  }
  p{
    font-size: 30px;
    font-weight: bold;
    margin-top:5px;
    margin-bottom:10px;
    color: #F4F5EC;
  }
  a{
    color:white;
    font-size:19px;
    text-decoration: underline;

  }
  a:hover{
    color: #4977cd;
    cursor:pointer;
  }
  </style>