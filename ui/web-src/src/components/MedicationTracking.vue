<template>
    <div class="windowM" >
      <!-- <h1>用藥追蹤</h1> -->

      
      <!-- <div class="title">用藥追蹤</div> -->
      <!-- <button @click="$emit('changeWindow','Window1')" class="bottom-center">回去Window1</button> -->

      <div class="demo-datetime-picker" >

      <div class="container" @touchmove="boxOnTouch" @touchend="boxOffTouch" ref="scrollboxRef">
        <el-date-picker
        v-model="value1"
        type="date"
        placeholder="選擇日期"
        format="YYYY-MM-DD"
        date-format="MMM DD, YYYY"
        time-format="HH:mm"
        size="large"
        style="margin-bottom:20px"
      />

      <button v-for="(time, index) in getAllTime" :key="index" class="content" :class="{'active':leftActive == index, 'inactive':leftActive!=index}"
        @click="leftActive = index"
      >{{ formatTime(time) }}</button>

        </div>
      <!-- <div class="line" /> -->
      <!-- <div class="block">
        <el-date-picker
          v-model="value2"
          type="datetimerange"
          start-placeholder="Start date"
          end-placeholder="End date"
          format="YYYY-MM-DD HH:mm:ss"
          date-format="YYYY/MM/DD ddd"
          time-format="A hh:mm:ss"
        />
      </div> -->
    </div>
    <div class="right-elem">
      <!-- 先不要自己多做可能做不出來的功能 -->
      <!-- <h2><status class="status-good">✓ 完成</status>已服用所有藥物</h2> -->
    </div>

        <div class="containerx">

          <div class="list-info" v-for="item in getAllMedFromTime" :key="item.SmartBoxMedicationID" :item="item" >
            <big-status class="status-info">{{ item.smartBoxMedication.pos }}號槽</big-status>
            <info>{{ item.medication.name }}</info><status :class="{'status-good':item.status==0, 'status-info':item.status == 1 }" style="float:right"> {{ item.Action }} </status>
          </div>
          </div>

    </div>
  </template>
  
  
  <script setup>
  import { ref,reactive, computed, watch, onMounted } from 'vue';
  import { ElDatePicker } from 'element-plus';
  import 'element-plus/dist/index.css';
  import 'element-plus/theme-chalk/el-date-picker.css';
  import {useMedboxStore} from "../../stores/medbox";
  import axios from 'axios';
  import { apiBaseUrl } from '../api';
  import {storeToRefs} from "pinia";

  const medboxStore = useMedboxStore()
  const {smartBoxInfo} = storeToRefs(medboxStore)

  const value1 = ref(new Date())
  const value2 = ref('')

  const leftActive = ref(0)

  const data = reactive([
  {
   'medication': {},
    'dateTime': new Date('2024-11-13T08:00:00'),
    'action':'拿取',
    'status':'0',
    'notes':'',
    'smartBoxMedication':{}
  }
])
function getUsageLogs(){
  if (!smartBoxInfo.value.smartBoxID) return;
  axios.get(`${apiBaseUrl}usagelog/date/${new Date(value1.value.getTime() + 8 * 60 * 60 * 1000).toISOString()}/smartbox/${smartBoxInfo.value.smartBoxID}`).then((res)=>{
     //delete the dataArray
     const newData = res.data.map(item => ({...item}));
     data.splice(0,data.length,...newData)
     console.log(new Date(value1.value).toISOString())
     console.log(res.data)
   })
}
onMounted(()=>{
  getUsageLogs()
})
watch(() => value1.value, () => {
  getUsageLogs()
});
const getAllMedFromTime = computed(() => {
  const targetDate = new Date(new Date(value1.value).setSeconds(0,0));
  const targetYear = targetDate.getFullYear();
  const targetMonth = targetDate.getMonth();
  const targetDay = targetDate.getDate();
  const targetTime = getAllTime.value[leftActive.value];

  if (!targetTime) {
    return [];
  }

  const targetHour = targetTime.getHours();
  const targetMinute = targetTime.getMinutes();
  const targetSecond = targetTime.getSeconds();
  const targetTimestamp = new Date(new Date(targetYear, targetMonth, targetDay, targetHour, targetMinute, targetSecond).setSeconds(0,0)).getTime();

  return data.filter((item) => {
    const itemTimestamp = new Date(new Date(item.dateTime).setSeconds(0,0)).getTime();
    console.log(itemTimestamp+" target: "+targetTimestamp)
    
    // return the item that has the same timestamp as the target timestamp
    // ignore the second part, all the time is rounded to the minute

    return itemTimestamp === targetTimestamp;

  });
});

const getAllTime= computed(() => {
    const targetDate = new Date(value1.value);
    const targetYear = targetDate.getFullYear();
    const targetMonth = targetDate.getMonth();
    const targetDay = targetDate.getDate();
    console.log("computed GetAllTime Triggered")
    const timesForDate = data
      .map((item) => new Date(new Date(item.dateTime).setSeconds(0,0)))
      .filter((date) => 
        date.getFullYear() === targetYear &&
        date.getMonth() === targetMonth &&
        date.getDate() === targetDay
      )
      .map((date) => date.getTime());

    return Array.from(new Set(timesForDate))
      .sort((a, b) => a - b)
      .map((timestamp) => new Date(timestamp));
  });


  //format the time to 上午HH:mm or 下午HH:mm
  const formatTime = (time) => {
    let hour = time.getHours()
    let minute = time.getMinutes()
    let ampm = hour >= 12 ? '下午' : '上午'
    hour = hour % 12
    hour = hour == 0 ? 12: hour
    hour = hour < 10 ? '0' + hour : hour
    minute = minute < 10 ? '0' + minute : minute
    return ampm + hour + ':' + minute
  }

  const emit = defineEmits(['ignoreChangePage']);
  const scrollboxRef = ref(null);

  function boxOnTouch(){
    var policyElement = scrollboxRef.value;
    //如果見底了，則return
    if(policyElement.scrollHeight - Math.round(policyElement.scrollTop) <= policyElement.clientHeight ){
      return
    }

    // if(policyElement.scrollTop == 0)return
    emit('ignoreChangePage',true)
  }
  function boxOffTouch(){
    setTimeout(()=>{
      emit('ignoreChangePage',false)
    },300)
  }
  </script>
  
<style scoped>

  h1{
    margin:40 0 10 10;
    display:inline-block;
    width:255;
    font-size:60px;
    position:absolute;
    top:0;
    left:0;
    color:rgb(244, 245, 236);

  }
  .windowM {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgb(51, 63, 67);
  }

  .title {
    position: absolute;
    top: 40px; 
    left: 20px;
    font-size: 60px;
    color: rgb(244, 245, 236);
    font-weight: bold; 
  }

  .demo-datetime-picker {
    display: flex;
    height: 300px;
    padding: 0;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: stretch;
    margin-top: -180px;
  }
  .demo-datetime-picker .block {
    padding: 30px 0;
    text-align: center;
  }

  /* 媽的沒用 */
  .large-date-picker {
    font-size: 20px; /* 調整字體大小 */
    width: 300px; /* 調整寬度 */
    height: 50px; /* 調整高度 */
  }
  
  .line {
    width: 1px;
    background-color: var(--el-border-color);
  }
  .el-input__inner{
    font-size:30px
  }
  status{
    display:inline-block;
    font-size:23;
    border-radius:10px;
    padding:5px;
    margin-right:10px;
    color:rgb(51, 63, 67);
    margin-top:8px;
    }
    big-status {
  display: inline-block; /* Changed to inline-block */
  font-size: 35px; /* Added unit */
  line-height: 42px; /* Adjust this value to match the container height */
  border-radius: 10px;
  padding: 5px;
  margin-right: 5px;
  color: rgb(51, 63, 67);
  vertical-align: bottom; /* Vertically align the element */
}
  .status-good{
    background-color:rgb(152, 200, 152);
  }
  .status-bad{
    background-color:rgb(243, 139, 139);
  }
  .status-info{
    background-color:rgb(168, 191, 240);
  }
  h2{
    color:rgb(244, 245, 236);
    
  }
  .right-elem{
    position:absolute;
    top:50;
    right:0;
    margin-right:10px;
  }

  .container {
    overflow-y:auto;
    position: absolute;
    padding: 10px;
    top: 70px;
    left: 20px; 
    background-color: rgba(255, 255, 255, 0.265);
    border-radius: 10px; 
    width: 220px;
    height: 410px;
    flex-direction: column;
    /* justify-content: space-between;  */
    align-items: center; /* 水平居中 */

  }
  .active{
    background-color: rgba(0, 0, 0, 0.5);
 
  }
  .inactive{
    background-color: rgba(43, 43, 43, 0.5);
    
  }
  .content {
    /* position: absolute; */
    /* text-align: center; */
    font-size: 30px;
    color: #ffffff;
    font-weight: bold;
    width: 220px; 
    height: 80px; 
    border: none; 
    border-radius: 10px; 
    margin-bottom: 10px;
  }
  .containerx {
    padding: 10px; 
    background-color: rgba(255, 255, 255, 0.265);
    border-radius: 10px; 
    width: 650px;
    height: 450px;
    bottom: 15px;
    margin-left:260px;
    margin-top:10px;
  }
  .list-info{
    width:97%;
    height:50px;
    background-color:rgba(0, 0, 0, 0.5);
    margin-top:10px;
    margin-bottom: 10px;
    padding:10px;
    border-radius:10px;
    color:rgb(244, 245, 236);
    font-size:50px;
    font-weight: bold;
  }
  info{
    line-height:50px;
  }
</style>
