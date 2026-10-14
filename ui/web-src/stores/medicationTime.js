import { defineStore } from 'pinia';

export const useMedicationTimeStore = defineStore('medicationTime', {
  state: () => ({
    // medicationTime: '用藥時間'
    medicationTimes: ['02:00', '12:00', '18:00', '22:00'] // 示例用藥時間
  }),
  actions: {
    setMedicationTime(newTime) {
      this.medicationTimes = newTime;
    }
  }
});

//['08:00', '12:00', '18:00', '22:00']