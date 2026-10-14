import {defineStore} from 'pinia'
import {ref,reactive} from 'vue'
export const useNotificationStore = defineStore('notification',()=>{
    const offset = 8 * 60; // UTC+8 的分鐘數
    const reminderArr = reactive(new Map());    
    const iterateKey = ref(0);
    function setReminder(remindObj){
        iterateKey.value++;
        for(let r of remindObj){
            if(reminderArr.has(r.id)){
                const existingReminder = reminderArr.get(r.id);
                reminderArr.set(r.id,{...existingReminder, 'key':iterateKey.value});
                continue;
            }
            
            reminderArr.set(r.id,{'remind':new Date( new Date(r.remind).getTime() + offset * 60 * 1000 ), 'text':r.text, 'key':iterateKey.value});

        }
        deleteRemindersNotOnServer();
    }

    function removeReminder(id){
        reminderArr.delete(id);
    }
    function clearReminder(){
        reminderArr.clear();
    }
    function deleteRemindersNotOnServer(){
        for(let [key, value] of reminderArr){
            if(value.key !== iterateKey.value){
                reminderArr.delete(key);
            }
        }
    }

    return {
        reminderArr,
        setReminder,
        removeReminder,
        clearReminder,
        deleteRemindersNotOnServer
        
    }

})