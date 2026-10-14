<template>
    <div class="windowS" >
      <!-- <div class="title">設定</div> -->
      <!-- <button @click="$emit('changeWindow','Window1')" class="bottom-center">回去Window1</button> -->
      
        <div class="container">
          <!-- <button class="content" @click="showContent('content1')">ᯤ</button>  -->
          <button class="content" @click="showContent('content2')">帳戶</button>
          <button class="content" @click="showContent('content3')">綁定</button>
        </div>

        <div class="containerx">
          <div v-if="activeContent === 'content1'" class="contentx">網路設定</div>

          <div v-if="activeContent === 'content2'" class="contentx">藥盒識別碼
            <div class="content2-2">此識別碼將與您的帳戶連結：{{ smartBoxInfo.smartBoxID }} </div>
            <div class="content2-3">設定照護者 </div>
            <!-- <div class="content2-4">指定照護者來協助患者。 </div>
            <button class="button-caregiver info" @click="setup">開始設定</button> -->
          </div>

          <div v-if="activeContent === 'content3'" class="contentx">解除綁定
            <div class="content3-2">重新設定藥盒綁定資訊</div>
            <button class="unbind danger" @click="unbindMedBox">解除</button>
          </div>
        </div>
    </div>
  </template>
  
  
  <script setup>
  import axios from 'axios';
  import { apiBaseUrl } from '../api';
  import { ref, onMounted } from 'vue';
  import {storeToRefs} from "pinia";
  import {useMedboxStore} from "../../stores/medbox";
  const emits = defineEmits(['unbinded']);
  // onMounted(()=>{
  //   try{
  //     eel.get_id()((val)=>{
  //       deviceId.value = val
  //       console.log(val)
  //     })
  //   }catch(e){
  //     console.log(e)
  //   } 
  // });
  const medboxStore = useMedboxStore()
  const {smartBoxInfo} = storeToRefs(medboxStore)


  const activeContent = ref('');

  const showContent = (content) => {
    activeContent.value = content;
  };
  const unbindMedBox = async() => {
    const con = confirm("您確定要解除綁定？")
    if(con){
      try{
        const smartbox = await axios.get(apiBaseUrl + "smartbox/" + smartBoxInfo.value.smartBoxID)
        const bindingId = smartbox.data.bindingID;
        await axios.post(apiBaseUrl + "smartbox/unregisterbox/",{
          smartBoxID: smartBoxInfo.value.smartBoxID,
          bindingID: bindingId
        })
        emits("unbinded")
      }catch(e){
        console.log(e)
      }

    }
  }


  </script>
  
  <style scoped>
  .windowS {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color:rgb(51, 63, 67);
  }

  .title {
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    font-size: 60px;
    color: #ffffff;
    font-weight: bold;
  }


  .container {
    position: absolute;
    padding: 10px;
    top: 100px;
    left: 20px; 
    background-color: rgba(255, 255, 255, 0.265);
    border-radius: 10px; 
    width: 80px;
    height: 350px;
    display: flex;
    flex-direction: column;
    /* justify-content: space-between;  */
    align-items: center; /* 水平居中 */

  }

  .content {
    /* position: absolute; */
    /* text-align: center; */
    font-size: 30px;
    color: #ffffff;
    font-weight: bold;
    width: 60px; 
    height: 100px; 
    background-color: rgba(0, 0, 0, 0.5);
    border: none; 
    border-radius: 10px; 
    margin-bottom: 10px;
  }

  .containerx {
    padding: 10px; 
    background-color: rgba(255, 255, 255, 0.265);
    border-radius: 10px; 
    width: 780px;
    height: 450px;
    margin-left: 120px;
    bottom: 15px;

  }

  .contentx {
    position: absolute;
    /* text-align: center; */
    font-size: 50px;
    color: #ffffff;
    font-weight: bold;
  }
  .content2-2 {
    position: absolute;
    /* text-align: center; */
    font-size: 30px;
    color: #ffffff;
    white-space: nowrap; /* 禁止換行 */
    margin-top: 20px;
    font-weight: normal; /* 設置為正常字重 */
  }
  .content2-3 {
    position: absolute;
    /* text-align: center; */
    font-size: 50px;
    color: #ffffff;
    margin-top: 100px;
    font-weight: bold;
  }
  .content2-4 {
    position: absolute;
    /* text-align: center; */
    font-size: 30px;
    color: #ffffff;
    white-space: nowrap; /* 禁止換行 */
    margin-top: 170px;
    font-weight: normal; /* 設置為正常字重 */
  }

  .button-caregiver {
    position: absolute;
    /* text-align: center; */
    font-size: 30px;
    color: rgba(0, 0, 0, 0.8);
    font-weight: bold;
    width: 200px; 
    height: 60px; 
    background-color: rgba(255, 255, 255);
    border: none; 
    border-radius: 10px; 
    margin-top: 300px;
    margin-left: -250px;
  }

  .content3-2 {
    position: absolute;
    /* text-align: center; */
    font-size: 30px;
    color: #ffffff;
    white-space: nowrap; /* 禁止換行 */
    margin-top: 20px;
    font-weight: normal; /* 設置為正常字重 */
  }

  .unbind {
    position: absolute;
    /* text-align: center; */
    font-size: 30px;
    color: rgba(0, 0, 0, 0.8);
    font-weight: bold;
    width: 200px; 
    height: 60px; 
    background-color: rgba(255, 255, 255);
    border: none; 
    border-radius: 10px; 
    margin-top: 150px; 
    margin-left: -200px;
  }
  .danger{
    background-color: rgb(255, 86, 86)
  }
  .info{
    background-color: rgb(139, 128, 255)

  }
  </style>
