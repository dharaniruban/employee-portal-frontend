<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Employee Count per Department</h2>
    <div v-if="loading" class="text-center text-gray-500 animate-pulse">Loading...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="chartData.labels.length === 0" class="text-center text-gray-500">No data available</div>
    <Bar v-else :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = ref({
  labels: [],
  datasets: [{
    label: 'Employee Count',
    data: [],
    backgroundColor: '#4F46E5',
  }]
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Employee Count per Department' }
  }
};

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/employee-report/', { credentials: 'include' });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data);
    chartData.value.labels = data.labels || [];
    chartData.value.datasets[0].data = data.data || [];
    if (!data.labels || !data.data) {
      error.value = 'Invalid data format from API';
    }
  } catch (err) {
    console.error('Fetch error:', err);
    error.value = 'Failed to load report data: ' + err.message;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
div {
  max-width: 800px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>