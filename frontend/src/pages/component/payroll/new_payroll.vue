<template>
  <div class="payroll-form">
    <div class="form-header">
      <div>
        <div class="form-kicker">
          {{ editing ? 'PAYROLL RECORD' : 'NEW PAYROLL' }}
        </div>

        <div class="form-title">
          {{ editing ? 'Edit Payroll' : 'Create Payroll' }}
        </div>

        <div class="form-subtitle">
          {{
            editing
              ? 'Update the selected employee payroll record.'
              : 'Create a salary and payment record for an employee.'
          }}
        </div>
      </div>

      <q-btn
        flat
        round
        dense
        icon="close"
        class="close-btn"
        :disable="saving"
        @click="$emit('cancel')"
      />
    </div>

    <q-separator />

    <q-form
      ref="payrollForm"
      class="form-body"
      @submit.prevent="savePayroll"
    >
      <!-- Employee -->
      <section class="form-section">
        <div class="section-heading">
          <div class="section-icon">
            <q-icon name="person" />
          </div>

          <div>
            <div class="section-title">
              Employee
            </div>

            <div class="section-description">
              Select the employee receiving this payroll.
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col-12">
            <q-select
              v-model="item.employee"
              outlined
              dense
              use-input
              clearable
              emit-value
              map-options
              input-debounce="0"
              label="Employee"
              placeholder="Search and select employee"
              :options="employeeOptions"
              :loading="employeesLoading"
              :disable="editing"
              :rules="[requiredRule]"
              @filter="filterEmployees"
              @update:model-value="handleEmployeeChange"
            >
              <template #prepend>
                <q-icon name="badge" />
              </template>

              <template #option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section avatar>
                    <q-avatar
                      size="36px"
                      class="employee-avatar"
                    >
                      {{ getInitials(scope.opt.name, scope.opt.employee_id) }}
                    </q-avatar>
                  </q-item-section>

                  <q-item-section>
                    <q-item-label class="employee-option-name">
                      {{ scope.opt.name }}
                    </q-item-label>

                    <q-item-label caption>
                      {{ scope.opt.employee_id }}

                      <span v-if="scope.opt.department_name">
                        · {{ scope.opt.department_name }}
                      </span>
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </template>

              <template #selected-item="scope">
                <div class="selected-employee">
                  <q-avatar
                    size="26px"
                    class="employee-avatar"
                  >
                    {{ getInitials(scope.opt.name, scope.opt.employee_id) }}
                  </q-avatar>

                  <span class="selected-employee-name">
                    {{ scope.opt.name }}
                  </span>
                </div>
              </template>

              <template #no-option>
                <q-item>
                  <q-item-section class="text-grey-6">
                    No employees found.
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
        </div>

        <div
          v-if="selectedEmployee"
          class="employee-summary"
        >
          <q-avatar
            size="40px"
            class="employee-avatar"
          >
            {{ getInitials(selectedEmployee.name, selectedEmployee.employee_id) }}
          </q-avatar>

          <div class="employee-summary-content">
            <div class="employee-summary-name">
              {{ selectedEmployee.name }}
            </div>

            <div class="employee-summary-meta">
              {{ selectedEmployee.employee_id || 'No ID' }}

              <span v-if="selectedEmployee.department_name">
                · {{ selectedEmployee.department_name }}
              </span>

              <span v-if="selectedEmployee.job_title">
                · {{ selectedEmployee.job_title }}
              </span>
            </div>
          </div>

          <div class="employee-summary-salary">
            <span>Current Salary</span>

            <strong>
              {{ formatCurrency(selectedEmployee.salary) }}
            </strong>
          </div>
        </div>
      </section>

      <!-- Salary -->
      <section class="form-section">
        <div class="section-heading">
          <div class="section-icon">
            <q-icon name="payments" />
          </div>

          <div>
            <div class="section-title">
              Salary Details
            </div>

            <div class="section-description">
              Define earnings, allowances and deductions.
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col-12 col-md-4">
            <q-input
              v-model.number="item.basic_salary"
              outlined
              dense
              type="number"
              min="0"
              step="0.01"
              label="Basic Salary"
              :rules="[requiredRule, nonNegativeRule]"
              @update:model-value="calculateTotalSalary"
            >
              <template #prepend>
                <span class="currency-label">
                  Rs.
                </span>
              </template>
            </q-input>
          </div>

          <div class="col-12 col-md-4">
            <q-input
              v-model.number="item.other_allowances"
              outlined
              dense
              type="number"
              min="0"
              step="0.01"
              label="Other Allowances"
              :rules="[nonNegativeRule]"
              @update:model-value="calculateTotalSalary"
            >
              <template #prepend>
                <q-icon name="add_card" />
              </template>
            </q-input>
          </div>

          <div class="col-12 col-md-4">
            <q-input
              v-model.number="item.deductions"
              outlined
              dense
              type="number"
              min="0"
              step="0.01"
              label="Deductions"
              :rules="[nonNegativeRule]"
              @update:model-value="calculateTotalSalary"
            >
              <template #prepend>
                <q-icon name="remove_circle_outline" />
              </template>
            </q-input>
          </div>
        </div>

        <div class="salary-calculation">
          <div class="calculation-label">
            <div class="calculation-title">
              Net Salary
            </div>

            <div class="calculation-description">
              Basic salary + allowances − deductions
            </div>
          </div>

          <div class="calculation-value">
            {{ formatCurrency(item.totalSalary) }}
          </div>
        </div>
      </section>

      <!-- Payment -->
      <section class="form-section">
        <div class="section-heading">
          <div class="section-icon">
            <q-icon name="receipt_long" />
          </div>

          <div>
            <div class="section-title">
              Payment Information
            </div>

            <div class="section-description">
              Set the payroll period and payment details.
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col-12 col-md-4">
            <q-select
              v-model="item.payroll_period"
              outlined
              dense
              emit-value
              map-options
              label="Payroll Period"
              :options="payrollPeriodOptions"
              :rules="[requiredRule]"
            >
              <template #prepend>
                <q-icon name="calendar_month" />
              </template>
            </q-select>
          </div>

          <div class="col-12 col-md-4">
            <q-select
              v-model="item.payment_method"
              outlined
              dense
              emit-value
              map-options
              label="Payment Method"
              :options="paymentMethodOptions"
              :rules="[requiredRule]"
            >
              <template #prepend>
                <q-icon name="account_balance_wallet" />
              </template>
            </q-select>
          </div>

          <div class="col-12 col-md-4">
            <q-input
              v-model="item.payment_date"
              outlined
              dense
              type="date"
              label="Payment Date"
              :rules="[requiredRule]"
            >
              <template #prepend>
                <q-icon name="event" />
              </template>
            </q-input>
          </div>
        </div>

        <div class="q-mt-sm">
          <q-input
            v-model="item.description"
            outlined
            dense
            type="textarea"
            autogrow
            label="Description"
            placeholder="Add optional notes about this payroll..."
            maxlength="500"
            counter
          >
            <template #prepend>
              <q-icon name="notes" />
            </template>
          </q-input>
        </div>
      </section>

      <!-- Error -->
      <q-banner
        v-if="errorMessage"
        rounded
        class="error-banner"
      >
        <template #avatar>
          <q-icon name="error_outline" />
        </template>

        {{ errorMessage }}
      </q-banner>

      <!-- Footer -->
      <div class="form-footer">
        <q-btn
          flat
          label="Cancel"
          class="cancel-button text-capitalize"
          :disable="saving"
          @click="$emit('cancel')"
        />

        <q-btn
          unelevated
          color="primary"
          :icon="editing ? 'save' : 'add'"
          :label="editing ? 'Update Payroll' : 'Save Payroll'"
          class="save-button text-capitalize"
          :loading="saving"
          type="submit"
        />
      </div>
    </q-form>
  </div>
</template>

<script>
import api from 'src/services/api'

export default {
  name: 'NewPayroll',

  props: {
    payroll: {
      type: Object,
      default: null
    },

    editing: {
      type: Boolean,
      default: false
    }
  },

  emits: ['saved', 'cancel'],

  data () {
    return {
      saving: false,
      employeesLoading: false,
      errorMessage: '',

      employees: [],
      filteredEmployees: [],

      item: {
        employee: null,
        basic_salary: 0,
        other_allowances: 0,
        deductions: 0,
        totalSalary: 0,
        description: '',
        payment_method: '',
        payment_date: this.getToday(),
        payroll_period: ''
      },

      paymentMethodOptions: [
        {
          label: 'Cash',
          value: 'CASH'
        },
        {
          label: 'Bank Transfer',
          value: 'BANK_TRANSFER'
        },
        {
          label: 'Cheque',
          value: 'CHEQUE'
        }
      ],

      payrollPeriodOptions: [
        {
          label: 'Monthly',
          value: 'MONTHLY'
        },
        {
          label: 'Bi-weekly',
          value: 'BI_WEEKLY'
        },
        {
          label: 'Weekly',
          value: 'WEEKLY'
        }
      ]
    }
  },

  computed: {
    employeeOptions () {
      return this.filteredEmployees.map(employee => ({
        label: employee.name,
        value: employee.id,
        name: employee.name,
        employee_id: employee.employee_id,
        department_name: employee.department_name,
        job_title: employee.job_title,
        salary: employee.salary
      }))
    },

    selectedEmployee () {
      return this.employees.find(
        employee => employee.id === this.item.employee
      ) || null
    }
  },

  watch: {
    payroll: {
      immediate: true,
      deep: true,
      handler (value) {
        if (value) {
          this.loadPayroll(value)
        } else {
          this.resetForm()
        }
      }
    }
  },

  mounted () {
    this.loadEmployees()
  },

  methods: {
    async loadEmployees () {
      this.employeesLoading = true

      try {
        const response = await api.get('/employees/')

        const data = Array.isArray(response.data)
          ? response.data
          : (response.data?.results || [])

        this.employees = data.map(employee => ({
          ...employee,
          name:
            employee.full_name ||
            employee.name ||
            employee.username ||
            employee.employee_id ||
            'Unknown Employee'
        }))

        this.filteredEmployees = [...this.employees]

        if (this.payroll) {
          this.loadPayroll(this.payroll)
        }
      } catch (error) {
        console.error('Employees load error:', error)

        this.errorMessage =
          'Unable to load employees. Please refresh and try again.'
      } finally {
        this.employeesLoading = false
      }
    },

    filterEmployees (value, update) {
      update(() => {
        const search = String(value || '').toLowerCase().trim()

        if (!search) {
          this.filteredEmployees = [...this.employees]
          return
        }

        this.filteredEmployees = this.employees.filter(employee => {
          const text = [
            employee.name,
            employee.employee_id,
            employee.department_name,
            employee.job_title
          ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()

          return text.includes(search)
        })
      })
    },

    handleEmployeeChange (employeeId) {
      const employee = this.employees.find(
        item => item.id === employeeId
      )

      if (!employee) {
        return
      }

      if (!this.editing) {
        this.item.basic_salary = Number(employee.salary || 0)
        this.calculateTotalSalary()
      }
    },

    loadPayroll (payroll) {
      this.errorMessage = ''

      const employeeId =
        typeof payroll.employee === 'object'
          ? payroll.employee?.id
          : payroll.employee

      this.item = {
        employee: employeeId || null,
        basic_salary: Number(payroll.basic_salary || 0),
        other_allowances: Number(payroll.other_allowances || 0),
        deductions: Number(payroll.deductions || 0),
        totalSalary: Number(
          payroll.total_salary ??
          payroll.totalSalary ??
          0
        ),
        description: payroll.description || '',
        payment_method: payroll.payment_method || '',
        payment_date: payroll.payment_date || this.getToday(),
        payroll_period: payroll.payroll_period || ''
      }

      this.calculateTotalSalary()
    },

    calculateTotalSalary () {
      const basic = Number(this.item.basic_salary || 0)
      const allowances = Number(this.item.other_allowances || 0)
      const deductions = Number(this.item.deductions || 0)

      this.item.totalSalary = Math.max(
        0,
        basic + allowances - deductions
      )
    },

    async savePayroll () {
      this.errorMessage = ''

      const valid = await this.$refs.payrollForm.validate()

      if (!valid) {
        return
      }

      this.calculateTotalSalary()

      const basic = Number(this.item.basic_salary || 0)
      const allowances = Number(this.item.other_allowances || 0)
      const deductions = Number(this.item.deductions || 0)

      if (!this.item.employee) {
        this.errorMessage = 'Please select an employee.'
        return
      }

      if (deductions > basic + allowances) {
        this.errorMessage =
          'Deductions cannot be greater than total earnings.'
        return
      }

      const payload = {
        employee: this.item.employee,
        basic_salary: basic,
        other_allowances: allowances,
        deductions,
        total_salary: Number(this.item.totalSalary || 0),
        payment_date: this.item.payment_date,
        payment_method: this.item.payment_method,
        payroll_period: this.item.payroll_period,
        description: this.item.description || ''
      }

      this.saving = true

      try {
        let response

        if (this.editing && this.payroll?.id) {
          response = await api.patch(
            `/payroll/${this.payroll.id}/`,
            payload
          )
        } else {
          response = await api.post(
            '/payroll/',
            payload
          )
        }

        this.$q.notify({
          type: 'positive',
          position: 'top',
          message: this.editing
            ? 'Payroll updated successfully.'
            : 'Payroll created successfully.'
        })

        this.$emit('saved', response.data)
      } catch (error) {
        console.error('Payroll save error:', error)

        this.errorMessage = this.getApiError(error)

        this.$q.notify({
          type: 'negative',
          position: 'top',
          message: this.errorMessage
        })
      } finally {
        this.saving = false
      }
    },

    getApiError (error) {
      const data = error.response?.data

      if (!data) {
        return 'Unable to save payroll. Please try again.'
      }

      if (typeof data === 'string') {
        return data
      }

      if (data.detail) {
        return data.detail
      }

      const messages = []

      Object.keys(data).forEach(key => {
        const value = data[key]

        if (Array.isArray(value)) {
          messages.push(`${key}: ${value.join(', ')}`)
        } else if (typeof value === 'string') {
          messages.push(`${key}: ${value}`)
        } else if (value && typeof value === 'object') {
          messages.push(`${key}: ${JSON.stringify(value)}`)
        }
      })

      return messages.length
        ? messages.join(' | ')
        : 'Unable to save payroll. Please check the entered information.'
    },

    resetForm () {
      this.errorMessage = ''

      this.item = {
        employee: null,
        basic_salary: 0,
        other_allowances: 0,
        deductions: 0,
        totalSalary: 0,
        description: '',
        payment_method: '',
        payment_date: this.getToday(),
        payroll_period: ''
      }

      this.$nextTick(() => {
        if (this.$refs.payrollForm) {
          this.$refs.payrollForm.resetValidation()
        }
      })
    },

    getToday () {
      const date = new Date()

      return [
        date.getFullYear(),
        String(date.getMonth() + 1).padStart(2, '0'),
        String(date.getDate()).padStart(2, '0')
      ].join('-')
    },

    requiredRule (value) {
      return (
        value !== null &&
        value !== undefined &&
        value !== ''
      ) || 'This field is required.'
    },

    nonNegativeRule (value) {
      if (
        value === null ||
        value === undefined ||
        value === ''
      ) {
        return true
      }

      return Number(value) >= 0 || 'Value cannot be negative.'
    },

    formatCurrency (value) {
      const amount = Number(value || 0)

      return `Rs. ${amount.toLocaleString('en-PK', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
      })}`
    },

    getInitials (name, employeeId) {
      if (name) {
        const parts = String(name)
          .trim()
          .split(/\s+/)
          .filter(Boolean)

        if (parts.length >= 2) {
          return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
        }

        return parts[0][0].toUpperCase()
      }

      if (employeeId) {
        return String(employeeId)
          .replace(/[^a-zA-Z0-9]/g, '')
          .slice(-2)
          .toUpperCase()
      }

      return 'EM'
    }
  }
}
</script>

<style scoped>
.payroll-form {
  width: 100%;
  background: #ffffff;
  color: #0f172a;
}

.form-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 15px 18px 13px;
}

.form-kicker {
  margin-bottom: 3px;
  color: #2563eb;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.form-title {
  color: #0f172a;
  font-size: 20px;
  font-weight: 800;
  line-height: 1.2;
}

.form-subtitle {
  margin-top: 3px;
  color: #64748b;
  font-size: 10px;
}

.close-btn {
  color: #64748b;
}

.form-body {
  padding: 15px 18px 17px;
}

.form-section {
  padding: 0;
}

.form-section + .form-section {
  margin-top: 18px;
  padding-top: 17px;
  border-top: 1px solid #e2e8f0;
}

.section-heading {
  display: flex;
  align-items: center;
  gap: 9px;
}

.section-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #eff6ff;
  color: #2563eb;
}

.section-icon .q-icon {
  font-size: 16px;
}

.section-title {
  color: #1e293b;
  font-size: 12px;
  font-weight: 750;
}

.section-description {
  margin-top: 2px;
  color: #94a3b8;
  font-size: 9px;
}

.employee-avatar {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
}

.employee-option-name {
  color: #1e293b;
  font-weight: 650;
}

.selected-employee {
  display: flex;
  align-items: center;
  gap: 7px;
}

.selected-employee-name {
  color: #1e293b;
  font-size: 12px;
}

.employee-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
  padding: 9px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 9px;
  background: #f8fafc;
}

.employee-summary-content {
  min-width: 0;
  flex: 1;
}

.employee-summary-name {
  color: #1e293b;
  font-size: 12px;
  font-weight: 700;
}

.employee-summary-meta {
  margin-top: 2px;
  color: #64748b;
  font-size: 9px;
}

.employee-summary-salary {
  text-align: right;
}

.employee-summary-salary span {
  display: block;
  color: #94a3b8;
  font-size: 8px;
}

.employee-summary-salary strong {
  display: block;
  margin-top: 2px;
  color: #1e293b;
  font-size: 11px;
}

.currency-label {
  color: #64748b;
  font-size: 10px;
  font-weight: 800;
}

.salary-calculation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-top: 8px;
  padding: 11px 13px;
  border: 1px solid #dbeafe;
  border-radius: 9px;
  background: #f8fbff;
}

.calculation-title {
  color: #1e293b;
  font-size: 11px;
  font-weight: 750;
}

.calculation-description {
  margin-top: 2px;
  color: #64748b;
  font-size: 8px;
}

.calculation-value {
  color: #2563eb;
  font-size: 18px;
  font-weight: 850;
  white-space: nowrap;
}

.error-banner {
  margin-top: 15px;
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
  font-size: 11px;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 7px;
  margin-top: 17px;
  padding-top: 13px;
  border-top: 1px solid #e2e8f0;
}

.cancel-button,
.save-button {
  min-height: 36px;
  border-radius: 7px;
}

.save-button {
  min-width: 130px;
}

:deep(.q-field__label) {
  color: #64748b;
  font-size: 10px;
}

:deep(.q-field__native),
:deep(.q-field__input) {
  color: #1e293b;
  font-size: 11px;
}

:deep(.q-field__marginal) {
  color: #64748b;
}

:deep(.q-field--outlined .q-field__control) {
  border-radius: 7px;
  min-height: 40px;
}

:deep(.q-field--outlined .q-field__control:before) {
  border-color: #cbd5e1;
}

:deep(.q-field--outlined.q-field--focused .q-field__control:after) {
  border-width: 1px;
}

@media (max-width: 600px) {
  .form-header,
  .form-body {
    padding-left: 13px;
    padding-right: 13px;
  }

  .form-title {
    font-size: 18px;
  }

  .employee-summary {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .employee-summary-salary {
    width: 100%;
    padding-left: 50px;
    text-align: left;
  }

  .salary-calculation {
    align-items: flex-start;
    flex-direction: column;
  }

  .calculation-value {
    width: 100%;
  }

  .form-footer {
    justify-content: stretch;
  }

  .form-footer .q-btn {
    flex: 1;
  }
}
</style>
