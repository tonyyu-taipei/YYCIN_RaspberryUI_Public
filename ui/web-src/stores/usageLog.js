import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUsageLogStore = defineStore('usageLog', () => {
  // 用藥紀錄的狀態
  const usageLogs = ref([]);

  // 新增用藥紀錄的函數
  const addUsageLog = (log) => {
    usageLogs.value.push(log);
  };

  // 獲取所有用藥紀錄的函數
  const getUsageLogs = () => {
    return usageLogs.value;
  };

  // 清空紀錄（如果需要）
  const clearLogs = () => {
    usageLogs.value = [];
  };

  return {
    usageLogs,
    addUsageLog,
    getUsageLogs,
    clearLogs
  };
});
