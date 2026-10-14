<template>
    <div class="window" >
      <h1>藥槽狀態</h1>

    <!-- 設定所有藥槽按鈕 -->
    <button @click="showSetAllAM = true" class="SetAll">設定所有藥槽</button>

    <!-- 彈出包含編輯和詳細資料的選項視窗 -->
    <div v-if="showSetAllAM" class="modal-overlay" @click="showSetAllAM = false">
        <button @click="openEdit" class="option-button">編輯</button>
        <!-- <button :class="{'detailsSAAM': true, 'active': showDetails}" @click="toggleDetails">詳細資料</button> -->
        <!-- 直接顯示詳細資料內容 -->
        <div>
          <DetailsSAAM 
            :startDate="startDate" 
            :time1="time1" 
            :time2="time2" 
            :time3="time3" 
            :time4="time4"
            @changeWindow="handleClose('showSetAllAM')" 
          />
        </div>
    </div>

    <!-- 顯示 SetAllAM 組件 -->
    <div v-if="showEdit" class="modal-overlay" @click="showEdit = false">
      <div class="modal-content" @click.stop>
        <SetAllAM @updateMedicationTime="updateMedicationTime" @close="handleClose('showEdit')" />
      </div>
    </div>

    <!-- 詳細資料浮動式窗 -->
    <div v-if="showDetails" class="modal-overlay" @click="toggleDetails">
      <div class="modal-content" @click.stop>
        <DetailsSAAM 
        :startDate="startDate" 
          :time1="time1" 
          :time2="time2" 
          :time3="time3" 
          :time4="time4"
        @changeWindow="toggleDetails" />
      </div>
    </div>


      <div class="temp-container">
        <div class="temp-block">
          <!-- <p>藥盒濕度</p> -->
          <status  :class="{'status-good':statusHumid=='良好', 'status-bad':statusHumid!='良好'}">{{ statusHumid }}</status>
                    <h3>{{ currentHumid.toFixed(1) }}%</h3>
        </div>
      <div class="temp-block">
        
          <!-- <p>藥盒溫度</p> -->
          <status :class="{'status-good':statusTemp=='良好', 'status-bad':statusTemp!='良好'}">
           {{ statusTemp }} 
           </status>
          <h3>{{ currentTemp.toFixed(1) }}°C</h3>
          </div>

        </div>


    <!-- 那8格藥盒 -->
      <MedBox class="innermed" :medBoxReactive="medBoxReactive" @showDialog="showDialog"  :hide-status=false :blink="blink" :key="updateKey"></MedBox>

    <!-- 浮動框 -->
      <!-- <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <h3>藥槽 {{ selectedBoxIndex }} 藥品</h3>
          <p>名稱: {{ selectedDrug.name }}</p>
          <p>數量: {{ selectedDrug.amount }}</p>
          <button @click="openEditDialog">修改藥物資訊</button>
        </div>
      </div> -->
      
    </div>
  </template>
  


<script setup>
import { ref, defineProps, watch, watchEffect, reactive } from 'vue';

//Store/Medbox，讀取全域的藥盒資料，需要下面這兩行
import {useMedboxStore} from "../../stores/medbox";
import {storeToRefs} from "pinia";
// import { useUsageLogStore } from '@/stores/usageLog';
//
import { useMedicationTimeStore } from '../../stores/medicationTime';
import SetAllAM from './SetAllAM.vue';
import DetailsSAAM from './DetailsSAAM.vue';
import MedBox from './MedBox.vue';
import axios from 'axios';
import { apiBaseUrl } from '../api';
const updateKey = ref(0);
const medicationTimeStore = useMedicationTimeStore();

const updateMedicationTime = (newTime) => {
  medicationTimeStore.setMedicationTime(newTime);
};

// 設定所有藥槽按鈕
const showSetAllAM = ref(false);
const showEdit = ref(false);
const showSingleAM = ref(false);
const showDetails = ref(false);
const toggleDetails = () => {
    showDetails.value = !showDetails.value;
};

// 顯示 SetAllAM 組件
const openEdit = () => {
  showSetAllAM.value = false;
  showEdit.value = true;
};

// 開啟詳細資料視窗
// const openDetails = () => {
//   showSetAllAM.value = false;
//   showDetails.value = true;
// };

const blink = reactive({
  '1':{Amount:1, Blink:false},
  '2':{Amount:0, Blink: false},
  '3':{Amount:0, Blink: false},
  '4':{Amount:0, Blink: false},
  '5':{Amount:1, Blink: false},
  '6':{Amount:0, Blink: false},
  '7':{Amount:1, Blink: false},
  '8':{Amount:0, Blink: false},

})
// 關閉視窗的邏輯
const handleClose = (windowName) => {
  if (windowName === 'showEdit') {
    showEdit.value = false;
  } else if (windowName === 'showSingleAM') {
    showSingleAM.value = false;
  } else if (windowName === 'showDetails') {
    showDetails.value = false;
  }
};

// 使用藥盒全域的資訊
const medboxStore = useMedboxStore()
// 讓store -> ref
const {smartBoxInfo} = storeToRefs(medboxStore)

// const usageLogStore = useUsageLogStore();
// 獲取所有紀錄
// const logs = usageLogStore.getUsageLogs(); 

// 由App.vue傳入之數值：目前溫濕度
//const props = defineProps(['temp', 'humid']);
const {temp, humid} = defineProps(['temp','humid']);
//本地數值：目前溫濕度狀態
const currentTemp = ref(0);
const currentHumid = ref(0)

const medContainer = reactive([])

const statusTemp = ref('良好');
const statusHumid = ref('良好');


// 顯示修改藥物資訊視窗
const showEditDialog = ref(false);

const showModal = ref(false);

// 藥槽的資料
const selectedBoxIndex = ref(null);
const selectedDrug = reactive({ name: '', amount: 0 });

const showDialog = (obj)=>{
selectedBoxIndex.value = obj.index;
selectedDrug.name = obj.drug.name;
selectedDrug.amount = obj.drug.amount;
if (selectedDrug.name !== '空') {
  showModal.value = true;
}
}



// 顯示修改藥物資訊視窗
const editDrugInfo = () => {
showEditDialog.value = true;
};

// 保存藥物資訊變更
// const saveChanges = () => {
// medBoxReactive[selectedBoxIndex.value].name = selectedDrug.name;
// medBoxReactive[selectedBoxIndex.value].amount = selectedDrug.amount;
// showEditDialog.value = false;
// };

// 打開藥物修改視窗
const openEditDialog = () => {
  showEditDialog.value = true;
};
// 關閉修改視窗
const closeEditDialog = () => {
  showEditDialog.value = false;
};


const medBoxReactive = reactive({
  '1': {name: '空', amount: 0, id: 0},
  '2': {name: '空', amount: 0, id: 0},
  '3': {name: '空', amount: 0,  id: 0},
  '4': {name: '空', amount: 0, id: 0},
  '5': {name: '空', amount: 0, id: 0},
  '6': {name: '空', amount: 0, id: 0},
  '7': {name: '空', amount: 0,  id: 0},
  '8': {name: '空', amount: 0, id: 0},

})

const getAllBoxMed = ()=>{
  if (!smartBoxInfo.value.smartBoxID) return;
  axios.get(`${apiBaseUrl}SmartBoxMedication/smartboxid/${smartBoxInfo.value.smartBoxID}`).then(res=>{
updateKey.value++
console.log(res.data)
res.data.forEach((item)=>{
  if(item.medication != null){
    medBoxReactive[item.pos].name = item.medication.name
    medBoxReactive[item.pos].amount = item.quantity
    medBoxReactive[item.pos].id = item.medication.medicationId
  }else{
    medBoxReactive[item.pos].name = '空'
    medBoxReactive[item.pos].amount = 0
  }
  medboxStore.resetSmartBoxMedication()
  medboxStore.addMedicationObj(medBoxReactive)
})
})
}
watch(() => smartBoxInfo.value.smartBoxID, (id) => {
  if (id) getAllBoxMed();
}, { immediate: true });



const closeModal = () => {
  showModal.value = false;
};

const selectDrug = (drug) => {
  selectedDrug.value = drug;
  console.log(`選擇的藥品: ${drug.name}`);
  closeModal();
};

// watchEffect: 當temp與humid的數值有改變時，更新本地的溫濕度狀態
watchEffect(()=>{
  currentTemp.value = temp;
  currentHumid.value = humid;
  if(currentTemp.value>30){
    statusTemp.value = '過高';
  }else{
    statusTemp.value = '良好';
  }
  if(currentHumid.value>70){
    statusHumid.value = '過高';
  }
})

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



  </script>
  
  <style scoped>
  h1{
    margin:40 0 10 10;
    display:inline-block;
    width:255;

  }
  .window {
    width: 100dvw;
    height: 100dvh;
    background-color: rgb(48, 53, 58);
    font-size: 30px;
    color: rgb(244, 245, 236);
    position: relative; /*bottom-center*/
  }
  .bottom-center {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }
  .temp-block{
    margin-top:40;
    width:190px;
    height:50px;
    padding-left:5;
    margin:8;
    background-color:rgb(244, 245, 236);
    border-radius: 10px;
    color: rgb(48, 53, 58);
    float:left;
    display:inline-flex;
    justify-content: center;
    align-items: center;

  }
  .temp-block h3{
    margin:0;
    display:inline-block;
    height:100%;
    vertical-align: middle;
    line-height:48px
  }
  .temp-container{
    float:right;
    margin:40 10 0 0
  }


  /* 設定所有藥槽按鈕 */

  .SetAll {
    font-weight: bold;
    font-size: 35px;
    width: 250px;
    height: 60px;
    border-radius: 10px;
  }

  .SetAll {
    position: absolute;
    top: 43px;
    background-color: rgb(242, 241, 215);
    border: 3px solid rgb(176, 93, 63);
    color: rgb(65, 72, 98);
  }

  /* 浮動視窗的背景遮罩 */
  .modal-overlay, .modal-overlay2 {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  /* 視窗內容 */
  .modal-content {
    background-color: white;
    color: black;
    padding: 20px; 
    border-radius: 20px;
    text-align: center;
  }

  /* 編輯按鈕 */
  .option-button {
    /* display: block; */
    position: fixed;
    bottom: 20px;
    right: 20px;
    margin: 30px;
    padding: 20px 30px;
    font-size: 30px;
    font-weight: bold;
    background-color: rgb(242, 241, 215); /* 背景顏色 */
    color: rgb(65, 72, 96); /* 文字顏色 */
    border: none; /* 移除邊框 */
    border-radius: 10px; /* 圓角 */
    border: 4px solid rgb(143, 143, 143); /* 添加邊框 */
  }

  /* 詳細資料按鈕 */
  .detailsSAAM {
    /* position: absolute; */
    /* top: 170px; */
    /* right: 170px; */
    /* font-family: 'Arial Black', sans-serif; */
    margin: 30px;
    padding: 20px 30px;
    font-size: 30px;
    font-weight: bold;
    background-color: rgb(65, 72, 96); /* 背景顏色 */
    color: #ffffff; /* 文字顏色 */
    border: none; /* 移除邊框 */
    border-radius: 5px; /* 圓角 */
  }
    
  /* 詳細資料按鈕的激活狀態 */
  .detailsSAAM.active {
    background-color: rgb(244, 245, 236); /* 點擊後的背景顏色 */
    color: rgb(65, 72, 96); /* 點擊後的文字顏色 */
  }
  .innermed{
    width:100%;
    margin-top: 20px;
  }
  status{
    display:inline-block;
    font-size:23;
    border-radius:10px;
    padding:5px;
    margin-right:10px
    }
  .status-good{
    background-color:rgb(152, 200, 152);
  }
  .status-bad{
    background-color:rgb(243, 139, 139);
  }

  </style>
