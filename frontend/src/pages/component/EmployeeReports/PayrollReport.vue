<template>
  <div>
    <q-table
      :rows="payrollData"
      :columns="payrollColumns"
      row-key="id"
      dense
      flat
    />
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      payrollData: [],
      payrollColumns: [
        {
          name: 'payment_date',
          required: true,
          label: 'Payment Date',
          align: 'left',
          field: 'payment_date',
          format: val => formatDate(val)
        },
        {
          name: 'basic_salary',
          required: true,
          label: 'Basic Salary',
          align: 'left',
          field: 'basic_salary'
        },
        {
          name: 'total_salary',
          required: true,
          label: 'Total Salary',
          align: 'left',
          field: 'total_salary'
        },
        {
          name: 'deductions',
          required: true,
          label: 'Deductions',
          align: 'left',
          field: 'deductions' 
        },
        {
          name: 'payroll_period',
          required: true,
          label: 'Payroll Period',
          align: 'left',
          field: 'payroll_period'
        }
      ]
    }
  },
  mounted() {
    this.fetchPayrollData()
  },
  methods: {
    fetchPayrollData() {
      const employeeId = 123 // Replace with the actual employee ID
      axios.get(`/employees/${employeeId}/payroll`)
        .then(response => {
          this.payrollData = response.data
        })
        .catch(error => {
          console.error('Error fetching payroll data:', error)
        })
    }
  }
}
</script>

<style scoped>
/* Add styles as needed */
</style>
