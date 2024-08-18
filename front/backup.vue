<template>
    <!-- <UIFieldNumber v-if="form.c_model == 'Parabolic'" v-model="form.fc" label="Максимум электронной концентрации" :delta="1"/> -->
    <p v-if="!outfc.success">{{ outfc.error.format()._errors[0] }}</p>
    <!-- <p v-if="!out.success">{{ out.error.issues[0].message }}</p> -->
    <!-- <UIFieldNumber v-if="form.c_model == 'Parabolic'" v-model="form.h0" label="Высота минимума электронной концентрации" :delta="1"/> -->
    <p v-if="!outh0.success">{{ outh0.error.format()._errors[0] }}</p>
    <!-- <UIFieldNumber v-if="form.c_model == 'Parabolic'" v-model="form.yb" label="Полувысота слоя" :delta="1"/> -->

    <UIFieldNumber v-if="form.c_model == 'Chapman'" v-model="form.fc" label="Максимум электронной концентрации" :delta="1"/>
    <UIFieldNumber v-if="form.c_model == 'Chapman'" v-model="form.hm" label="Высота максимума электронной концентрации" :delta="1"/>
    <UIFieldNumber v-if="form.c_model == 'Chapman'" v-model="form.h" label="Высота минимума электронной концентрации" :delta="1"/>
    <!-- <UIFieldCheckbox v-model="form.viewline" :active="['включено','отключено']"/>
    <UIFieldSelect v-model="form.c_model" :models="mymodels"/> -->
    <!-- <Scatter
        :data="chartData" :options="options">
    </Scatter> -->
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

const mymodels = ['Parabolic', 'Chapman']
const form = ref({
    c_model: 'Parabolic',
    viewline: true,
    fc: null,
    yb: 150,
    h0: null,
    h: 80,
    hm: 200,
});
const data = ref([]);
const url = computed(() => (`/api/ne/${form.value.c_model}`))
const {status} = useFetch(() => unref(url), { //для обращения к серверу (куда мы будем делать запрос, объект со свойствами)
    query: unref(form),
    onResponse({ response }) { // декомпозиция (вытаскивание из объекта свойства)
        data.value = response._data;
        console.log(data.value)
    },
})

const chartData = computed(() => ({
    datasets: [
        {
            label: "Высотный профиль",
            borderColor: "#FF0000",
            backgroundColor: "#FF000043",
            data: data.value
        }
    ]
}));
const options = computed(() => ({
    showLine: form.value.viewline,
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


//Validation
import {z} from "zod"
const argh0 = z.number({
    required_error: "Поле должно быть заполнено",
    invalid_type_error: "Введите данные",
}).positive({ message: 'Число должно быть положительным'})
const argfc = z.number({
    required_error: "Поле должно быть заполнено",
    invalid_type_error: "Введите данные",
}).min(1, {message: 'Число должно быть больше 0'}).max(20, {message: 'Число должно быть меньше или равно 20'})

const outfc = computed(() => (argfc.safeParse(form.value.fc)))
const outh0 = computed(() => (argh0.safeParse(form.value.h0)))
// const outyb = computed(() => (argyb.safeParse(form.value.yb)))
// console.log(out.value.error.issues[0].message)
</script>
