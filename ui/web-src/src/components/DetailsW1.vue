<template>
  <div class="windoww" >
    <div class="detail">
    <!-- <button @click="$emit('changeWindow','Window1')" class="bottom-center">回去Window1</button> -->
      <h3>目前吃藥詳細資料</h3>
      <p>起始日期: {{ startDate }}</p>
      <p>早上: {{ time1 }}</p>
      <p>中午: {{ time2 }}</p>
      <p>晚上: {{ time3 }}</p>
      <p>睡前: {{ time4 }}</p>
      <!-- <p>------個別設定------</p>
      <p>藥槽: {{ selectedBox }}</p> -->
    </div>
  </div>
</template>


<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  startDate: String,
  time1: String,
  time2: String,
  time3: String,
  time4: String,
  selectedBox: String
});

</script>

<style scoped>
.windoww {
  width: 200px;
  height: 250px;
  padding: 80px 50px;
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(242, 241, 215);
  border: 4px solid rgb(65, 72, 96); /* 添加邊框 */
}

.detail {
  position: absolute;
  text-align: center; /* 文字居中 */
  font-size: 30px;
  color: rgb(60, 66, 87);
  font-family: 'Arial Black', sans-serif;
  font-weight: bold;
}
</style>