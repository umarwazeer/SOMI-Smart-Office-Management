<template>
  <div class="q-pa-md">
    <div class="row">
      <div class="col q-pt-lg">
        <div class="text-h5">Employee Payment</div>
      </div>
      <div class="col-auto q-gutter-x-sm q-py-md">
        <q-btn
          label="Add Salary"
          style="width: 160px"
          color="primary"
          dense
          icon="add"
          @click="open('top')"
          class="float-right text-capitalize text-body1"
        >
        </q-btn>
        <q-btn
          class="q-ml-md text-capitalize"
          label="Print Report"
          icon="print"
          color="secondary"
          @click="printReport"
        />
        <span class="row q-gutter-l-sm items-start q-pr-md">
          <q-select
            v-model="selectedYear"
            :options="years"
            label="Year"
            outlined
            dense
          />
          <q-select
            v-model="selectedMonth"
            :options="months"
            label="Month"
            outlined
            dense
          />
          <q-btn
            label="Apply"
            color="primary"
            dense
            @click="applyFilter"
          />
        </span>
      </div>
    </div>
    <q-separator />
    <q-table
      ref="myTable"
      :position="position"
      :class="tableClass"
      tabindex="0"
      title="Employee Salary"
      :rows="filteredRows"
      :columns="columns"
      dense
      row-key="id"
      selection="multiple"
      v-model:selected.sync="selected"
      :pagination.sync="pagination"
      :filter="filter"
      @focusin.native="activateNavigation"
      @focusout.native="deactivateNavigation"
      @keydown.native="onKey"
    >
      <template v-slot:body-cell-status="props">
        <q-td>
          <q-badge
            :props="props"
            :class="props.row.status == 'Present' ? 'bg-cyan-4 text-white  q-px-xs   text-body2  text-body1' : 'bg-red-4 text-white  q-px-xs   text-body2  text-body1' "
            outline
          >
            {{ props.row.status }}
          </q-badge>
        </q-td>
      </template>
      <template v-slot:top-right>
        <div class="row q-gutter-sm q-py-md">
          <div class="col">
            <q-input
              label="Type a keyword here"
              class=""
              style="width: 200px"
              outlined
              dense
              rounded
              v-model="filter"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
        </div>
      </template>
    </q-table>
    <q-dialog v-model="dialog">
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="q-pt-none">
          <New_payroll/>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="OK" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from 'vue'
import Payroll from "../EmployeeReports/PayrollReport.vue";

export default {
  components: {
   Payroll
  },
  setup () {
    const dialog = ref(false)
    const position = ref('top')
    const selectedYear = ref(null)
    const selectedMonth = ref(null)

    const years = Array.from({length: 5}, (_, i) => new Date().getFullYear() - i)
    const months = [
      {label: 'January', value: 1},
      {label: 'February', value: 2},
      {label: 'March', value: 3},
      {label: 'April', value: 4},
      {label: 'May', value: 5},
      {label: 'June', value: 6},
      {label: 'July', value: 7},
      {label: 'August', value: 8},
      {label: 'September', value: 9},
      {label: 'October', value: 10},
      {label: 'November', value: 11},
      {label: 'December', value: 12},
    ]

    const applyFilter = () => {
      // Fetch data based on selectedYear and selectedMonth
      fetchData(selectedYear.value, selectedMonth.value)
    }

    const fetchData = (year, month) => {
      axios
        .get(`http://127.0.0.1:2024/payroll?year=${year}&month=${month}`)
        .then((response) => {
          this.rows = response.data;
          console.log("new response", response);
        })
        .catch((error) => {
          console.log(error);
        });
    }

    return {
      dialog,
      position,
      selectedYear,
      selectedMonth,
      years,
      months,
      applyFilter
    }
  },
  data() {
    return {
      filter: "",
      selected: [],
      pagination: {},
      columns: [
        { name: "employee_id", align: "left", label: "Employee_Id", field: "employee_id" },
        { name: "basic_salary", align: "left", label: "Basic Salary", field: "basic_salary" },
        { name: "totalSalary", align: "left", label: "Total Salary", field: "totalSalary" },
        { name: "employee_name", required: true, label: "UserName", align: "left", field: (row) => row.employee_name, format: (val) => `${val}`, sortable: true },
        { name: "department_name", align: "center", label: "Deparmtment", align: "left", field: "department_name", sortable: true },
        { name: "payment_date", label: "payment_date", field: "payment_date", align: "left", sortable: true },
        { name: "payment_method", align: "left", label: "payment_method", field: "payment_method", required: true, sortable: true },
        { name: "deductions", label: "deductions", align: "center", field: "deductions", required: true, sortable: true },
        { name: "payroll_period", label: "payroll_period", field: "payroll_period", sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) },
      ],
      rows: [],
    };
  },
  mounted() {
    this.showData();
  },
  computed: {
    tableClass() {
      return this.navigationActive === true ? "shadow-8 no-outline" : void 0;
    },
  },
  methods: {
    showData() {
      axios
        .get("http://127.0.0.1:2024/payroll")
        .then((response) => {
          this.rows = response.data;
          console.log("new response", response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    printReport() {
      // You can implement printing functionality here
      console.log("Printing report...");
    },
  },
};
</script>
