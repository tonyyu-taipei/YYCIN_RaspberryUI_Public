<template>
  <div class="app">
    <!-- 登入畫面 -->
    <Login 
      v-if="!isLoggedIn || binded!=2" 
      @login-success="handleLoginSuccess" 
      :medbox="smartBoxInfo" 
      :serverURL="serverURL" 
      :bindingMode="binded" 
    />

    <div class="display-top">
      <!-- 顯示當前日期與時間 -->
      <div class="date-display">{{ currentDate }}</div>
      <!-- 當藥盒開啟時，有個綠色點點不斷放大縮小提醒使用者目前是開啟狀態 -->
       <div class=circlegreen v-if="!boxClosed"></div>
        <div class=circlered v-if="indentificationLock">

       </div>
      <div class="indicator-display">{{ indicatorText }}</div>

      <div class="time-display">{{ currentTime }}</div>
    </div>

    <!-- 主要頁面 -->
    <div v-if="isLoggedIn && binded==2">
      <!-- 動態切換頁面 -->
      <component :is="page" />
      
      <!-- 顯示功能頁面及底部功能列 -->
      <div @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd">
        <keep-alive>
          <Window1 v-if="page === 'Window1'" @changeWindow="addPage" @notify="notifyAndShowMed" :audioShutUp="audioShutUp"/>
        </keep-alive>

        <Window2 v-if="page === 'Window2'" :humid="currentHumid" :temp="currentTemp" @changeWindow="addPage" :key="idKey"/>


        <!-- <Window3 v-if="page === 'Window3'" @changeWindow="addPage" @ignoreChangePage="ignoreChangeHandler"/> -->
        <NotificationWindow v-if="page === 'Notifications'" @changeWindow="addPage" :notificationId="notificationId" @closeNotifyWindow="closeNotification" :idsToNotify="notifyIds"/>
        <!-- 功能列按鈕 -->
        <div v-if="currentViewComponent" class="fullscreenComponent">
          <component :is="currentViewComponent" @ignoreChangePage="ignoreChangeHandler" @unbinded="restartTestRegistered" :serverURL="serverURL"></component>
        </div>

        <!-- 功能列與其按鈕 -->
        <div v-if="showBottomBar" class="dark-overlay" @click="showBottomBar = false">
          <div :class="['bottom-bar', { 'show': showBottomBar }]">
            <!-- <button @click="handleChangeView('AddMedication')">藥物新增</button> -->
            <!-- <button @click="handleChangeView('DataStatistics')">資料統計</button> -->
            <button @click="handleChangeView('MedicationTracking')">用藥追蹤</button>
            <button @click="handleChangeView('')">主畫面</button>
            <button @click="handleChangeView('Settings')">設定</button>
          </div>
        </div>

        <!-- 右側未吃藥提醒 -->
        <!-- <div v-if="page == 'Window1' || page == 'Window2' || page == 'Window3'" class="rectangle" :class="{ 'open': isRectangleOpen }">
          <div class="square" @click="toggleRectangle">
            <span>!</span>
          </div>
          <div v-if="page === 'Window1'" class="medication-list">
            <div><p>08：00 未吃藥</p></div>
            <div class="medicationTime">用藥時間</div>
          </div>
        </div> -->

        <!-- 功能列觸發按鈕 -->
        <!-- <button class="sidebar-button" @click="toggleBottomBar" v-if="isLoggedIn && binded">功能</button> -->
      </div>

      <!-- 當前頁面是 Window2 時顯示按鈕 -->
      <!-- <button v-if="page === 'Window2'" @click="showNotification" class="notification-button">顯示通知</button> -->
    </div>

    <!-- 浮動通知頁面 -->
    <div v-if="showNotificationPage" class="notification-overlay">
      <div class="notification-content">
        <p>拍攝藥物中...</p>
        <p>請勿打開藥盒</p>
        <!-- <button @click="closeNotification">OK</button> -->

      </div>
    </div>

  </div>
</template>
<script setup>
//伺服器URL
const serverURL = ref(apiBaseUrl);
import { ref, computed,onMounted, reactive,watch } from 'vue';
import { apiBaseUrl } from './api';
import Window1 from './components/Window1.vue';
import Window2 from './components/Window2.vue';
import Window3 from './components/Window3.vue';
import Login from './components/Login.vue';
import AddMedication from './components/AddMedication.vue';
import DataStatistics from './components/DataStatistics.vue';
import MedicationTracking from './components/MedicationTracking.vue';
import Settings from './components/Settings.vue';
import NotificationWindow from './components/NotificationWindow.vue';
import axios from 'axios';
import {storeToRefs} from "pinia";
import {useMedboxStore} from "../stores/medbox";
import {useNotificationStore} from "../stores/notification";
import { ElNotification } from 'element-plus'
const audioShutUp = ref(false);
const indentificationLock = ref(false);
let intervalForLogin = null;
const ignoreChangePage = ref(false)
const boxOpenedCount = ref(0);
const binded = ref(0)
const notifyIds = reactive([]);
//藥盒物件相關資訊
const closeNotifyWindow = ()=>{
  audioShutUp.value = true;
}
const medboxStore = useMedboxStore()
const {smartBoxInfo} = storeToRefs(medboxStore)

// const smartBoxInfo = reactive({
//   "smartBoxID": smartBoxInfo.smartBoxID,
//     "location": "",
//     "patientID": null,
//     "bindingID": null,
//     "smartBoxMedications": null
// })

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
const notificationId = ref(0);
onMounted(()=>{
  setInterval(updateTemp,2000);

  // 獲取藥盒ID
  try{
    eel.get_id()((val)=>{
      if(val != null && val !== ''){
        medboxStore.setSmartBoxId(val)
      }
        //medboxStore.changeSmartBoxID(val)
      });
  }catch(e){
    // console.error(e);
    console.error("獲取裝置錯誤：")
    console.error(e);
    console.error("請設定 SMARTBOX_ID 以使用裝置綁定功能")
  }

  // 更新日期和時間
  uploadTempAndHumid();
  updateDate();
  updateTime();
  setInterval(updateTime,1000);
  setInterval(updateDate,10000);
  setInterval(uploadTempAndHumid,30000); //每30秒上傳溫濕度
  intervalForLogin = setInterval(testRegistered,4000);
  testRegistered();
  // notificationServerCheck();
  notificationCheck();

  setInterval(notificationCheck,1000);
  // setInterval(notificationServerCheck,10000);

});
const restartTestRegistered = ()=>{
  clearInterval(intervalForLogin);
  intervalForLogin = setInterval(testRegistered,4000);
  testRegistered();
}
  // 解除滾動事件的綁定 加了會壞掉
// onUnmounted(() => {
//   const scrollBox = document.querySelector('.scrollable-boxes');
//   scrollBox.removeEventListener('touchmove', preventScroll);
// });


//切換頁面
const page = ref('Window2');
const isLoggedIn = ref(true);
const showBottomBar = ref(false);

//溫濕度感測器
const currentHumid = ref(50.1)
const currentTemp = ref(26.5)

//按鈕狀態
const boxClosed=ref(false)

const uploadTempAndHumid = ()=>{
  if(binded.value != 2 || !smartBoxInfo.value.smartBoxID)
  return;
  axios.post(serverURL.value +"EnvLog",{
    smartBoxID: smartBoxInfo.value.smartBoxID,
    envLogID:0,
    temperature: currentTemp.value,
    humidity: currentHumid.value,
  }).then(()=>{
    console.log("自動上傳溫濕度成功")
  }).catch(err=>{
    console.error("自動上傳溫濕度錯誤")
    console.error(err)
  })
}
// 根據 `page` 動態切換組件
//利用 computed 來動態決定應該顯示哪一個子組件，
//這樣 <component :is="currentPage" /> 就能根據不同的 page 值來切換顯示的組件。
// const currentPage = computed(() => {
//   switch (page.value) {
//     case 'Window1':
//       return Window1;
//     case 'Window2':
//       return Window2;
//     case 'Window3':
//       return Window3;
//     default:
//       return null;
//   }
// });

// 預設為 null，點擊按鈕後顯示相應頁面
 const currentView = ref(null); 
// 根據 `currentView` 動態返回對應組件
const currentViewComponent = computed(() => {
  switch (currentView.value) {
    case 'AddMedication':
      page.value = ""
      return AddMedication;
    case 'DataStatistics':
      page.value = ""
      return DataStatistics;
    case 'MedicationTracking':
      page.value = ""
      return MedicationTracking;
    case 'Settings':
      page.value = ""
      return Settings;
    default:
      return null; // 預設為 null
  }
});
// 樹莓派裝置ID，將會做伺服器登入使用

async function testRegistered(){
  if (!smartBoxInfo.value.smartBoxID) {
    binded.value = 0;
    isLoggedIn.value = false;
    return;
  }

  try{
    console.log({
      "smartBoxID": smartBoxInfo.value.smartBoxID,
      "location":""
    })
    try{
      const res = await axios.post(serverURL.value + "smartbox/checkboxbinding",{
        "smartBoxID": smartBoxInfo.value.smartBoxID,
        "location":""
      })
      console.log("藥盒回傳資訊")
      console.log(res)
      if(res.data == "SmartBox is bound to a patient"){
        handleLoginSuccess()
        binded.value = 2;
        isLoggedIn.value = true;
        clearInterval(intervalForLogin);

      }
      if(res.data == "SmartBox is not bound to any patient"){
        handleLoginSuccess()
        binded.value = 1;
        isLoggedIn.value = false;
      }
    }catch(e){
      isLoggedIn.value = false;
      binded.value = 0;
      
    }
    try{
      const smartbox = await axios.get(serverURL.value + "smartbox/" + smartBoxInfo.value.smartBoxID)
      console.log("testRegistered獲取藥盒資訊")
      console.log(smartbox)
      medboxStore.changeMedboxLocation(smartbox.data.location);
      medboxStore.changeMedboxPatient(smartbox.data.patientID);
      medboxStore.changeMedboxBinding(smartbox.data.bindingID);
      medboxStore.resetSmartBoxMedication();


    }catch(e){
      console.error("testRegistered獲取藥盒資訊失敗")
      console.error(e);
    }
  }catch(err){
    console.error(err)

  }
}

//功能列主畫面按鈕
function handleChangeView(view) {
  if (view === '') {
    // 返回 Window1 頁面
    currentView.value = null;
    page.value = 'Window1';
  } else {
    // 切換到其他頁面
    currentView.value = view;
    page.value = 'Window1';   //清空 page，確保顯示 currentViewComponent
  }
  showBottomBar.value = false;  // 隱藏功能列
}



//功能列
let startY = 0;

// 處理登入成功
function handleLoginSuccess() {
  isLoggedIn.value = true;
  page.value = "Window1"; // 登入成功後轉到 Window1
}

const indicatorText = computed(()=>{
  let text = boxClosed.value?"":"藥盒開啟中"
  if(indentificationLock.value){
    text = "藥盒辨識中"
  }
  return text
})
//切換頁面
function addPage(toWhere) {
  /*if(page.value == 2){
    page.value = 0
  }else
  page.value++*/
  page.value = toWhere;
}



//功能列
const addPage2 = (newPage) => {
  page.value = newPage;
};

//切換頁面
const touchStartX = ref(0);
const touchEndX = ref(0);
//const emit = defineEmits(['changeWindow']);

//長方形未吃藥提醒功能列
const isRectangleOpen = ref(false); //false: 關閉 true: 開啟
// const toggleRectangle = () => {
//   isRectangleOpen.value = !isRectangleOpen.value;
// };
function toggleRectangle() {
  isRectangleOpen.value = !isRectangleOpen.value;
}


const handleTouchStart = (event) => {
//切換頁面
  touchStartX.value = event.touches[0].clientX;
  touchEndX.value = event.touches[0].clientX;
//功能列
  startY = event.touches[0].clientY;

};

const handleTouchMove = (event) => {
//切換頁面
  touchEndX.value = event.touches[0].clientX;
  const currentY = event.touches[0].clientY;
//功能列
  if(ignoreChangePage.value){
    return
  }
  if (startY - currentY > 100) {
    showBottomBar.value = true; // 上滑顯示功能列
  } else if (currentY - startY > 100) {
    showBottomBar.value = false; // 下滑隱藏功能列
  }
};


function toggleBottomBar() {
  showBottomBar.value = !showBottomBar.value;
}



//切換頁面
const handleTouchEnd = () => {
  // console.log(page)
  if(ignoreChangePage.value){
    return
  }
  if (touchStartX.value - touchEndX.value > 50) {
    // 向左滑動
    switch(page.value){
      case "Window1":
        addPage("Window2")
        break;
    }
  }
  else if ( touchEndX.value - touchStartX.value > 50) {
    // 向右滑動
    switch(page.value){
      case "Window2":
        addPage("Window1")
        break;
      case "Window3":
        addPage("Window2")
        break;
    }
  }
};

const updateTemp = async() =>{
  try{
    eel.detectButtonPressed()((val)=>{
      boxClosed.value = val;
      let newVal = val;
      if(!newVal){
    boxOpenedCount.value++;
  }else{
    ElNotification.closeAll()
  }
  console.log("boxOpenedCount: " + boxOpenedCount.value)
  let promises = [];
  if (newVal && !indentificationLock.value && boxOpenedCount.value > 3) {
    indentificationLock.value = true;
    showNotificationPage.value = true;
      // ElNotification({
      //   title: '藥盒辨識中',
      //   message: '請確保藥盒容器確實關閉，並請勿在中途開啟。｀',
      //   type: 'info',
      //   duration: 0
      // })


    if (!smartBoxInfo.value.smartBoxID) return;
    axios.get(`${serverURL.value}SmartBoxMedication/smartboxid/${smartBoxInfo.value.smartBoxID}`).then(async res => {
      let orig = res.data;

      eel.identification()(async (box)=>{

      
      console.log("辨識結果")
      for (const key in box) {
          console.log(`Color: ${box[key].color}, Shape: ${box[key].shape}`);
          let resIdentification = {data:null};
          if (box[key].color && box[key].shape){
            resIdentification = await axios.get(`${serverURL.value}medication/identify/${box[key].color}/${box[key].shape}`)
          }
            let pos = parseInt(key);
            let medicationData = resIdentification.data;
            console.log("伺服器比對結果：")
            console.log(resIdentification.data)
            // 替換medication資料
            orig.forEach(item => {
              if (item.pos === pos) {
                item.medication = medicationData;

                // 轉換格式並發送PUT請求
                let payload = {
                  smartBoxMedicationID: item.smartBoxMedicationID,
                  smartBoxID: item.smartBoxID,
                  split: item.split,
                  quantity: item.quantity,
                  medicationID: item.medication ? item.medication.medicationId : 0
                };
                console.log("更新藥物資訊")
                console.log(payload)
                if(!payload.medicationID){
                  payload.medicationID = 0;
                }
                axios.put(`${serverURL.value}SmartBoxMedication/`, payload)
                  .then(response => {
                    console.log(`Updated smartBoxMedicationID ${item.smartBoxMedicationID}`);
                    idKey.value++;
                  })
                  .catch(err => {
                    console.error(err);
                  });
              }
            });
            console.log('All updates completed');
            showNotificationPage.value = false;
            currentView.value = "";
            page.value = "Window2";
            ElNotification.closeAll()
            boxOpenedCount.value = 0;
          
        
          promises.push(resIdentification);
        
      }
    })
      // 等待所有請求完成

    }).catch(err => {
      console.error(err);
    });

  
  }

    })
    eel.readTemp()((val)=>{
      currentTemp.value = val.temperature_c
      currentHumid.value = val.humidity

      if(val.humidity != null){
        // TODO: send data to server 
      }
    })
  }catch{}
}
const ignoreChangeHandler = (onPress)=>{
  ignoreChangePage.value = onPress
}

const notificationStore = useNotificationStore()
const {reminderArr} = storeToRefs(notificationStore)

const notificationServerCheck = ()=>{
  axios.get(serverURL.value + "TestRemind/").then(res=>{
        notificationStore.setReminder(res.data);

  }).catch(err=>{
    console.error(err)
  })
}
const notifyAndShowMed = (medicationIds)=>{
  page.value = "Notifications"
  notifyIds.splice(0,notifyIds.length)
  medicationIds.forEach((item)=>{
    notifyIds.push(item)
  })
  console.log(notifyIds)

}
const notificationCheck = ()=>{
  reminderArr.value.forEach((item, key)=>{
    //需要考量setinterval的時間差
    if(item.remind <= new Date().getTime() && new Date().getTime() - item.remind < 20000){
      console.log("提醒")
      page.value = "Notifications"
      notificationId.value = key

    }

  })
}


// 全屏顯示通知
const showNotificationPage = ref(false); // 控制浮動通知頁面的顯示

function showNotification() {
  showNotificationPage.value = true; // 顯示通知
}

function closeNotification() {
  showNotificationPage.value = false; // 點擊 OK 後關閉通知
}
</script>

<!--全域style-->
<style>
@font-face {
  font-family: taipeiSansTC;
  src: url('assets/fonts/TaipeiSansTCBeta-Bold.ttf');
  font-weight: bold;
}
@font-face {
  font-family: taipeiSansTC;
  src: url('assets/fonts/TaipeiSansTCBeta-Regular.ttf');
}
@font-face{
  font-family: taipeiSansTC;
  src: url('assets/fonts/TaipeiSansTCBeta-Light.ttf');
}
*{
  font-family: 'taipeiSansTC', sans-serif;
 }
.center{
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>

<style scoped>
.app {
  position: absolute;
  height:100dvh;
  overflow: hidden;
  top:0;
  left:0;
  padding:0;
  margin:0;
  z-index:1
}

.dark-overlay { /* 功能列遮罩 */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}
.bottom-bar {
  position: fixed;
  bottom: -100px; /* 隱藏狀態 */
  left: 0;
  width: 100%;
  background-color: #00000000;
  /* opacity: 0.9; */
  color: white;
  text-align: center;
  padding: 10px;
  transition: bottom 0.3s ease;
  display: flex;
  justify-content: space-between; /* 水平排列按鈕 */
  align-items: center; /* 垂直居中 */
  z-index: 2; /* 確保功能列在遮罩之上 */
}

.bottom-bar.show {
  bottom: 0; /* 顯示狀態 */
}

.bottom-bar::before,
.bottom-bar::after {
  content: '';
  width: 20px;
  height: 2px;
  background-color: white;
  margin-left: 8px; /* 調整左側邊距 */
  margin-right: 25px; /* 調整右側邊距 */
}

.bottom-bar button {
  display: block;
  width: 300;
  padding: 10px;
  margin: 10px;
  background-color: rgb(244, 245, 236);
  color: rgb(48, 53, 58);
  border: none;
  cursor: pointer;
  font-size: 26px;
  font-weight: bold;
  border-radius: 10px; /* 設置外框圓角 */
  box-shadow: 0 0 10px 2px rgba(241, 240, 214, 0.359); /* 添加光暈 */
}

.sidebar-button {
  position: absolute;
  left: 0;
  top: 50%;
  width:70px;
  height: 70px;
  border-radius: 50%;
  transform: translateY(-50%);
  background-color: #544f85a1;
  color: #ffffff;
  font-weight: bold;
  border: none;
  padding: 10px;
  font-size: 20px;
  cursor: pointer;
}

.rectangle {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 300px;
  background-color: rgb(242, 241, 215);
  transition: width 0.3s;
  display: flex;
  align-items: center;
  border-radius: 10px; /* 設置外框圓角 */
  border: 2px solid rgb(176, 93, 63); /* 添加邊框 */
  overflow: visible; /* 確保內部元素顯示 */
}

.rectangle.open {
  width: 150px; /* 展開時的寬度 */
}

.square {
  width: 50px;
  height: 50px;
  background-color: rgb(176, 93, 63);
  cursor: pointer;
  position: absolute;
  left: -50px; /* 小正方形凸出來 */
  border-radius: 5px; /* 設置外框圓角 */
  display: flex;
  justify-content: center;
  align-items: center;
  color: rgb(245, 231, 220); /* 設置驚嘆號顏色 */
  font-size: 24px; /* 設置驚嘆號大小 */
  font-weight: bold;
}

.medication-list {
  padding: 10px;
  color: rgb(65, 72, 98);
  font-weight: bold;
}
.indicator-display{
  position:absolute;
  top: 10px;
  width:100%;
  text-align:center;
  color: rgb(244, 245, 236);
  font-size: 24px; 
  font-weight: bold;

}
.date-display {
  position:absolute;
  top: 10px;
  left: 10px;
  color: rgb(244, 245, 236);
  font-size: 24px; 
  font-weight: bold;
}
.time-display {
  position:absolute;
  top: 10px;
  right: 10px;
  font-size: 16px;
  color: rgb(244, 245, 236);
  font-size: 24px;
  font-weight: bold;
}
.display-top{
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  width:100dvw;
  height:50px;
}


/* 通知按鈕 */
.notification-button {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  background-color: rgb(176, 93, 63);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.notification-content {
  background-color: rgb(242, 241, 215);
  border: 5px solid rgb(176, 93, 63);
  width: 850px;
  height: 400px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-size: 60px;
  color: rgb(65, 72, 98);
  font-weight: bold;
  text-align: center; /* 文字置中 */
  display: flex; 
  justify-content: center; /* 水平置中 */
  align-items: center; /* 垂直置中 */
  flex-direction: column; /* 垂直排列元素 */

}

.notification-content p {
  margin: 0 0 20px;
}

.notification-content button {
  padding: 10px 20px;
  background-color: rgb(176, 93, 63);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 30px;
  width: 100px;
  height: 50px;
  margin-top: 20px;
}
.circlegreen{
  position: absolute;
  top: 13px;
  left: 42%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  background-color: #65d365;
  border-radius: 50%;
  animation: circle 3s infinite ease-in-out;
}
.circlered{
  position: absolute;
  top: 13px;
  left: 42%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  background-color: #c51818;
  border-radius: 50%;
  animation: circle 3s infinite ease-in-out;
}
@keyframes circle {
  0% {
    transform: translateX(-50%) scale(1);
  }
  50% {
    transform: translateX(-50%) scale(0.5);
  }
  100% {
    transform: translateX(-50%) scale(1);
  }
}

</style>
