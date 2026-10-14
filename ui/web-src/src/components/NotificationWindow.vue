<template>
  <div class="window">
    <h1>通知</h1>    <button @click="notificationClear()" class="SetAll" style="margin-left:40px">關閉通知</button>
    <div class="container">
      <med-box class="medb" :medBoxReactive="medBoxReactive" hide-status="true" :blink="blink"></med-box>
    </div>

  </div>
</template>

<script setup>
import MedBox from './MedBox.vue';
import {reactive, onMounted, ref} from 'vue';
import {useNotificationStore} from "../../stores/notification";
import {useMedboxStore} from "../../stores/medbox";
import {storeToRefs} from 'pinia';
import axios from 'axios';
import { apiBaseUrl } from '../api';

const emit = defineEmits(['changeWindow']);

const medBoxReactive = reactive({
  '1': {name: '空', amount: 0,id:0},
  '2': {name: '空', amount: 0,id:0},
  '3': {name: '空', amount: 0 ,id:0},
  '4': {name: '空', amount: 0 ,id:0},
  '5': {name: '空', amount: 0 ,id:0},
  '6': {name: '空', amount: 0  ,id:0},
  '7': {name: '空', amount: 0 ,id:0},
  '8': {name: '空', amount: 0 ,id:0},

})
const blink = reactive({
  '1':{Amount:0, Blink: false},
  '2':{Amount:0, Blink: false},
  '3':{Amount:0, Blink: false},
  '4':{Amount:0, Blink: false},
  '5':{Amount:0, Blink: false},
  '6':{Amount:0, Blink: false},
  '7':{Amount:0, Blink: false},
  '8':{Amount:0, Blink: false},

})

const notificationStore = useNotificationStore()
const {reminderArr} = storeToRefs(notificationStore)
const {notificationId, idsToNotify} = defineProps(['notificationId', 'idsToNotify'])
const medboxStore = useMedboxStore()
const {smartBoxInfo} = storeToRefs(medboxStore)
const updateKey = ref(0)
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
})

if(!idsToNotify && idsToNotify.length == 0){
    return
  }
  for(let id of idsToNotify){
    console.log(id)
    // iterate through medBoxReactive
    for(let key in medBoxReactive){
      console.log(medBoxReactive[key].id)
      if(medBoxReactive[key].id == id){
        blink[key].Blink = true
        console.log('blink')
      }
    }
  }
})
}
onMounted(()=>{
  getAllBoxMed()
  console.log(idsToNotify)

})
function notificationClear(){
  // axios.delete(`${apiBaseUrl}testremind/`+notificationId)
  // notificationStore.removeReminder(notificationId)
  // console.log(notificationId)
  emit('changeWindow','Window1')
}
</script>

<style>

  .window {
    width: 100dvw;
    height: 100dvh;
    background-color: rgb(48, 53, 58);
    font-size: 30px;
    color: rgb(244, 245, 236);
    position: relative; /*bottom-center*/
  }
  .container{
    height:100dvh;
  }
  h1{
    display:inline-block;
    height:30px;
  }

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

</style>
