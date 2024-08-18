<template>
    <select name="elec" id="h" @change="onChange">
        <option v-for="model in props.models" :key="model" :value="model">{{ model }}</option>
    </select>
    <label for="h">{{ c_model }}</label>
</template>

<script setup>
const c_model = defineModel()
const props = defineProps(['models'])

const onChange = (event) => {
    c_model.value = event.target.value
}
</script>
