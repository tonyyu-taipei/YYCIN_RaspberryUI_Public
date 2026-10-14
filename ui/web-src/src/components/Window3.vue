<template>
    <div class="window" >
      <div class="personalInformation">用藥者資訊</div>
        <!-- <h1>個人資訊(吃藥時間、用藥類別、其他...資料庫)</h1> -->

      <div class="main-container">

        <!-- 固定在左邊的個人資訊容器 -->
        <div class="container">
          <!-- <div class="content">姓名：{{ smartBoxInfo.patientID.name }}
            <p>性別：{{ gender}}</p>
            <p>年齡：{{ smartBoxInfo.patientID.age }}歲</p>
            <p>手機：{{ smartBoxInfo.patientID.phoneNumber }}</p>
          </div> -->
        </div>

        <!-- 可滾動的框區域 -->
        <div class="scrollable-boxes" @touchmove="boxOnTouch" @touchend="boxOffTouch" ref="scrollboxRef">
          <div class="additional-boxes">

            <!-- <div class="box">
            <Window1 />
            </div> -->
            
            <!-- <div class="box" ></div> -->
          </div>
        </div>

      </div>
    </div>
</template>
  

<script setup>
  import { ref, computed, watchEffect } from 'vue';

import {storeToRefs} from "pinia";
import {useMedboxStore} from "../../stores/medbox";
const medBoxStore = useMedboxStore()
const {smartBoxInfo} = storeToRefs(medBoxStore)
const gender = ref("載入中");
// const smartBoxInfo = reactive({
//   "smartBoxID": smartBoxInfo.smartBoxID,
//     "location": "",
//     "patientID": null,
//     "bindingID": null,
//     "smartBoxMedications": null
// })

  // import Window1 from './Window1.vue';

  const emit = defineEmits(['ignoreChangePage']);
  const scrollboxRef = ref(null);

  function boxOnTouch(){
    var policyElement = scrollboxRef.value;
    if(policyElement.scrollLeft == 0)return
    emit('ignoreChangePage',true)
  }
  function boxOffTouch(){
    setTimeout(()=>{
      emit('ignoreChangePage',false)
    },300)
  }
  watchEffect(()=>{
    if(smartBoxInfo.value.patientID){
      switch(smartBoxInfo.value.patientID.gender){
        case 0:
          gender.value = "女";
          break;
        case 1:
          gender.value = "男";
          break;
          case 2:
            gender.value = "其他";
            break;
        default:
        gender.value = "未知";
      }
    }
  }) 
  </script>
  
  <style scoped>
  
  .window {
    width: 100dvw;
    height: 100dvh;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    background-color: rgb(48, 53, 58);
  }
  .personalInformation {
    position: absolute;
    top: 40px; 
    left: 20px;
    font-size: 60px;
    color: rgb(244, 245, 236);
    font-weight: bold; 
  }

  .main-container {
    display: flex;
    /* align-items: flex-start;  */
    align-items: center;
    gap: 20px; /* 容器之間的間距 */
    margin-top: 80px;
  }

  /* 固定在左邊的個人資訊區域 */
  .container {
    /* position: relative; */
    /* margin-top: 10px; */
    /* margin-top: 80px;  */
    /* margin-left: -580px;  */
    position: fixed;
    padding: 20px; 
    background-color: rgba(255, 255, 255, 0.265);
    border-radius: 10px; 
    width: 280px;
    height: 350px;

  }

  .content {
    font-size: 30px;
    color: rgb(244, 245, 236);
    font-weight: bold; 
  }

  /* 可滾動的框區域 */
  .scrollable-boxes {
    margin-left: 300px; /* 為了避開左邊固定的 .container */
    width: calc(100vw - 320px); /* 減去 .container 的寬度 */
    overflow-x: auto; /* 允許橫向滾動 */
    overflow-y: hidden; /* 隱藏垂直滾動，避免觸發換頁滾動 */
    white-space: nowrap; /* 確保子元素不會換行，觸發橫向滾動 */
    position: relative; /* 確保這個區域在滾動時不影響其他區域 */
    scroll-behavior: smooth; /* 平滑滾動 */
  }

  /* 避免滾動穿透 */
  .scrollable-boxes::-webkit-scrollbar {
    height: 8px; /* 調整滾動條的高度 */
  }

  /* 內部框的排列方式 */
  .additional-boxes {
    display: flex;
    gap: 10px; /* 框之間的間距 */
    padding: 10px;
  }

  /* 單個框樣式 */
  .box {
    width: 400px;
    height: 360px;
    background-color: rgba(25, 25, 25, 0.5);
    color: white;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    /* border: 1px solid #ccc; */
    border-radius: 10px;
    flex-shrink: 0; /* 防止框縮小 */
  }
  </style>