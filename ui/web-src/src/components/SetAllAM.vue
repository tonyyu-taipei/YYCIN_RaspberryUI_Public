<template>
    <div class="windows" >
      <div class="title">所有藥槽</div>

      <div class="content">
        <span>起始日期</span>
        <input type="date" v-model="startDate" class="date-picker" />
      </div>

      <div class="time-selectors">
      <div class="time-selector">
        <input type="time" id="time1" v-model="time1" class="time-picker" />
        <label for="time1" class="time-label">早上</label>
      </div>
      <div class="time-selector">
        <input type="time" id="time2" v-model="time2" class="time-picker" />
        <label for="time2" class="time-label">中午</label>
      </div>
      <div class="time-selector">
        <input type="time" id="time3" v-model="time3" class="time-picker" />
        <label for="time3" class="time-label">晚上</label>
      </div>
      <div class="time-selector">
        <input type="time" id="time4" v-model="time4" class="time-picker" />
        <label for="time4" class="time-label">睡前</label>
      </div>
    </div>
  
    <button @click="handleSave" class="confirm-button">確認</button>
    <!-- <button @click="handleClear" class="cancel-button">清除</button> -->
    <button @click="cancel" class="cancel-button">取消</button>

    <!-- <button :class="{'detailsSAAM': true, 'active': showDetails}" @click="toggleDetails">詳細資料</button> -->

    <!-- 詳細資料浮動式窗 -->
    <div v-if="showDetails" class="modal-overlay" @click="toggleDetails">
      <div class="modal-content" @click.stop>
        <DetailsSAAM 
          :key="key"
          @changeWindow="toggleDetails" />
      </div>
    </div>
  
  </div>
</template>
  
  
<script setup>
  import { ref, defineEmits  } from 'vue';
  import DetailsSAAM from './DetailsSAAM.vue';
  import {useNotifyMedStore} from "../../stores/notifymed";
  import {storeToRefs} from "pinia";
  import { useMedicationTimeStore } from '../../stores/medicationTime';


  const notifymed = useNotifyMedStore();
  const {startDate, time1, time2, time3, time4} = storeToRefs(notifymed);
  const showDetails = ref(false);
  const key = ref(0);

  const emit = defineEmits(['updateMedicationTime', 'sendData', 'close']);
  
  ///////////////////////////////////////////


  const medicationTimeStore = useMedicationTimeStore();

  //////////////////////////////////////////

  const handleClear = () => {
      startDate.value = '';
      time1.value = '';
      time2.value = '';
      time3.value = '';
      time4.value = '';
    };

  
  // 確認按鈕的處理邏輯，包括儲存資料和發送資料
  const handleSave = () => {
      // 將資料儲存到 Pinia store
      notifymed.setStartDate(startDate.value);
      notifymed.setTime1(time1.value);
      notifymed.setTime2(time2.value);
      notifymed.setTime3(time3.value);
      notifymed.setTime4(time4.value);

      /////////////////////////////////////////////
      const newMedicationTime = [time1.value, time2.value, time3.value, time4.value].filter(time => time);
      medicationTimeStore.setMedicationTime(newMedicationTime);
      emit('updateMedicationTime', newMedicationTime);

      // const newMedicationTime = `${time1.value}, ${time2.value}, ${time3.value}, ${time4.value}`;
      // const newTimes = [time1.value, time2.value, time3.value, time4.value].filter(time => time);
      // medicationTimeStore.setMedicationTimes(newTimes);

      /////////////////////////////////////////////

      // 合併發送資料的邏輯
      const data = {
        startDate: startDate.value,
        time1: time1.value,
        time2: time2.value,
        time3: time3.value,
        time4: time4.value,
        selectedBox: 'someSelectedBoxValue'  // 假設有選擇的藥槽資料
      };
      emit('sendData', data);  // 發送資料給父組件

      // 顯示已儲存的提醒
      alert('時間已儲存');
      showDetails.value = true; // 顯示詳細資料
      emit('close'); // 發送關閉事件
  };

  

  // const handleSave = () => {
  //   notifymed.setStartDate(startDate.value);
  //   notifymed.setTime1(time1.value);
  //   notifymed.setTime2(time2.value);
  //   notifymed.setTime3(time3.value);
  //   notifymed.setTime4(time4.value);
  //   alert('時間已儲存');
  //   showDetails.value = true;
  //   // key++;
  //   emit('close');
  // };

  // const emit = defineEmits(['close']);
  const cancel = () => {
    console.log('取消按鈕被點擊');
    // 假設這個組件是通過 v-if 或 v-show 控制顯示的
    // 你可以使用 emit 事件來通知父組件關閉這個視窗
    // 清除輸入框的值
    emit('close');
  };

  const toggleDetails = () => {
    showDetails.value = !showDetails.value;
    key.value += 1;//這啥阿
  };


  </script>
  
<style scoped>
  .windows {
    width: 880px;
    height: 400px;
    padding: 8px 5px;
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgb(242, 241, 215);
    }
 
  .title {
    position: absolute;
    top: 80; 
    margin: 0 auto;  /*置中 */
    text-align: center; /* 文字居中 */
    font-size: 40px;
    color: #4b4a4a;
    font-weight: bold;
    }
  .content {
    position: absolute;
    top: 160; 
    left: 80; 
    margin: 10px; 
    font-size: 35px;
    color: #4b4a4a;
    font-weight: bold;
    }
  .date-label {
    font-size: 20px;
    color: #ff6347; /* 設定日期標籤的顏色 */
    font-weight: bold;
  }

  .date-picker {
    margin-left: 25px;
    padding: 10px;
    font-size: 20px;
    border: none; /* 移除邊框 */
    border-radius: 10px; /* 圓角 */
    background-color:#7b7a7a; /* 黑色背景 */
    color: #ffffff; /* 白色文字 */
    font-family: 'Arial Black', sans-serif;
    outline: none; /* 移除預設的 focus 樣式 */
    transition: border-color 0.3s; /* 邊框顏色過渡效果 */
    }
    .date-picker::-webkit-calendar-picker-indicator {
    filter: invert(1); /* 反轉顏色，將圖標變為白色 */
    }

  .time-selectors {
    display: flex;
    justify-content: center; /* 水平居中 */
    gap: 20px; /* 時間選單之間的間距 */
    margin-top: 80px;
    }

  .time-selector {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
    }

  .time-picker {
    margin-bottom: 5px;
    margin-left: 0px;
    padding: 10px;
    width: 200px;
    font-size: 25px;
    border: none; /* 移除邊框 */
    border-radius: 15px; /* 圓角 */
    background-color: #7b7a7a; /* 黑色背景 */
    color: #ffffff; /* 白色文字 */
    font-family: 'Arial Black', sans-serif;
    /* font-weight: bold; */
    outline: none; /* 移除預設的 focus 樣式 */
    }

  .time-picker::-webkit-calendar-picker-indicator {
    filter: invert(1); /* 反轉顏色，將圖標變為白色 */
    }

  .time-label {
    margin-top: 10px; /* 與 time-picker 之間的距離 */
    font-size: 25px;
    color: #7b7a7a;
    font-weight: bold;
    /* margin-left: 0px; */
    }

  .cancel-button {
    position: absolute;
    bottom: 80px;
    left: 80px;
    padding: 10px 20px;
    font-size: 20px;
    font-weight: bold;
    font-family: 'Arial Black', sans-serif;
    background-color: rgb(176, 93, 63); /* 背景顏色 */
    color: #ffffff; /* 文字顏色 */
    border: none; /* 移除邊框 */
    border-radius: 5px; /* 圓角 */
  }
  .confirm-button {
    position: absolute;
    bottom: 80px;
    right: 80px;
    padding: 10px 20px;
    font-size: 20px;
    font-weight: bold;
    font-family: 'Arial Black', sans-serif;
    background-color: #6674aa; /* 背景顏色 */
    color: #ffffff; /* 文字顏色 */
    border: none; /* 移除邊框 */
    border-radius: 5px; /* 圓角 */
  }

  .detailsSAAM {
    position: absolute;
    top: 170px;
    right: 170px;
    padding: 10px 20px;
    font-size: 22px;
    font-family: 'Arial Black', sans-serif;
    font-weight: bold;
    background-color: rgb(65, 72, 96); /* 背景顏色 */
    color: #ffffff; /* 文字顏色 */
    border: none; /* 移除邊框 */
    border-radius: 5px; /* 圓角 */
  }
  .detailsSAAM.active {
    background-color: rgb(244, 245, 236); /* 點擊後的背景顏色 */
    color: rgb(65, 72, 96); /* 點擊後的文字顏色 */
  }
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

  </style>