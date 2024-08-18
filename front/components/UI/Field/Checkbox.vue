<template>
    <input @click="viewline = !viewline " type="checkbox" id="check" v-if="viewline" checked>
    <input @click="viewline = !viewline " type="checkbox" id="check" v-else>
    <label for="check">Соединение точек линией {{ (viewline)?props.active[0]:props.active[1] }}</label>
</template>

<script setup>
    const viewline = defineModel()
    const props = defineProps(['active'])
</script>