<template>
    <div class="windoww" >
      <div class="detail">
        <h3>設置時間和日期</h3>
        <p>起始日期 <input v-model="startDate" placeholder="起始日期" class="detail" /></p>
        <p>早上 <input v-model="time1" placeholder="早" class="detail" /></p>
        <p>中午 <input v-model="time2" placeholder="中" class="detail" /></p>
        <p>晚上 <input v-model="time3" placeholder="晚" class="detail" /></p>
        <p>睡前 <input v-model="time4" placeholder="睡前" class="detail" /></p>
        <!-- <p>藥槽: <input v-model="selectedBox" placeholder="藥槽" class="detail" /></p> -->
        <!-- <button @click="sendData">確認</button> -->
        <!-- <p>起始日期: {{ startDate }}</p>
        <p>早: {{ time1 }}</p>
        <p>中: {{ time2 }}</p>
        <p>午: {{ time3 }}</p>
        <p>晚: {{ time4 }}</p> -->
        <!-- <p>------個別設定------</p>
        <p>藥槽: {{ selectedBox }}</p> -->
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref, watch, defineEmits } from 'vue';
  import {useNotifyMedStore} from "../../stores/notifymed";
  import {storeToRefs} from "pinia";
  // import { useUsageLogStore } from '@/stores/usageLog';

  const notifymed = useNotifyMedStore();
  const {startDate, time1, time2, time3, time4} = storeToRefs(notifymed);

  // const startDate = ref('');
  // const time1 = ref('');
  // const time2 = ref('');
  // const time3 = ref('');
  // const time4 = ref('');
  const selectedBox = ref('');

  const emit = defineEmits(['sendData']);
  
  // const usageLogStore = useUsageLogStore();

  const sendData = () => {
    const data = {
      startDate: startDate.value,
      time1: time1.value,
      time2: time2.value,
      time3: time3.value,
      time4: time4.value,
      selectedBox: selectedBox.value,
    };
    
    // 新增紀錄到 usageLog store
    // usageLogStore.addUsageLog(log);

    emit('sendData', data);
    emit('close'); // 關閉浮動窗
  };

  // 監聽數據變化，自動發送數據
  watch([startDate, time1, time2, time3, time4, selectedBox], sendData);
    
  // const props = defineProps({
  //   startDate: String,
  //   time1: String,
  //   time2: String,
  //   time3: String,
  //   time4: String,
  //   selectedBox: String
  // });
  </script>
  
  <style scoped>
  .windoww {
    width: 300px;
    height: 450px;
    padding: 0px 50px;
    border-radius: 20px;
    /* display: flex; */
    /* justify-content: center; */
    /* align-items: center; */
    background-color: rgb(65, 72, 96);
    border: 4px solid rgb(242, 241, 215);
    overflow: scroll; /* 添加這行來啟用滾動條 */
  }
  
  .detail {
    /* position: absolute; */
    text-align: center; 
    font-size: 30px;
    color: rgb(242, 241, 215);
    /* font-family: 'Arial Black', sans-serif; */
    font-weight: bold;
    display: inline-block; /* 使 input 元素與文字在同一行沒用 */
    margin-bottom: 30px;
  }
  input.detail {
    color: rgb(242, 241, 215);
    background-color: transparent; /* 設置背景透明 */
    border: none; /* 移除邊框 */
    outline: none; /* 移除聚焦時的外框 */
    padding: 10px; /* 增加內部間距 */
    width: 100%; /* 設置寬度 */
    box-sizing: border-box; /* 確保 padding 不影響寬度 */
  }
  p {
    display: inline; /* 使 p 元素與其他元素在同一行 */
  }
  </style>