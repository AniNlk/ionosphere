<template>
    <UIParamAdjust v-model="form" @send_form="paramForm" ></UIParamAdjust>
    <UIGraph v-model="form.viewline" :dot_data="dotData"></UIGraph>
</template>

<script setup>

const form = ref({
    c_model: 'Parabolic',
    viewline: true,
    //Все, что ниже в форме нужно только лишь за тем, чтобы это перезаписать
    fc_p: 5,
    h0: 100,
    yb: 200,
    fc_c: 5,
    h: 100,
    hm: 200,
    status: true
});
const form_sentParams = ref()
const paramForm = (param_form) => {
    form_sentParams.value =  param_form
    form.value.fc_p = form_sentParams.value.Parabolic.paramValues[0]
    form.value.h0 = form_sentParams.value.Parabolic.paramValues[1]
    form.value.yb = form_sentParams.value.Parabolic.paramValues[2]
    form.value.fc_c = form_sentParams.value.Chapman.paramValues[0]
    form.value.h = form_sentParams.value.Chapman.paramValues[1]
    form.value.hm = form_sentParams.value.Chapman.paramValues[2]
    form.value.status = form_sentParams.value.status
}


const dotData = ref();
const url = computed(() => (`/api/ne/${form.value.c_model}`))
useFetch(() => unref(url), { 
//для обращения к серверу (куда мы будем делать запрос, объект со свойствами)
    query: unref(form),
    onResponse({ response }) { 
    // декомпозиция (вытаскивание из объекта свойства)
        if(form.value.status)
        dotData.value = response._data;
    },
})

</script>