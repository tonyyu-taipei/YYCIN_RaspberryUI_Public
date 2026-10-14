import {defineStore} from 'pinia'
import {ref} from 'vue'
export const useNotifyMedStore = defineStore('notifymed',()=>{

    const time1 = ref('');
    const time2 = ref('');
    const time3 = ref('');
    const time4 = ref('');

    const startDate = ref('');
    

    function setTime1(value){
        time1.value = value;
    }
    function setTime2(value){
        time2.value = value;
    }
    function setTime3(value){
        time3.value = value;
    }
    function setTime4(value){
        time4.value = value;
    }
    function setStartDate(value){
        startDate.value = value;
    }

    



    return {
        time1, time2,time3,time4,startDate,setTime1,setTime2,setTime3,setTime4,setStartDate
        
    }

})