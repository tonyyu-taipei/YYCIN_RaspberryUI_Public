import {defineStore} from 'pinia'
import {reactive} from 'vue'
export const useMedboxStore = defineStore('medbox',()=>{
    const smartBoxInfo = reactive({
        "smartBoxID": null,
        "location": "",
        "patientID": null,
        "bindingID": null,
        "smartBoxMedications": {
            '1':{name:'',id:0,amount:0},
            '2':{name:'',id:0,amount:0},
            '3':{name:'',id:0,amount:0},
            '4':{name:'',id:0,amount:0},
            '5':{name:'',id:0,amount:0},
            '6':{name:'',id:0,amount:0},
            '7':{name:'',id:0,amount:0},
            '8':{name:'',id:0,amount:0},
        }
    })

    // 更換藥盒位置
    function changeMedboxLocation(location){
        smartBoxInfo.location = location
    }


    function changeMedboxPatient(patientID){
        smartBoxInfo.patientID = patientID
    }

    function changeMedboxBinding(bindingID){
        smartBoxInfo.bindingID = bindingID
    }
    function addMedication(medication){
        smartBoxInfo.smartBoxMedications.push(medication)
    }

    function addMedicationObj(medications){
        smartBoxInfo.smartBoxMedications = medications

    }

    function removeMedication(medication){
        smartBoxInfo.smartBoxMedications = smartBoxInfo.smartBoxMedications.filter(med => med.id !== medication.id)
    }
    function resetSmartBoxMedication(){
        smartBoxInfo.smartBoxMedications = {
            '1':{name:'',id:0,amount:0},
            '2':{name:'',id:0,amount:0},
            '3':{name:'',id:0,amount:0},
            '4':{name:'',id:0,amount:0},
            '5':{name:'',id:0,amount:0},
            '6':{name:'',id:0,amount:0},
            '7':{name:'',id:0,amount:0},
            '8':{name:'',id:0,amount:0},
        }
    }
    function setSmartBoxId(id){
        smartBoxInfo.smartBoxID = id
    }



    return {
        smartBoxInfo,
        changeMedboxLocation,
        changeMedboxPatient,
        changeMedboxBinding,
        addMedication,
        removeMedication,
        resetSmartBoxMedication,
        addMedicationObj,
        setSmartBoxId
        
    }

})
