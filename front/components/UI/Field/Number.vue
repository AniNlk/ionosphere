<template>
    <div style="display: flex; flex-direction: row;">
        <button @click="counter -= delta ">-</button>
        <input type="number" 
            style="::-webkit-inner-spin-button,
                    ::-webkit-inner-spin-button {
                display: none;
                -webkit-appearance: none;
                margin: 0;}"    
            :value="counter" placeholder="Введите число" @input="onInput"/>
        <button @click="counter += delta ">+</button>
        <label>{{ props.label }}</label>
    </div>
</template>

<script setup>

const counter = defineModel();
const delta = 1
const props = defineProps(['label'])
const onInput = (event) => {
    const { target: { value } } = event
    if (Number.isNaN(+value)) {
        return
    }
    (value === ' ') ? counter.value = null : counter.value = +value //?
}
</script>