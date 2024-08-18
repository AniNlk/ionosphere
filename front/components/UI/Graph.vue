<template>
    <Scatter
        :data="chartData" :options="options">
    </Scatter>
</template>

<script setup>

import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
}from 'chart.js'
import { Scatter } from 'vue-chartjs'
ChartJS.register(
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
);

const Data = defineProps(['dot_data'])
const Options = defineModel()
const chartData = computed(() => ({
    datasets: [
        {
            label: "Высотный профиль",
            borderColor: "#00FF00",
            backgroundColor: "#00FF0043",
            data: Data.dot_data
        }
    ]
}));
const options = computed(() => ({
    showLine: Options.value,
    scales: {
        y: {
            title: {
                text: "Высота, км",
                display: true,
            }
        },
        x: {
            title: {
                text: "Электронная концентрация, e/m⁻³",
                display: true
            }
        }
    }
}))

</script>