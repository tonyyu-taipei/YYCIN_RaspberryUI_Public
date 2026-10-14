<template>
    <div class="windowD" >
      <div class="title">資料統計</div>
      <!-- <button @click="$emit('changeWindow','Window1')" class="bottom-center">回去Window1</button> -->
      
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue';
  
  </script>
  
  <style scoped>
  .windowD {
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
  </style>