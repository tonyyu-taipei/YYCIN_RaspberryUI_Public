<template>
  <div class="window">
    <!-- {{medicationTimeStore.medicationTime}} -->
    <div class="bottom-container">
      <div class="medicationTime">用藥時間</div>
      <!-- 用藥時間 -->
       <div :key="key">
          <div class="currentMedicationTime">{{ currentMedTime }}</div>
        </div>
        <!-- <div class="missedMedication">08：00 未吃藥</div> -->
        <div class="nextMedicationTime">下次用藥時間 {{ nextMedTime }}</div>
    </div>

    <button :class="{'bottom2': true, 'active': showDetails}" @click="toggleDetails">詳細資料</button>
    <!-- <DetailsSAAM @sendData="receiveData" /> -->

        
        <!-- 詳細資料浮動式窗 -->
        <div v-if="showDetails" class="modal-overlay" @click="showDetails = false">
      <div class="modal-content" @click.stop>
        <!-- 顯示 DetailsSAAM 的浮動窗 -->
        <DetailsSAAM @sendData="receiveData" @close="showDetails = false" />
      </div>
    </div>

    <!-- 這裡顯示 DetailsW1 的資料 -->
    <DetailsW1
      v-if="showData"
      :startDate="startDate"
      :time1="time1"
      :time2="time2"
      :time3="time3"
      :time4="time4"
      :selectedBox="selectedBox"
      @changeWindow="toggleDetails"
    />

    
    <!-- 左下角的提醒按鈕 -->
    <button class="alert-button" @click="playAlertSound">提醒</button>
  </div>
</template>

<script setup>
// JavaScript

import { ref, onMounted, computed,defineProps,watch,reactive } from 'vue';
import DetailsSAAM from './DetailsSAAM.vue';
import DetailsW1 from './DetailsW1.vue';
const emit = defineEmits(['notify']);
const {audioShutUp} = defineProps(['audioShutUp']);
const audio = new Audio('https://taira-komori.jpn.org/sound_os2/animals01/dog1a.mp3');
import { useMedicationTimeStore } from '../../stores/medicationTime';
import { useMedboxStore } from '../../stores/medbox';
import axios from 'axios';
import { apiBaseUrl } from '../api';
import {storeToRefs} from "pinia";
const medicationTimeStore = useMedicationTimeStore(); //用藥時間
const medboxStore = useMedboxStore()
const {smartBoxInfo} = storeToRefs(medboxStore)
const showDetails = ref(false);
const showData = ref(false); // 用來控制顯示 DetailsW1
const startDate = ref('');
const time1 = ref('');
const time2 = ref('');
const time3 = ref('');
const time4 = ref('');
const selectedBox = ref('');
const currentMedTime = ref('無');
const nextMedTime = ref('無');




//偵測使用者關閉通知時，讓狗閉嘴
watch(()=>audioShutUp, (val)=>{
  if(val){
    audio.pause();
  }
})
//狗叫
const reminderCount = ref([]); // 用來記錄每個用藥時間的提醒次數
const hasAlerted = ref(false); // 用來標記是否已經播放過提醒聲音
const isFirstLoad = ref(true);  // 标志，防止第一次加载时触发提醒
let timerId = null; // 用來保存定時器 ID，方便後續清除

const toggleDetails = () => {
  showDetails.value = !showDetails.value;
};

const receiveData = (data) => { 
  startDate.value = data.startDate;
  time1.value = data.time1;
  time2.value = data.time2;
  time3.value = data.time3;
  time4.value = data.time4;
  selectedBox.value = data.selectedBox;
  showData.value = true; // 設定為 true 以顯示 DetailsW1
  console.log('Received data:', data);//用藥時間
};





//////////////////////////////////////////////////////

// 計算最近的用藥時間
const currentMedicationTime = () => {
  const now = new Date();
  const currentTime = now.getHours() * 60 + now.getMinutes();
  const times = medicationTimeStore.medicationTimes.map(time => {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  });

  // 返回最近的一個用藥時間
  const pastTimes = times.filter(time => time <= currentTime);
  const upcomingTimes = times.filter(time => time > currentTime);
  
  if (pastTimes.length > 0) {
    const closestTime = Math.max(...pastTimes); // 找到最大的過去時間
    const hours = Math.floor(closestTime / 60);
    const minutes = closestTime % 60;
    currentMedTime.value =  `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
  }else{
    currentMedTime.value = "無";
  }
  
  //currentMedTime.value = "無";
};

// 計算下次用藥時間
const getNextMedicationTime = () => {
  const now = new Date();
  const currentTime = now.getHours() * 60 + now.getMinutes();
  const times = medicationTimeStore.medicationTimes.map(time => {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  });

  const upcomingTimes = times.filter(time => time > currentTime);
  
  if (upcomingTimes.length > 0) {
    return Math.min(...upcomingTimes);
  }
  
  // 如果當天的用藥時間都過了，返回第二天的第一個用藥時間
  return times[0]; // 這裡需要確保 times 非空
};

const nextMedicationTime = () => {
  const nextTimeInMinutes = getNextMedicationTime();
  const hours = Math.floor(nextTimeInMinutes / 60);
  const minutes = nextTimeInMinutes % 60;
  nextMedTime.value =  `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
};
//////////////////////////////////

let notified = false
// 左下角的提醒按鈕
const playAlertSound = (index) => {
  
  audio.play();
  if(!notified){
    let timeTake = ""
    switch(index){
      case 0:
        timeTake = "morning";
        break;
      case 1:
        timeTake = "noon";
        break;
      case 2:
        timeTake = "evening";
        break;
      case 3:
        timeTake = "beforebed";
        break;
    }

    emit('notify', medicationOnTime[timeTake]);
    notified = true;
  }
};

const currentDate = ref('');//更新日期
const currentTime = ref('');//更新時間

const updateDate = () => {//更新日期
  const now = new Date();
  currentDate.value = now.toLocaleDateString('zh-TW', {
    //year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
};

const updateTime = () => {//更新時間
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-TW', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

//各項時間需要服用之藥物
const medicationOnTime = reactive({
  morning: [],
  noon: [],
  evening: [],
  beforebed: [],
  whenneeded:[]
})
onMounted(() => {
  axios.get(`${apiBaseUrl}prescription/medbox/${smartBoxInfo.value.smartBoxID}`).then((response) => {
    console.log(response.data);

     // 取出今天 早、中、晚、睡前 的用藥時間的藥物ID
      const today = new Date();
      for(let prescriptions of response.data){
        for(let medicationDetail of prescriptions.medicationDetails){
          const startDate = new Date(medicationDetail.startDate);
          const endDate = new Date(medicationDetail.endDate);
          if(today >= startDate && today <= endDate){
            if(medicationDetail.takeAfterBreakfast){
              medicationOnTime.morning.push(medicationDetail.medication.medicationId);
            }
            if(medicationDetail.takeAfterLunch){
              medicationOnTime.noon.push(medicationDetail.medication.medicationId);
            }
            if(medicationDetail.takeAfterDinner){
              medicationOnTime.evening.push(medicationDetail.medication.medicationId);
            }
            if(medicationDetail.takeBeforeBed){
              medicationOnTime.beforebed.push(medicationDetail.medication.medicationId);
            }
            if(medicationDetail.takeWhenNeeded){
              medicationOnTime.whenneeded.push(medicationDetail.medication.medicationId);
            }
          }
        }
      }
  });
  // 初始化每個用藥時間的提醒次數為 0
  medicationTimeStore.medicationTimes.forEach(() => {
    reminderCount.value.push(0);
  });

  setInterval(() => {
    currentMedicationTime();
    nextMedicationTime();
    const now = new Date();
    const currentTimeInMinutes = now.getHours() * 60 + now.getMinutes();

    // 檢查每個用藥時間
    medicationTimeStore.medicationTimes.forEach((time, index) => {
      const [hours, minutes] = time.split(':').map(Number);
      const medicationTimeInMinutes = hours * 60 + minutes;

      // 如果當前時間到達用藥時間，並且提醒次數小於 2，則播放提醒
      if (currentTimeInMinutes === medicationTimeInMinutes && reminderCount.value[index] < 3 &&!audioShutUp) {
        if (!isFirstLoad.value) {
          // 如果是第一次加载，避免触发提醒
          playAlertSound(index);
        }
        reminderCount.value[index] += 1; // 增加對應的提醒次數


      }else{
        notified = false;
      }
    });

    // 第一次加载时设置标志，避免触发提醒
    if (isFirstLoad.value) {
      isFirstLoad.value = false;
    }

  }, 1000); // 每秒檢查一次時間
});
</script>

<style scoped>
/* CSS */
.window {
  width: 100dvw;
  height: 100dvh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(48, 53, 58);
  position: relative; /*bottom-center????*/
  overflow: hidden;
  padding:0;
  margin: 0;
}

.bottom-container {
  /* position: relative; */
  margin-top: -25px;
  padding: 50px; /* 設置內距 */
  background-color: rgba(255, 255, 255, 0.265); /* 設置背景顏色 */
  border-radius: 10px; /* 設置圓角 */
  /* align-items: center; */
  width: 280px; /* 設置寬度 */
  height: 50px;
  max-width: 500px; /* 設置最大寬度 */
}



.bottom-center {
  position: absolute;
  bottom: 0;
  left: 0%;
  transform: translateX(-50%);
}
.bottom2 {
  position: absolute;
  bottom: 20px;
  margin: 0 auto;  /*置中 */
  font-weight: bold; /* 設定字體粗體 */
  font-size: 32px;
  width: 160px;
  height: 50px;
  padding: 0px;
  border: 4px solid rgb(143, 143, 143); /* 添加邊框 */
  background-color: rgb(48, 53, 58);
  color: rgb(244, 245, 236);
  cursor: pointer; /* 設定滑鼠樣式 */
  border-radius: 10px;
}
.bottom2.active {
  background-color: rgb(244, 245, 236); /* 點擊後的背景顏色 */
  color: rgb(65, 72, 96); /* 點擊後的文字顏色 */
}
.medicationTime {
  position: absolute;
  top: 90px; /* 調整這個值來控制偏上程度 */
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center; /* 文字居中 */
  font-size: 60px;
  color: rgb(244, 245, 236);
  font-family: 'Arial Black', sans-serif;
  font-weight: bold;
    
}
.currentMedicationTime {
  position: absolute;
  top: 250px; /* 調整這個值來控制偏上程度 */
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center; /* 文字居中 */
  font-size: 90px;
  color: rgb(244, 245, 236);
  font-family: 'Arial Black', sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* .missedMedication {
    position: absolute;
    bottom: 20%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    font-size: 20px;
    color: #ffffff;
    font-family: 'Arial Black', sans-serif;
    font-weight: bold;
} */
.nextMedicationTime {
    position: absolute;
    bottom: 65px;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center; /* 文字居中 */
    font-size: 47px;
    color: rgb(244, 245, 236);
    font-family: 'Arial Black', sans-serif;
    font-weight: bold;
}
/* 詳細資料背景遮罩 */
.modal-overlay { 
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.alert-button {
  position: absolute;
  bottom: 20px;
  left: 20px;
  padding: 10px 20px;
  font-size: 20px;
  font-weight: bold;
  background-color: rgb(48, 53, 58);
  color: rgb(48, 53, 58);
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* .modal-content { 
  background-color: white;
  padding: 80px 50px;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1001;
} */

</style>