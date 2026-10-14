<template>
   <div class="medbox-comp">
      <div :class="{'med-block-red':!blinkingRed && blink[index]['Blink'], 'med-block':!(!blinkingRed && blink[index]['Blink'])}" v-for="(item, index) in medBoxReactive" :key="index" @click="handleClick(index)">
        {{ index }}  
        <h3>{{ medBoxReactive[index].name }}</h3>
        <med-storage v-if="medBoxReactive[index].name != '空'">
          <b v-if="!hideStatus" :class="{'status-good':medBoxReactive[index].amount > 5, 'status-bad':medBoxReactive[index].amount <= 5}">
            {{ medBoxReactive[index].amount > 5 ? '足夠' : '將盡' }}
          </b>
        </med-storage>
        <!-- <button @click.stop="handleEditClick(index)" class="edit-button">修改</button> -->
      </div>


      <!-- <div v-if="showDialog" class="dialog-overlay"> -->

        <!-- 顯示藥物資訊 -->
        <div v-if="showDialog" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
              <h3>藥槽 {{ selectedBoxIndex }} 藥品</h3>
              <p>名稱: {{ selectedDrug.name }}</p>
              <p>數量: {{ selectedDrug.amount }}</p>
              <button @click="openEditDialog" class="openEditDialog">修改藥物資訊</button>
            </div>
          </div>

       <!-- 修改藥物資訊視窗 -->
      <div v-if="showEditDialog" class="dialog-overlay">
        <div class="dialog">
          <h3>修改藥物資訊</h3>
          <label for="drug-name">藥物名稱:</label>
          <select id="drug-name" v-model="selectedDrug.name" class="drug-menu">
            <option value="驅異樂膜衣錠">驅異樂膜衣錠</option>
            <option value="糖漸平膜衣錠">糖漸平膜衣錠</option>
            <option value="心寧美">心寧美</option>
            <option value="利福全錠">利福全錠</option>
            <option value="吐福錠">吐福錠</option>
            <option value="維帕特膜衣錠">維帕特膜衣錠</option>
            <option value="合必爽錠">合必爽錠</option>
          </select>

          <label for="drug-amount">目前藥物數量:</label>
          <div class="drug-amount">
            <input type="range" v-model="selectedDrug.amount" min="0" max="30" step="1" />
            <span>{{ selectedDrug.amount }}</span>
          </div>
          
          <button @click="closeDialog" class="closeDialog">取消</button>
          <button @click="saveChanges" class="saveChanges">保存</button>

          </div>
        </div>
      <!-- </div> -->

    </div>
</template>

<script setup>
import { ref,reactive,onMounted } from 'vue';
const {medBoxReactive, hideStatus, blink} = defineProps(['medBoxReactive', 'hideStatus', 'blink']);
const emit = defineEmits(['showDialog']);

const selectedBoxIndex = ref(-1);
const selectedDrug = reactive({name: '', amount: 0});

const blinkingRed = ref(false);

const showDialog = ref(false);
const showEditDialog = ref(false);

//藥盒藥品資訊
const handleClick = (index) => {
  console.log(`藥盒 ${index + 1} 被點擊`);
  selectedBoxIndex.value = index;
  selectedDrug.name = medBoxReactive[index].name;
  selectedDrug.amount = medBoxReactive[index].amount;
  // emit('showDialog', {index: selectedBoxIndex.value, drug: selectedDrug});
  showDialog.value = true;
}

//保存修改藥物資訊
const saveChanges = () => {
  medBoxReactive[selectedBoxIndex.value].name = selectedDrug.name;
  medBoxReactive[selectedBoxIndex.value].amount = selectedDrug.amount;
  emit('updateMedBoxReactive', medBoxReactive);
  showEditDialog.value = false;
  showDialog.value = true;
};


// 打開藥物修改視窗
const openEditDialog = () => {
  showDialog.value = false;
  showEditDialog.value = true;
};


onMounted(()=>{
  if(blink){
    setInterval(()=>{
      blinkingRed.value = !blinkingRed.value;
    }, 1000);
  }
})

const closeDialog = () => {
  showDialog.value = false;
  showEditDialog.value = false;
};

const closeModal = () => {
  showDialog.value = false;
};




</script>

<style scoped>
  .med-block{
    width:190px;
    height:135px;
    padding: 15;
    margin:8;
    background-color:rgb(67, 75, 95);
    color:rgb(189, 189, 189);
    border-radius: 10px;
    border: none; /* 移除邊框 */
  }
  .med-block-red{
    background-color:rgb(153, 46, 46);
    width:190px;
    height:135px;
    padding: 15;
    margin:8;
    color:rgb(189, 189, 189);
    border-radius: 10px;
    border: none; /* 移除邊框 */
  }
  .med-block h3, .med-block-red h3{
    margin:0;
    width:100%;
    word-wrap: break-word;
    text-align: center;
    vertical-align: middle;
    font-size:30px;

  }
  .medbox-comp{
    display: flex;
    flex-direction: row;
    flex-wrap:wrap;
     justify-content: center;
    align-items: center;
    filter: drop-shadow(0px 0px 30px rgba(0,0,0,0.5));
    
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

med-storage{
    text-align: center;
    width:100%;
    height:50px;
    padding-top:9px;
    display:inline-block;
    margin:10 0 0 0;

  }
  med-storage b{
    width:80px;
    font-weight:600;
    border-radius: 10px;
    padding:8px;
    background-color:rgb(152, 200, 152);
    color:rgb(48, 53, 58);
    font-size:20
  }

  .edit-button {
  margin-top: 10px;
  padding: 5px 10px;
  cursor: pointer;
}

  .dialog-overlay {
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

.dialog {
  width: 400px;
  background: rgb(55, 55, 55);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dialog h3 {
  margin-top: 0;
}

.dialog label {
  display: block;
  margin-top: 10px;
}

.dialog input {
  width: 100%;
  padding: 5px;
  margin-top: 5px;
}

.dialog button {
  margin-top: 10px;
  padding: 5px 10px;
  cursor: pointer;
}
.drug-menu{
  width:100%;
  padding:5px;
  margin-top:5px;
  border-radius:5px;
  background-color:rgb(255, 255, 255);
  color:rgb(65, 65, 65);
  font-size:30px;
}
.drug-amount{
  width:100%;
  padding:5px;
  margin-top:5px;
  border-radius:5px;
  background-color:rgb(255, 255, 255);
  color:rgb(65, 65, 65);
  font-size:30px;
}

  /* 浮動視窗的背景遮罩 */
  .modal-overlay{
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

  .openEditDialog {
  /* display: block; */
  /* position: fixed; */
  /* bottom: 20px; */
  /* right: 20px;
  margin: 30px; */
  padding: 10px;
  font-size: 25px;
  /* font-weight: bold; */
  background-color: rgb(102, 108, 124); /* 背景顏色 */
  color: rgb(255, 255, 255); /* 文字顏色 */
  border: none; /* 移除邊框 */
  border-radius: 10px; /* 圓角 */
  /* border: 3px solid rgb(143, 143, 143); */
}

.closeDialog {
  /* position: absolute; */
  /* bottom: 80px; */
  /* left: 80px; */
  padding: 10px 20px;
  font-size: 20px;
  font-weight: bold;
  font-family: 'Arial Black', sans-serif;
  background-color: rgb(176, 93, 63);
  color: #ffffff; 
  border: none; /* 移除邊框 */
  border-radius: 5px; /* 圓角 */
  }

  
.saveChanges {
    position: absolute;
    right: 273px;
    /* position: fixed;  */
    /* bottom: 80px; */
    /* right: 80px; */
    padding: 10px 20px;
    font-size: 20px;
    font-weight: bold;
    font-family: 'Arial Black', sans-serif;
    background-color: #6674aa;
    color: #ffffff;
    border: none; /* 移除邊框 */
    border-radius: 5px; /* 圓角 */
  }



</style>