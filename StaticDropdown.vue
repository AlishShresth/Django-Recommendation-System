<template>
  <div class="relative bg-white cursor-pointer" @blur="open = false" tabindex="0" :style="'width: ' + width"
    :id="generatedID">
    <div @click="open = !open"
      class="px-[10px] py-[2px] rounded-sm flex justify-between select-none border border-secondary-100 min-h-[30px]">
      <span class="truncate h-fit my-auto">{{ displayValue }}</span>
      <icon icon="chevron-down" class="my-auto w-[10px] duration-200 text-secondary-800"
        :class="open ? 'rotate-180' : ''" />
    </div>
    <div
      class="absolute right-0 bg-white z-[3] border border-secondary-100 divide-y divide-secondary-100 -mt-[2px] overflow-y-auto"
      :id="generatedID + '-drop'" :class="[open ? '' : 'hidden']"
      :style="'max-height: ' + height + '; width: ' + (childWidth != '' ? childWidth : mainWidth)">
      <div class="flex" v-for="(option, i) in options" @click="selectOption(option.id)" :key="i">
        <span class="px-[15px] py-[5px] hover:bg-primary-50 w-[100%]"
          :class="[modelValue === option.id ? 'bg-primary-50 border-secondary-200 border mx[-10px] ' +
            (((modelValue === option.id) && i == 0) ? (options.length == 1 ? '' : '-mb-[1px]') : i == options.length - 1 ? '-mt-[1px]' : '-my-[1px]') : '']">
          {{ option.name }}
        </span>
      </div>
      <div v-if="options.length == 0" class="px-[15px] py-[2px] w-[100%]">
        {{ noData }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeMount, onMounted } from 'vue';
import { ref } from 'vue';
import type { DropdownValue } from '@/dtos/components/static_dropdown.d.ts'
import type { PropType } from 'vue';

const generatedID = ref('');

const props = defineProps({
  modelValue: {
    type: [null, String, Number],
    required: true
  },
  options: {
    type: Array as PropType<DropdownValue[]>,
    required: true,
    default: () => []
  },
  width: {
    type: String,
    default: '200px',
  },
  childWidth: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '300px'
  },
  placeholder: {
    type: String,
    default: 'Please Select'
  },
  noData: {
    type: String,
    default: 'No Option Found'
  }
});

const emit = defineEmits(['update:modelValue']);
const open = ref(false);

const displayValue = props.placeholder;

const mainWidth = computed(() => {
  if (!props.childWidth) {
    nextTick(() => {
      const val = document.getElementById(generatedID.value);
      const val2 = document.getElementById(generatedID.value + "-drop");
      if (val2) {
        val2.style.width = val?.offsetWidth + "px";
      }
    })
  }
})

const generateID = () => {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < 9) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  generatedID.value = 'dropdown-' + result;
}

const selectOption = (id: string | number) => {
  emit('update:modelValue', id);
  open.value = false;
};

onMounted(() => {
  generateID();
})
</script>