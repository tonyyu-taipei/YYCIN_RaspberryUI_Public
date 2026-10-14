<template>
    <div class="windowA" >
    <!-- 設定所有藥槽按鈕 -->
    <button @click="showSetAllAM = true" class="SetAll">設定所有藥槽</button>

    <!-- 彈出包含編輯和詳細資料的選項視窗 -->
    <div v-if="showSetAllAM" class="modal-overlay" @click="showSetAllAM = false">
      <!-- <div class="modal-content" @click.stop> -->
        <button @click="openEdit" class="option-button">編輯</button>
        <!-- <button :class="{'detailsSAAM': true, 'active': showDetails}" @click="toggleDetails">詳細資料</button> -->

         <!-- 直接顯示詳細資料內容，移除按鈕 -->
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
      <!-- </div> -->
    </div>

    <!-- 顯示 SetAllAM 組件 -->
    <div v-if="showEdit" class="modal-overlay" @click="showEdit = false">
      <div class="modal-content" @click.stop>
        <SetAllAM @close="handleClose('showEdit')" />
      </div>
    </div>

    <!-- 顯示詳細資料視窗 -->
    <!-- <div v-if="showDetails" class="modal-overlay" @click="showDetails = false">
      <div class="modal-content" @click.stop>
        <p>這裡是詳細資料的內容。</p>
        <button @click="showDetails = false">關閉</button>
      </div>
    </div> -->

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

    <!-- 設定個別藥槽按鈕 -->
    <button @click="showSingleAM = true" class="SetASingle">設定個別藥槽</button>

    <!-- 顯示 SetASingleAM 組件 -->
    <div v-if="showSingleAM" class="modal-overlay2" @click="showSingleAM = false">
      <div class="modal-content" @click.stop>
        <SetASingleAM @close="handleClose('showSingleAM')" />
      </div>
    </div>
  </div>
  </template>
  
  
<script setup>
  import { ref } from 'vue';
  import SetAllAM from './SetAllAM.vue';
  import SetASingleAM from './SetASingleAM.vue';
  import DetailsSAAM from './DetailsSAAM.vue';

 // 控制視窗的顯示
const showSetAllAM = ref(false);
const showEdit = ref(false);
const showSingleAM = ref(false);

const showDetails = ref(false);
  const toggleDetails = () => {
    showDetails.value = !showDetails.value;
  };

// 開啟編輯視窗
const openEdit = () => {
  showSetAllAM.value = false;
  showEdit.value = true;
};

// 開啟詳細資料視窗
const openDetails = () => {
  showSetAllAM.value = false;
  showDetails.value = true;
};

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

</script>

<style scoped>
.windowA {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(51, 63, 67);
}

.SetAll, .SetASingle {
  font-weight: bold;
  font-size: 50px;
  width: 400px;
  height: 100px;
  cursor: pointer;
  border-radius: 10px;
}

.SetAll {
  position: absolute;
  top: 150px;
  background-color: rgb(65, 72, 96);
  border: 5px solid rgb(120, 135, 159);
  color: rgb(242, 241, 215);
}

.SetASingle {
  position: absolute;
  bottom: 150px;
  background-color: rgb(120, 135, 159);
  border: 5px solid rgb(242, 241, 215);
  color: rgb(56, 62, 83);
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
  /* padding: 20px; */
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

  
</style>


<!-- <style scoped>
  .windowA {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgb(51, 63, 67);
  }

  .title {
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center; /* 文字居中 */
    font-size: 60px;
    color: #ffffff;
    font-family: 'Arial Black', sans-serif;
    font-weight: bold; 
  }
  .SetAll {
    position: absolute;
    top: 150px;
    margin: 0 auto;  /*置中 */
    font-weight: bold; /* 設定字體粗體 */
    font-size: 50px;
    width: 400px;
    height: 100px;
    padding: 0px;
    border: none; /* 移除框線 */
    background-color: rgb(65,72,96);
    border: 5px solid rgb(120, 135, 159); /* 添加邊框 */
    color: rgb(242, 241, 215);
    cursor: pointer; /* 設定滑鼠樣式 */
    border-radius: 10px;
}
.SetASingle {
  position: absolute;
  bottom: 150px;
  margin: 0 auto;  /*置中 */
  font-weight: bold; /* 設定字體粗體 */
  font-size: 50px;
  width: 400px;
  height: 100px;
  padding: 0px;
  /* border: none; */
  background-color: rgb(120, 135, 159);
  border: 5px solid rgb(242, 241, 215); /* 添加邊框 */
  color: rgb(56, 62, 83);
  cursor: pointer; /* 設定滑鼠樣式 */
  border-radius: 10px;
}

/* 詳細資料背景遮罩 */
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
/* 詳細資料背景遮罩 */
.modal-overlay2 { 
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
</style> -->