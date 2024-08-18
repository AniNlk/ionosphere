<template>
    <div style="display: flex; flex-direction: row;">
        <div style="display: flex; flex-direction: column;">
            <UIFieldNumber 
            v-for="i in form.Parabolic.params.length" 
            v-if="view.c_model == 'Parabolic'" 
            v-model="form.Parabolic.paramValues[i-1]" 
            name 
            :label="form.Parabolic.paramNames[i-1]" 
            @keyup="sendData"
            @click="sendData"
            />
            <UIFieldNumber 
            v-for="i in form.Chapman.params.length" 
            v-if="view.c_model == 'Chapman'" 
            v-model="form.Chapman.paramValues[i-1]" 
            :label="form.Chapman.paramNames[i-1]" 
            @keyup="sendData"
            @click="sendData"
            />
        </div>
        <p style="margin-left: 2rem ; color: red" v-if="!out.success">{{ out.error.issues[out.error.issues.length-1].message }}</p>
    </div>
    <UIFieldCheckbox 
    v-model="view.viewline" 
    :active="['включено','отключено']"
    />
    <UIFieldSelect 
    v-model="view.c_model" 
    :models="mymodels"
    @change="sendData"
    />
    <!-- <p v-if="status === 'pending'">Пожалуйста, подождите...</p> -->
</template>

<script setup>
    const view = defineModel()
    const emits = defineEmits(['send_form', 'send_status'])
    const mymodels = ['Parabolic', 'Chapman']

    const form = ref({
        Parabolic: {
            params: ['fc', 'h0', 'yb'],
            paramValues: [5, 100, 200],
            paramNames: ['Максимум электронной концентрации', 'Высота минимума электронной концентрации', 'Полувысота слоя'],
    }, Chapman: {
        params: ['fc', 'h', 'hm'],
        paramValues: [5, 100, 200],
        paramNames: ['Максимум электронной концентрации', 'Высота минимума электронной концентрации', 'Высота максимума электронной концентрации'],
    }, status: true
    })
    
    //Validation
    import {z} from "zod"
    const arg = z.object({
        params: z.array(z.string()),
        paramValues: z.array(z.number({
    required_error: "Поле должно быть заполнено",
    invalid_type_error: "Введите данные",
}).positive({ message: "Все значения должны быть положительны" }))
}).refine(data => {
    const fcIndex = data.params.indexOf('fc');
    if (fcIndex !== -1) {
        const fcValue = data.paramValues[fcIndex];
        const minValid = z.number().min(1, { message: "Значение должно быть больше 0" }).safeParse(fcValue);
        const maxValid = z.number().max(20, { message: "Значение должно быть не более 20" }).safeParse(fcValue);
    return minValid.success && maxValid.success;
}
  return true;
}, 
{message: "Значение максимума должно быть между 1 и 20"}
);

const out = ref({success: true})
const sendData = () => {
    if (view.value.c_model === 'Parabolic') {
        out.value = arg.safeParse(form.value.Parabolic)
    } else if (view.value.c_model === 'Chapman') {
        out.value = arg.safeParse(form.value.Chapman)
    }
    form.value.status = out.value.success
    emits('send_form', form.value)
    console.log(out.value)
}
</script>