<template>
  <div class="tabulator-body">
    <!-- Buttons -->
    <div class="flex justify-end mb-[15px]">
      <button @click="toggleSettings" class="btn-outline" aria-label="Open settings">
        <Icon icon="gear" class="my-[2.5px]" />
      </button>
    </div>

    <!-- Table Block -->
    <div>
      <div ref="table" id="tabulator" :class="action ? 'tabulator-action' : ''"></div>
    </div>

    <!-- Settings Block -->
    <Modal :show="showSettings" @onClose="showSettings = false" @onSave="applySettings" :title="settings.title"
      :action="settings.action" width="600px">

      <div class="flex">
        <div class="w-[50%]">
          <span class="text-[16px] font-semibold">Columns Attributes</span>
          <div>
            <input v-model="columnSearch" class="input-text mb-[15px]" placeholder="Search for attributes"
              aria-label="Search columns" />
            <div v-for="(column, index) in filteredColumns" :key="column.field" class="my-[7.5px]">
              <div v-if="column.field !== 'action'" class="flex">
                <input type="checkbox" :disabled="!column.isNotMandatory" v-model="selectedColumnIds"
                  :value="column.field" class="mx-[5px]" aria-labelledby="column-checkbox" :id="column.title" />
                <div>
                  <label :for="column.title" class="select-none">{{ column.title }}</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Page Size -->
        <div class="w-[50%]">
          <span class="text-[16px] font-semibold">Page Size</span>
          <div class="mb-[15px]">
            <label v-for="size in paginationSizeSelector" :key="size" class="flex items-center mt-[7.5px]">
              <input type="radio" v-model="paginationSize" :value="size" class="mr-[10px]"
                aria-label="Select page size" />
              {{ size }}
            </label>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import type { TabulatorHeader, TabulatorData, TabulatorAction } from '@/dtos/components/tabulator';
import type { PropType } from 'vue';
import { getCurrentInstance } from 'vue';
import { TabulatorFull as Tabulator } from 'tabulator-tables';

const instance = getCurrentInstance();
const emit = instance?.emit;

const table = ref('');
const showSettings = ref(false);
const columnSearch = ref('');
const paginationSize = ref(25);
const selectedColumnIds = ref<string[]>([]);

let tabulatorInstance: Tabulator | null = null;
const selectedColumn = ref<TabulatorHeader[]>([]);

const settings = ref({
  title: [{ name: 'Settings' }],
  action: [
    { title: 'Cancel', emit: 'onClose', class: 'btn-outline' },
    { title: 'Apply', emit: 'onSave' },
  ],
});

const props = defineProps({
  data: {
    type: Array as PropType<TabulatorData[]>,
    required: true,
  },
  columns: {
    type: Array as PropType<TabulatorHeader[]>,
    required: true,
  },
  placeholder: String,
  paginationSize: { type: Number, default: 25 },
  paginationSizeSelector: { type: Array as PropType<number[]>, default: [25, 50, 100, 200] },
  action: {
    type: Boolean,
    default: false,
  },
  actionButtons: {
    type: Array as PropType<TabulatorAction[]>,
    default: [],
  },
  heightOffset: {
    type: Number,
    required: true,
  }
});

const filteredColumns = computed(() => {
  return props.columns.filter(col => col.title.toLowerCase().includes(columnSearch.value.toLowerCase()));
});

onMounted(() => {
  paginationSize.value = props.paginationSize;
  document.addEventListener('click', handleOutClick);
  initializeTabulator();
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutClick);
});

//Tabulator
const initializeTabulator = () => {
  selectedColumnIds.value = props.columns.map((col) => col.field);
  updateSelectedColumns();

  tabulatorInstance = new Tabulator(table.value, {
    data: props.data,
    columns: selectedColumn.value,
    placeholder: props.placeholder ? props.placeholder : "No records found!",
    pagination: true,
    paginationSize: paginationSize.value,
    paginationSizeSelector: props.paginationSizeSelector,
    layout: 'fitColumns',
    height: window.innerHeight - props.heightOffset,
  });
  tabulatorInstance.on('rowClick', function (e: any, row: any) {
    const dropdown = document.querySelector('.action-show');
    const isActionButtonClicked = e.target.closest('.action-btn');
    if (!isActionButtonClicked) {
      dropdown?.classList.remove('action-show');
    }
    if (props.action) {
      e.preventDefault();
      const doc = document.querySelector('.datarow-selected');
      if (doc) {
        doc.classList.remove('datarow-selected');
      }
      row.getElement().classList.add('datarow-selected');
    }
  });
};

const handleOutClick = (event: any) => {
  const dropdown = document.querySelector('.action-show');
  const mainDiv = document.getElementById('tabulator');
  const isRowClicked = event.target.closest('.tabulator-row');
  const isActionButtonClicked = event.target.closest('#action-btn');
  if (!mainDiv?.contains(event.target) || (!isRowClicked && !isActionButtonClicked)) {
    dropdown?.classList.remove('action-show');
  }
}

//Settings
const updateSelectedColumns = () => {
  selectedColumn.value = props.columns.filter((col) =>
    selectedColumnIds.value.includes(col.field)
  );

  if (props.action) {
    selectedColumn.value.push({
      title: 'Action',
      field: 'action',
      width: 99,
      vertAlign: 'middle',
      hozAlign: 'center',
      headerSort: false,
      formatter: (cell: any) => {
        const actions = props.actionButtons.map((e) => `<div class="p-[4.5px] hover:bg-primary-50 cursor-pointer transition-all flex gap-1 font-medium ${e.class}">${e.name}</div>`).join('');
        return `<div class="relative" id="action-btn">
                  <button class="action-btn btn btn-gray w-[40px] bg-[#EAEAEA] hover:bg-[#e1e1e1] text-secondary-500 flex justify-center">
                    <svg class="rotate-90 svg-inline--fa fa-ellipsis-vertical" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="ellipsis-vertical" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 512"><path class="" fill="currentColor" d="M64 360a56 56 0 1 0 0 112 56 56 0 1 0 0-112zm0-160a56 56 0 1 0 0 112 56 56 0 1 0 0-112zM120 96A56 56 0 1 0 8 96a56 56 0 1 0 112 0z"></path></svg>
                  </button>
                  <div class=" action-dropdown hidden select-none absolute bg-white z-3 border border-secondary-100 divide-y divide-secondary-100 min-w-[100px]">
                      ${actions}
                  </div>
                </div>`;
      },
      cellClick: (e, cell) => {
        const clickedElement = e.target;
        const actionBtn = clickedElement.closest('.action-btn');
        const parentDiv = clickedElement.closest('.relative');
        const tabelClass = document.querySelector('.tabulator-tableholder');
        if (tabelClass) {
          const tableRect = tabelClass.getBoundingClientRect();
          if (actionBtn && parentDiv) {
            const dropdown = parentDiv.querySelector('.action-dropdown');
            const isDropdownVisible = dropdown.classList.contains('action-show');
            document.querySelectorAll('.action-dropdown').forEach((el) => el.classList.remove('action-show'));
            if (!isDropdownVisible) {
              dropdown.style.top = "";
              dropdown.style.left = "";
              dropdown.style.right = "";
              dropdown.classList.add('action-show');
              dropdown.style.right = '0px';

              const dropdownRect = dropdown.getBoundingClientRect();

              if (dropdownRect.bottom > tableRect.bottom - 10) {
                dropdown.style.top = "-63px";
              } else {
                dropdown.style.top = "";
              }
            }
          }
        }
        props.actionButtons.forEach((action) => {
          if (clickedElement.classList.contains(action.class)) {
            if (emit) {
              const id = cell.getRow().getData().id;
              emit(action.emit, id);
            }
          }
        });
      },

    });
  }
};

const applySettings = () => {
  updateSelectedColumns();
  tabulatorInstance?.setColumns(selectedColumn.value);
  tabulatorInstance?.setPageSize(paginationSize.value);
  showSettings.value = false;
};

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};

watch(
  () => props.data,
  (newData) => {
    tabulatorInstance?.setData(newData);
  },
  { deep: true }
);

watch(
  () => props.columns,
  () => {
    updateSelectedColumns();
    tabulatorInstance?.setColumns(selectedColumn.value);
  },
  { deep: true }
);
</script>