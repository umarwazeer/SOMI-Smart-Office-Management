<template>
  <div class="payroll-page q-pa-lg">
    <!-- Page Header -->
    <div class="page-header q-mb-lg">
      <div class="header-content">
        <div class="eyebrow">FINANCE & WORKFORCE</div>

        <div class="page-title-row">
          <div class="page-icon">
            <q-icon name="payments" size="25px" />
          </div>

          <div>
            <h1 class="page-title">Payroll Reports</h1>
            <p class="page-subtitle">
              Manage salary records, payments and payroll information
            </p>
          </div>
        </div>
      </div>

      <div class="header-actions">
        <q-btn
          flat
          no-caps
          icon="refresh"
          label="Refresh"
          class="header-btn"
          :loading="loading"
          @click="loadPayroll"
        />

        <q-btn
          flat
          no-caps
          icon="print"
          label="Print"
          class="header-btn"
          :disable="loading || payrollData.length === 0"
          @click="printReport"
        />

        <q-btn
          v-if="canManage"
          unelevated
          no-caps
          color="primary"
          icon="add"
          label="Create Payroll"
          class="create-btn"
          @click="openCreatePayroll"
        />
      </div>
    </div>

    <!-- Error -->
    <q-banner
      v-if="errorMessage"
      class="error-banner q-mb-lg"
      rounded
    >
      <template #avatar>
        <q-icon name="error_outline" />
      </template>

      {{ errorMessage }}

      <template #action>
        <q-btn
          flat
          dense
          no-caps
          label="Retry"
          @click="loadPayroll"
        />
      </template>
    </q-banner>

    <!-- Summary Cards -->
    <div class="summary-grid q-mb-lg">
      <q-card class="summary-card">
        <div class="summary-icon summary-icon--records">
          <q-icon name="receipt_long" size="21px" />
        </div>

        <div class="summary-content">
          <div class="summary-label">Payroll Records</div>
          <div class="summary-value">
            {{ payrollData.length }}
          </div>
          <div class="summary-caption">
            Total records
          </div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--paid">
          <q-icon name="account_balance_wallet" size="21px" />
        </div>

        <div class="summary-content">
          <div class="summary-label">Total Payroll</div>
          <div class="summary-value">
            {{ formatAmount(totalPayroll) }}
          </div>
          <div class="summary-caption">
            Total salary amount
          </div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--deductions">
          <q-icon name="remove_circle_outline" size="21px" />
        </div>

        <div class="summary-content">
          <div class="summary-label">Deductions</div>
          <div class="summary-value">
            {{ formatAmount(totalDeductions) }}
          </div>
          <div class="summary-caption">
            Total deductions
          </div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--employees">
          <q-icon name="groups" size="21px" />
        </div>

        <div class="summary-content">
          <div class="summary-label">Employees Paid</div>
          <div class="summary-value">
            {{ uniqueEmployees }}
          </div>
          <div class="summary-caption">
            Unique employees
          </div>
        </div>
      </q-card>
    </div>

    <!-- Filters -->
    <q-card class="filter-card q-mb-lg">
      <q-card-section class="filter-section">
        <div class="filter-heading">
          <div class="filter-title-row">
            <q-icon name="tune" size="18px" />
            <span>Payroll Filters</span>
          </div>

          <q-btn
            flat
            dense
            no-caps
            icon="restart_alt"
            label="Clear"
            class="clear-btn"
            :disable="!hasActiveFilters"
            @click="clearFilters"
          />
        </div>

        <div class="filter-grid">
          <!-- Search -->
          <q-input
            v-model="filters.search"
            outlined
            dense
            clearable
            label="Search employee"
            placeholder="Name or employee ID"
            class="filter-control search-control"
          >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <!-- Department -->
          <q-select
            v-model="filters.department"
            :options="departmentOptions"
            option-label="name"
            option-value="id"
            emit-value
            map-options
            outlined
            dense
            clearable
            label="Department"
            class="filter-control"
          />

          <!-- Payroll Period -->
          <q-select
            v-model="filters.payroll_period"
            :options="payrollPeriodOptions"
            option-label="label"
            option-value="value"
            emit-value
            map-options
            outlined
            dense
            clearable
            label="Payroll Period"
            class="filter-control"
          />

          <!-- Payment Method -->
          <q-select
            v-model="filters.payment_method"
            :options="paymentMethodOptions"
            option-label="label"
            option-value="value"
            emit-value
            map-options
            outlined
            dense
            clearable
            label="Payment Method"
            class="filter-control"
          />

          <!-- From Date -->
          <q-input
            v-model="filters.date_from"
            outlined
            dense
            type="date"
            label="From Date"
            class="filter-control"
          />

          <!-- To Date -->
          <q-input
            v-model="filters.date_to"
            outlined
            dense
            type="date"
            label="To Date"
            class="filter-control"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Payroll Table -->
    <q-card class="table-card">
      <q-card-section class="table-header">
        <div>
          <div class="table-title">Payroll Records</div>

          <div class="table-subtitle">
            {{ filteredRows.length }}
            record{{ filteredRows.length === 1 ? '' : 's' }}
            available
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <q-table
        :rows="filteredRows"
        :columns="columns"
        row-key="id"
        :loading="loading"
        flat
        class="payroll-table"
        :rows-per-page-options="[10, 20, 50, 0]"
        no-data-label="No payroll records found"
        loading-label="Loading payroll records..."
      >
        <!-- Employee -->
        <template #body-cell-employee="props">
          <q-td :props="props">
            <div class="employee-cell">
              <q-avatar
                size="38px"
                class="employee-avatar"
              >
                {{ getInitials(props.row.employee_name) }}
              </q-avatar>

              <div class="employee-info">
                <div class="employee-name">
                  {{ props.row.employee_name || 'Unknown Employee' }}
                </div>

                <div class="employee-id">
                  {{ props.row.employee_id || '—' }}
                </div>
              </div>
            </div>
          </q-td>
        </template>

        <!-- Department -->
        <template #body-cell-department="props">
          <q-td :props="props">
            <div class="department-cell">
              <q-icon name="business" size="16px" />
              <span>
                {{ props.row.department_name || 'No Department' }}
              </span>
            </div>
          </q-td>
        </template>

        <!-- Basic Salary -->
        <template #body-cell-basic_salary="props">
          <q-td :props="props">
            <span class="money-value">
              {{ formatAmount(props.row.basic_salary) }}
            </span>
          </q-td>
        </template>

        <!-- Allowances -->
        <template #body-cell-other_allowances="props">
          <q-td :props="props">
            <span class="allowance-value">
              + {{ formatAmount(props.row.other_allowances) }}
            </span>
          </q-td>
        </template>

        <!-- Deductions -->
        <template #body-cell-deductions="props">
          <q-td :props="props">
            <span class="deduction-value">
              - {{ formatAmount(props.row.deductions) }}
            </span>
          </q-td>
        </template>

        <!-- Total -->
        <template #body-cell-total_salary="props">
          <q-td :props="props">
            <span class="total-value">
              {{ formatAmount(props.row.total_salary) }}
            </span>
          </q-td>
        </template>

        <!-- Period -->
        <template #body-cell-payroll_period="props">
          <q-td :props="props">
            <q-badge class="period-badge">
              {{ formatPeriod(props.row.payroll_period) }}
            </q-badge>
          </q-td>
        </template>

        <!-- Payment Method -->
        <template #body-cell-payment_method="props">
          <q-td :props="props">
            <div class="payment-method">
              <q-icon
                :name="getPaymentIcon(props.row.payment_method)"
                size="16px"
              />

              <span>
                {{ formatPaymentMethod(props.row.payment_method) }}
              </span>
            </div>
          </q-td>
        </template>

        <!-- Payment Date -->
        <template #body-cell-payment_date="props">
          <q-td :props="props">
            <div class="date-cell">
              <q-icon name="event" size="15px" />
              {{ formatDate(props.row.payment_date) }}
            </div>
          </q-td>
        </template>

        <!-- Actions -->
        <template #body-cell-actions="props">
          <q-td :props="props">
            <div class="action-group">
              <q-btn
                round
                flat
                dense
                icon="visibility"
                class="action-btn"
                aria-label="View payroll"
                @click="viewPayroll(props.row)"
              >
                <q-tooltip>
                  View Details
                </q-tooltip>
              </q-btn>

              <q-btn
                v-if="canManage"
                round
                flat
                dense
                icon="edit"
                class="action-btn"
                aria-label="Edit payroll"
                @click="editPayroll(props.row)"
              >
                <q-tooltip>
                  Edit Payroll
                </q-tooltip>
              </q-btn>

              <q-btn
                v-if="canAdmin"
                round
                flat
                dense
                icon="delete_outline"
                color="negative"
                class="action-btn"
                aria-label="Delete payroll"
                @click="confirmDelete(props.row)"
              >
                <q-tooltip>
                  Delete Payroll
                </q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

        <!-- Empty -->
        <template #no-data>
          <div class="empty-state">
            <q-icon name="payments" size="44px" />

            <div class="empty-title">
              No Payroll Records
            </div>

            <div class="empty-text">
              No payroll records match the selected filters.
            </div>
          </div>
        </template>
      </q-table>
    </q-card>

    <!-- Payroll Details Dialog -->
    <q-dialog v-model="detailsDialog">
      <q-card class="details-card">
        <q-card-section class="details-header">
          <div class="details-heading">
            <div class="details-icon">
              <q-icon name="receipt_long" size="22px" />
            </div>

            <div>
              <div class="details-title">
                Payroll Details
              </div>

              <div class="details-subtitle">
                Complete salary and payment information
              </div>
            </div>
          </div>

          <q-btn
            round
            flat
            dense
            icon="close"
            @click="detailsDialog = false"
          />
        </q-card-section>

        <q-separator />

        <q-card-section
          v-if="selectedPayroll"
          class="details-content"
        >
          <div class="details-employee">
            <q-avatar
              size="54px"
              class="details-avatar"
            >
              {{ getInitials(selectedPayroll.employee_name) }}
            </q-avatar>

            <div>
              <div class="details-employee-name">
                {{ selectedPayroll.employee_name || 'Unknown Employee' }}
              </div>

              <div class="details-employee-meta">
                {{ selectedPayroll.employee_id || '—' }}

                <span v-if="selectedPayroll.department_name">
                  •
                </span>

                {{ selectedPayroll.department_name || 'No Department' }}
              </div>
            </div>
          </div>

          <div class="details-section">
            <div class="details-section-title">
              Salary Breakdown
            </div>

            <div class="salary-breakdown">
              <div class="breakdown-item">
                <span>Basic Salary</span>

                <strong>
                  {{ formatAmount(selectedPayroll.basic_salary) }}
                </strong>
              </div>

              <div class="breakdown-item">
                <span>Other Allowances</span>

                <strong class="positive">
                  + {{ formatAmount(selectedPayroll.other_allowances) }}
                </strong>
              </div>

              <div class="breakdown-item">
                <span>Deductions</span>

                <strong class="negative">
                  - {{ formatAmount(selectedPayroll.deductions) }}
                </strong>
              </div>

              <q-separator />

              <div class="breakdown-total">
                <span>Net Salary</span>

                <strong>
                  {{ formatAmount(selectedPayroll.total_salary) }}
                </strong>
              </div>
            </div>
          </div>

          <div class="details-grid">
            <div class="detail-box">
              <span>Payroll Period</span>

              <strong>
                {{ formatPeriod(selectedPayroll.payroll_period) }}
              </strong>
            </div>

            <div class="detail-box">
              <span>Payment Method</span>

              <strong>
                {{ formatPaymentMethod(selectedPayroll.payment_method) }}
              </strong>
            </div>

            <div class="detail-box">
              <span>Payment Date</span>

              <strong>
                {{ formatDate(selectedPayroll.payment_date) }}
              </strong>
            </div>

            <div class="detail-box">
              <span>Record ID</span>

              <strong>
                #{{ selectedPayroll.id }}
              </strong>
            </div>
          </div>

          <div
            v-if="selectedPayroll.description"
            class="description-box"
          >
            <div class="description-label">
              Description
            </div>

            <div class="description-text">
              {{ selectedPayroll.description }}
            </div>
          </div>
        </q-card-section>

        <q-card-actions class="details-footer">
          <q-btn
            flat
            no-caps
            label="Close"
            @click="detailsDialog = false"
          />

          <q-space />

          <q-btn
            v-if="selectedPayroll && canManage"
            unelevated
            no-caps
            color="primary"
            icon="edit"
            label="Edit Payroll"
            @click="editPayroll(selectedPayroll)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Create Payroll Dialog -->
    <q-dialog
      v-model="createDialog"
      persistent
      transition-show="scale"
      transition-hide="scale"
    >
      <q-card class="create-payroll-card">
        <q-card-section class="create-dialog-header">
          <div class="create-dialog-heading">
            <div class="create-dialog-icon">
              <q-icon name="payments" size="22px" />
            </div>

            <div>
              <div class="create-dialog-title">
                Create Payroll
              </div>

              <div class="create-dialog-subtitle">
                Add a new employee payroll record
              </div>
            </div>
          </div>

          <q-btn
            round
            flat
            dense
            icon="close"
            @click="closeCreateDialog"
          />
        </q-card-section>

        <q-separator />

        <q-card-section class="create-dialog-content">
          <NewPayroll
            @saved="handlePayrollSaved"
            @cancel="closeCreateDialog"
          />
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { Dialog, Notify } from 'quasar'
import api from 'src/services/api'
import NewPayroll from './new_payroll.vue'

export default {
  name: 'PayrollReport',

  components: {
    NewPayroll
  },

  data() {
    return {
      payrollData: [],
      departments: [],

      loading: false,
      errorMessage: '',

      detailsDialog: false,
      createDialog: false,

      selectedPayroll: null,

      filters: {
        search: '',
        department: null,
        payroll_period: null,
        payment_method: null,
        date_from: '',
        date_to: ''
      },

      payrollPeriodOptions: [
        {
          label: 'Weekly',
          value: 'WEEKLY'
        },
        {
          label: 'Bi-weekly',
          value: 'BI_WEEKLY'
        },
        {
          label: 'Monthly',
          value: 'MONTHLY'
        }
      ],

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

      columns: [
        {
          name: 'employee',
          label: 'Employee',
          field: 'employee_name',
          align: 'left',
          sortable: true
        },
        {
          name: 'department',
          label: 'Department',
          field: 'department_name',
          align: 'left',
          sortable: true
        },
        {
          name: 'basic_salary',
          label: 'Basic Salary',
          field: 'basic_salary',
          align: 'right',
          sortable: true
        },
        {
          name: 'other_allowances',
          label: 'Allowances',
          field: 'other_allowances',
          align: 'right',
          sortable: true
        },
        {
          name: 'deductions',
          label: 'Deductions',
          field: 'deductions',
          align: 'right',
          sortable: true
        },
        {
          name: 'total_salary',
          label: 'Net Salary',
          field: 'total_salary',
          align: 'right',
          sortable: true
        },
        {
          name: 'payroll_period',
          label: 'Period',
          field: 'payroll_period',
          align: 'left',
          sortable: true
        },
        {
          name: 'payment_method',
          label: 'Payment',
          field: 'payment_method',
          align: 'left',
          sortable: true
        },
        {
          name: 'payment_date',
          label: 'Payment Date',
          field: 'payment_date',
          align: 'left',
          sortable: true
        },
        {
          name: 'actions',
          label: 'Actions',
          field: 'actions',
          align: 'right'
        }
      ]
    }
  },

  computed: {
    role() {
      return String(
        this.$store.getters.userRole ||
        this.$store.getters.role ||
        this.$store.state?.auth?.user?.role ||
        ''
      ).toUpperCase()
    },

    canManage() {
      return (
        this.role === 'ADMIN' ||
        this.role === 'MANAGER'
      )
    },

    canAdmin() {
      return this.role === 'ADMIN'
    },

    departmentOptions() {
      return this.departments || []
    },

    hasActiveFilters() {
      return Boolean(
        this.filters.search ||
        this.filters.department ||
        this.filters.payroll_period ||
        this.filters.payment_method ||
        this.filters.date_from ||
        this.filters.date_to
      )
    },

    /*
     * Filters only affect the table.
     * Summary cards intentionally use payrollData directly.
     */
    filteredRows() {
      const search = String(
        this.filters.search || ''
      )
        .trim()
        .toLowerCase()

      let selectedDepartmentName = ''

      if (this.filters.department) {
        const department = this.departments.find(
          item =>
            String(item.id) ===
            String(this.filters.department)
        )

        selectedDepartmentName =
          String(department?.name || '').toLowerCase()
      }

      return this.payrollData.filter(row => {
        if (search) {
          const employeeName = String(
            row.employee_name || ''
          ).toLowerCase()

          const employeeId = String(
            row.employee_id || ''
          ).toLowerCase()

          if (
            !employeeName.includes(search) &&
            !employeeId.includes(search)
          ) {
            return false
          }
        }

        if (
          selectedDepartmentName &&
          String(row.department_name || '')
            .toLowerCase() !== selectedDepartmentName
        ) {
          return false
        }

        if (
          this.filters.payroll_period &&
          row.payroll_period !==
            this.filters.payroll_period
        ) {
          return false
        }

        if (
          this.filters.payment_method &&
          row.payment_method !==
            this.filters.payment_method
        ) {
          return false
        }

        if (
          this.filters.date_from &&
          row.payment_date <
            this.filters.date_from
        ) {
          return false
        }

        if (
          this.filters.date_to &&
          row.payment_date >
            this.filters.date_to
        ) {
          return false
        }

        return true
      })
    },

    /*
     * Summary cards intentionally use ALL payroll records.
     */
    totalPayroll() {
      return this.payrollData.reduce(
        (total, row) =>
          total + Number(row.total_salary || 0),
        0
      )
    },

    totalDeductions() {
      return this.payrollData.reduce(
        (total, row) =>
          total + Number(row.deductions || 0),
        0
      )
    },

    uniqueEmployees() {
      return new Set(
        this.payrollData
          .map(row => row.employee)
          .filter(Boolean)
      ).size
    }
  },

  mounted() {
    this.loadInitialData()
  },

  methods: {
    async loadInitialData() {
      await Promise.all([
        this.loadDepartments(),
        this.loadPayroll()
      ])
    },

    async loadDepartments() {
      try {
        const response = await api.get(
          '/departments/'
        )

        this.departments = Array.isArray(
          response.data
        )
          ? response.data
          : response.data?.results || []
      } catch (error) {
        console.error(
          'Failed to load departments:',
          error
        )
      }
    },

    async loadPayroll() {
      this.loading = true
      this.errorMessage = ''

      try {
        /*
         * Load the complete payroll dataset.
         * Filters are intentionally handled locally
         * so summary cards stay independent.
         */
        const response = await api.get(
          '/payroll/'
        )

        this.payrollData = Array.isArray(
          response.data
        )
          ? response.data
          : response.data?.results || []
      } catch (error) {
        console.error(
          'Failed to load payroll:',
          error
        )

        this.payrollData = []

        this.errorMessage =
          error.response?.data?.detail ||
          'Unable to load payroll records. Please try again.'
      } finally {
        this.loading = false
      }
    },

    clearFilters() {
      this.filters = {
        search: '',
        department: null,
        payroll_period: null,
        payment_method: null,
        date_from: '',
        date_to: ''
      }
    },

    openCreatePayroll() {
      this.createDialog = true
    },

    closeCreateDialog() {
      this.createDialog = false
    },

    async handlePayrollSaved() {
      this.createDialog = false
      await this.loadPayroll()

      Notify.create({
        type: 'positive',
        message:
          'Payroll record created successfully.',
        position: 'top-right'
      })
    },

    editPayroll(row) {
      if (!row?.id) {
        return
      }

      this.detailsDialog = false

      this.$router.push({
        path: '/edit_payroll',
        query: {
          id: row.id
        }
      })
    },

    viewPayroll(row) {
      this.selectedPayroll = row
      this.detailsDialog = true
    },

    confirmDelete(row) {
      if (!row?.id) {
        return
      }

      Dialog.create({
        title: 'Delete Payroll Record',

        message:
          `Are you sure you want to delete the payroll record for ` +
          `${row.employee_name || 'this employee'}? ` +
          `This action cannot be undone.`,

        cancel: {
          flat: true,
          noCaps: true,
          label: 'Cancel'
        },

        ok: {
          unelevated: true,
          noCaps: true,
          color: 'negative',
          label: 'Delete'
        },

        persistent: true
      }).onOk(() => {
        this.deletePayroll(row)
      })
    },

    async deletePayroll(row) {
      try {
        await api.delete(
          `/payroll/${row.id}/`
        )

        Notify.create({
          type: 'positive',
          message:
            'Payroll record deleted successfully.',
          position: 'top-right'
        })

        await this.loadPayroll()
      } catch (error) {
        console.error(
          'Failed to delete payroll:',
          error
        )

        Notify.create({
          type: 'negative',
          message:
            error.response?.data?.detail ||
            'Unable to delete payroll record.',
          position: 'top-right'
        })
      }
    },

    formatAmount(value) {
      const amount = Number(value || 0)

      return `Rs. ${amount.toLocaleString(
        'en-PK',
        {
          minimumFractionDigits: 0,
          maximumFractionDigits: 2
        }
      )}`
    },

    formatDate(value) {
      if (!value) {
        return '—'
      }

      const parts = String(value).split('-')

      if (parts.length !== 3) {
        return value
      }

      return `${parts[2]}-${parts[1]}-${parts[0]}`
    },

    formatPeriod(value) {
      const labels = {
        WEEKLY: 'Weekly',
        BI_WEEKLY: 'Bi-weekly',
        MONTHLY: 'Monthly'
      }

      return labels[value] || value || '—'
    },

    formatPaymentMethod(value) {
      const labels = {
        CASH: 'Cash',
        BANK_TRANSFER: 'Bank Transfer',
        CHEQUE: 'Cheque'
      }

      return labels[value] || value || '—'
    },

    getPaymentIcon(value) {
      switch (value) {
        case 'CASH':
          return 'payments'

        case 'CHEQUE':
          return 'description'

        case 'BANK_TRANSFER':
        default:
          return 'account_balance'
      }
    },

    getInitials(name) {
      if (!name) {
        return 'EM'
      }

      const words = String(name)
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (words.length === 1) {
        return words[0]
          .slice(0, 2)
          .toUpperCase()
      }

      return (
        words[0].charAt(0) +
        words[words.length - 1].charAt(0)
      ).toUpperCase()
    },

    printReport() {
      const rows = this.filteredRows

      if (!rows.length) {
        Notify.create({
          type: 'warning',
          message:
            'There are no payroll records to print.',
          position: 'top-right'
        })

        return
      }

      const reportRows = rows
        .map(row => {
          return `
            <tr>
              <td>${this.escapeHtml(
                row.employee_name || '—'
              )}</td>
              <td>${this.escapeHtml(
                row.employee_id || '—'
              )}</td>
              <td>${this.escapeHtml(
                row.department_name || '—'
              )}</td>
              <td>${this.formatAmount(
                row.basic_salary
              )}</td>
              <td>${this.formatAmount(
                row.other_allowances
              )}</td>
              <td>${this.formatAmount(
                row.deductions
              )}</td>
              <td>${this.formatAmount(
                row.total_salary
              )}</td>
              <td>${this.escapeHtml(
                this.formatPeriod(
                  row.payroll_period
                )
              )}</td>
              <td>${this.escapeHtml(
                this.formatDate(
                  row.payment_date
                )
              )}</td>
            </tr>
          `
        })
        .join('')

      const printWindow = window.open(
        '',
        '_blank',
        'width=1200,height=800'
      )

      if (!printWindow) {
        Notify.create({
          type: 'negative',
          message:
            'Please allow pop-ups to print the report.',
          position: 'top-right'
        })

        return
      }

      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
          <head>
            <title>SOMI Payroll Report</title>

            <style>
              body {
                font-family: Arial, sans-serif;
                margin: 32px;
                color: #172033;
              }

              h1 {
                margin: 0;
                font-size: 24px;
              }

              .subtitle {
                margin-top: 6px;
                color: #64748b;
                font-size: 13px;
              }

              .summary {
                display: flex;
                gap: 18px;
                margin: 24px 0;
              }

              .summary-box {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                min-width: 170px;
              }

              .summary-label {
                color: #64748b;
                font-size: 11px;
              }

              .summary-value {
                margin-top: 4px;
                font-size: 18px;
                font-weight: bold;
              }

              table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 18px;
              }

              th,
              td {
                border: 1px solid #dbe2ea;
                padding: 8px;
                text-align: left;
                font-size: 11px;
              }

              th {
                background: #f1f5f9;
                font-weight: bold;
              }

              .footer {
                margin-top: 24px;
                color: #64748b;
                font-size: 10px;
              }

              @media print {
                body {
                  margin: 15px;
                }
              }
            </style>
          </head>

          <body>
            <h1>SOMI — Payroll Report</h1>

            <div class="subtitle">
              Smart Office Management & Intelligence
            </div>

            <div class="summary">
              <div class="summary-box">
                <div class="summary-label">
                  Payroll Records
                </div>

                <div class="summary-value">
                  ${rows.length}
                </div>
              </div>

              <div class="summary-box">
                <div class="summary-label">
                  Total Payroll
                </div>

                <div class="summary-value">
                  ${this.formatAmount(
                    this.totalPayroll
                  )}
                </div>
              </div>

              <div class="summary-box">
                <div class="summary-label">
                  Total Deductions
                </div>

                <div class="summary-value">
                  ${this.formatAmount(
                    this.totalDeductions
                  )}
                </div>
              </div>

              <div class="summary-box">
                <div class="summary-label">
                  Employees Paid
                </div>

                <div class="summary-value">
                  ${this.uniqueEmployees}
                </div>
              </div>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Employee ID</th>
                  <th>Department</th>
                  <th>Basic Salary</th>
                  <th>Allowances</th>
                  <th>Deductions</th>
                  <th>Net Salary</th>
                  <th>Period</th>
                  <th>Payment Date</th>
                </tr>
              </thead>

              <tbody>
                ${reportRows}
              </tbody>
            </table>

            <div class="footer">
              Generated by SOMI Payroll Management
            </div>
          </body>
        </html>
      `)

      printWindow.document.close()
      printWindow.focus()

      setTimeout(() => {
        printWindow.print()
        printWindow.close()
      }, 250)
    },

    escapeHtml(value) {
      return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
    }
  }
}
</script>

<style scoped>
.payroll-page {
  min-height: 100%;
  background: #f7f9fc;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.header-content {
  min-width: 0;
}

.eyebrow {
  margin-bottom: 7px;
  color: #7b8798;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.11em;
}

.page-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 12px;
  background: #eaf2ff;
  color: #2563eb;
}

.page-title {
  margin: 0;
  color: #172033;
  font-size: 24px;
  font-weight: 750;
  line-height: 1.2;
}

.page-subtitle {
  margin: 5px 0 0;
  color: #7a8699;
  font-size: 12px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.header-btn {
  min-height: 38px;
  border: 1px solid #e1e7ef;
  border-radius: 8px;
  background: #ffffff;
  color: #526071;
}

.create-btn {
  min-height: 38px;
  border-radius: 8px;
  padding: 0 15px;
}

.error-banner {
  border: 1px solid #fecaca;
  background: #fff7f7;
  color: #991b1b;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.summary-card {
  min-height: 88px;
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 14px 16px;
  border: 1px solid #e6ebf1;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 3px 12px rgba(15, 23, 42, 0.045);
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease;
}

.summary-card:hover {
  border-color: #d3dce7;
  box-shadow: 0 7px 20px rgba(15, 23, 42, 0.075);
  transform: translateY(-1px);
}

.summary-icon {
  width: 43px;
  height: 43px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 9px;
}

.summary-icon--records {
  background: #eef4ff;
  color: #2563eb;
}

.summary-icon--paid {
  background: #ecfdf5;
  color: #059669;
}

.summary-icon--deductions {
  background: #fff7ed;
  color: #ea580c;
}

.summary-icon--employees {
  background: #f3efff;
  color: #7c3aed;
}

.summary-content {
  min-width: 0;
}

.summary-label {
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.2;
}

.summary-value {
  margin-top: 3px;
  color: #172033;
  font-size: 20px;
  font-weight: 750;
  line-height: 1.15;
  white-space: nowrap;
}

.summary-caption {
  margin-top: 3px;
  color: #9aa5b5;
  font-size: 9px;
}

.filter-card,
.table-card {
  border: 1px solid #e5eaf0;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
}

.filter-section {
  padding: 16px;
}

.filter-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 14px;
}

.filter-title-row {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #344054;
  font-size: 12px;
  font-weight: 700;
}

.filter-title-row .q-icon {
  color: #2563eb;
}

.clear-btn {
  color: #667085;
  font-size: 11px;
}

.filter-grid {
  display: grid;
  grid-template-columns:
    minmax(220px, 1.65fr)
    repeat(5, minmax(115px, 1fr));
  gap: 10px;
  align-items: center;
}

.filter-control {
  min-width: 0;
}

.filter-control :deep(.q-field__control) {
  min-height: 40px;
  border-radius: 8px;
}

.filter-control :deep(.q-field__label) {
  font-size: 11px;
}

.search-control {
  min-width: 220px;
}

.table-header {
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 14px 17px;
}

.table-title {
  color: #1f2937;
  font-size: 14px;
  font-weight: 700;
}

.table-subtitle {
  margin-top: 3px;
  color: #98a2b3;
  font-size: 10px;
}

.payroll-table {
  border-radius: 0 0 12px 12px;
}

.payroll-table :deep(thead tr) {
  background: #f8fafc;
}

.payroll-table :deep(th) {
  height: 46px;
  color: #667085;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.payroll-table :deep(td) {
  height: 61px;
  color: #344054;
  font-size: 11px;
  border-color: #edf0f4;
}

.payroll-table :deep(tbody tr:hover) {
  background: #fafcff;
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 170px;
}

.employee-avatar {
  flex-shrink: 0;
  background: #eaf2ff;
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
}

.employee-info {
  min-width: 0;
}

.employee-name {
  color: #344054;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.3;
}

.employee-id {
  margin-top: 2px;
  color: #98a2b3;
  font-size: 9px;
}

.department-cell,
.payment-method,
.date-cell {
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}

.department-cell {
  color: #526071;
}

.department-cell .q-icon,
.payment-method .q-icon,
.date-cell .q-icon {
  color: #98a2b3;
}

.money-value {
  color: #526071;
  font-weight: 600;
  white-space: nowrap;
}

.allowance-value {
  color: #059669;
  font-weight: 600;
  white-space: nowrap;
}

.deduction-value {
  color: #dc2626;
  font-weight: 600;
  white-space: nowrap;
}

.total-value {
  color: #172033;
  font-weight: 750;
  white-space: nowrap;
}

.period-badge {
  padding: 5px 8px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #526071;
  font-size: 9px;
  font-weight: 700;
}

.payment-method {
  color: #526071;
}

.date-cell {
  color: #667085;
}

.action-group {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2px;
}

.action-btn {
  color: #667085;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #2563eb;
}

.empty-state {
  min-height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 35px 20px;
  color: #98a2b3;
  text-align: center;
}

.empty-state > .q-icon {
  color: #c5ccd6;
}

.empty-title {
  margin-top: 10px;
  color: #526071;
  font-size: 14px;
  font-weight: 700;
}

.empty-text {
  margin-top: 4px;
  color: #98a2b3;
  font-size: 11px;
}

.details-card,
.create-payroll-card {
  width: 650px;
  max-width: 94vw;
  max-height: 90vh;
  overflow: hidden;
  border-radius: 16px;
  background: #ffffff;
}

.details-header,
.create-dialog-header {
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 14px 18px;
}

.details-heading,
.create-dialog-heading {
  display: flex;
  align-items: center;
  gap: 11px;
}

.details-icon,
.create-dialog-icon {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  background: #eaf2ff;
  color: #2563eb;
}

.details-title,
.create-dialog-title {
  color: #172033;
  font-size: 16px;
  font-weight: 700;
}

.details-subtitle,
.create-dialog-subtitle {
  margin-top: 3px;
  color: #98a2b3;
  font-size: 10px;
}

.details-content,
.create-dialog-content {
  max-height: calc(90vh - 80px);
  overflow-y: auto;
  padding: 18px;
}

.create-dialog-content {
  padding: 0;
}

.details-employee {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 13px;
  border: 1px solid #e5eaf0;
  border-radius: 11px;
  background: #f8fafc;
}

.details-avatar {
  background: #eaf2ff;
  color: #2563eb;
  font-size: 15px;
  font-weight: 700;
}

.details-employee-name {
  color: #1f2937;
  font-size: 14px;
  font-weight: 700;
}

.details-employee-meta {
  margin-top: 3px;
  color: #7a8699;
  font-size: 10px;
}

.details-section {
  margin-top: 20px;
}

.details-section-title {
  margin-bottom: 10px;
  color: #344054;
  font-size: 12px;
  font-weight: 700;
}

.salary-breakdown {
  padding: 13px;
  border: 1px solid #e5eaf0;
  border-radius: 11px;
}

.breakdown-item,
.breakdown-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 7px 0;
  color: #667085;
  font-size: 11px;
}

.breakdown-item strong {
  color: #344054;
  font-size: 11px;
}

.breakdown-item .positive {
  color: #059669;
}

.breakdown-item .negative {
  color: #dc2626;
}

.breakdown-total {
  padding-top: 12px;
  color: #344054;
  font-weight: 700;
}

.breakdown-total strong {
  color: #172033;
  font-size: 15px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 12px;
}

.detail-box {
  padding: 11px;
  border: 1px solid #e5eaf0;
  border-radius: 9px;
  background: #ffffff;
}

.detail-box span {
  display: block;
  color: #98a2b3;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}

.detail-box strong {
  display: block;
  margin-top: 4px;
  color: #344054;
  font-size: 11px;
}

.description-box {
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #e5eaf0;
  border-radius: 9px;
  background: #f8fafc;
}

.description-label {
  color: #98a2b3;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}

.description-text {
  margin-top: 5px;
  color: #475467;
  font-size: 11px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.details-footer {
  min-height: 60px;
  padding: 9px 16px;
  background: #ffffff;
}

.details-footer :deep(.q-btn) {
  min-height: 36px;
  border-radius: 8px;
}

@media (max-width: 1250px) {
  .filter-grid {
    grid-template-columns:
      minmax(200px, 1.5fr)
      repeat(2, minmax(140px, 1fr));
  }
}

@media (max-width: 1100px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .payroll-table {
    min-width: 1050px;
  }

  .table-card {
    overflow: hidden;
  }

  .payroll-table :deep(.q-table__middle) {
    overflow-x: auto;
  }
}

@media (max-width: 750px) {
  .payroll-page {
    padding: 16px !important;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .header-btn,
  .create-btn {
    flex: 1;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .search-control {
    min-width: 0;
  }

  .summary-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .summary-card {
    min-height: 78px;
    padding: 12px 14px;
  }

  .summary-value {
    font-size: 19px;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 430px) {
  .page-title {
    font-size: 20px;
  }

  .page-subtitle {
    font-size: 11px;
  }

  .page-icon {
    width: 43px;
    height: 43px;
  }

  .header-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .create-btn {
    grid-column: 1 / -1;
  }

  .details-card,
  .create-payroll-card {
    max-width: 96vw;
    border-radius: 14px;
  }

  .details-content {
    padding: 14px;
  }
}

.body--dark .payroll-page {
  background: #0f1722;
}

.body--dark .page-title,
.body--dark .table-title,
.body--dark .details-title,
.body--dark .create-dialog-title,
.body--dark .details-section-title {
  color: #e5e7eb;
}

.body--dark .page-subtitle,
.body--dark .eyebrow,
.body--dark .table-subtitle,
.body--dark .summary-caption,
.body--dark .details-subtitle,
.body--dark .create-dialog-subtitle {
  color: #94a3b8;
}

.body--dark .page-icon,
.body--dark .details-icon,
.body--dark .create-dialog-icon {
  background: #172554;
  color: #60a5fa;
}

.body--dark .header-btn,
.body--dark .summary-card,
.body--dark .filter-card,
.body--dark .table-card,
.body--dark .details-card,
.body--dark .create-payroll-card {
  background: #111827;
  border-color: #263244;
}

.body--dark .summary-card {
  box-shadow: none;
}

.body--dark .summary-label,
.body--dark .filter-title-row,
.body--dark .table-title {
  color: #cbd5e1;
}

.body--dark .summary-value,
.body--dark .total-value {
  color: #f1f5f9;
}

.body--dark .payroll-table :deep(thead tr) {
  background: #18212f;
}

.body--dark .payroll-table :deep(th) {
  color: #94a3b8;
}

.body--dark .payroll-table :deep(td) {
  color: #cbd5e1;
  border-color: #263244;
}

.body--dark .payroll-table :deep(tbody tr:hover) {
  background: #18212f;
}

.body--dark .employee-name,
.body--dark .money-value,
.body--dark .department-cell,
.body--dark .payment-method,
.body--dark .date-cell {
  color: #cbd5e1;
}

.body--dark .employee-id {
  color: #718096;
}

.body--dark .employee-avatar,
.body--dark .details-avatar {
  background: #172554;
  color: #60a5fa;
}

.body--dark .period-badge {
  background: #202a38;
  color: #cbd5e1;
}

.body--dark .action-btn {
  color: #94a3b8;
}

.body--dark .action-btn:hover {
  background: #202a38;
  color: #60a5fa;
}

.body--dark .empty-title {
  color: #cbd5e1;
}

.body--dark .empty-text,
.body--dark .empty-state > .q-icon {
  color: #718096;
}

.body--dark .details-employee,
.body--dark .description-box {
  background: #202a38;
  border-color: #303b4d;
}

.body--dark .details-employee-name,
.body--dark .detail-box strong,
.body--dark .breakdown-item strong,
.body--dark .breakdown-total {
  color: #e5e7eb;
}

.body--dark .details-employee-meta,
.body--dark .detail-box span,
.body--dark .description-label {
  color: #94a3b8;
}

.body--dark .salary-breakdown,
.body--dark .detail-box {
  background: #111827;
  border-color: #303b4d;
}

.body--dark .breakdown-item,
.body--dark .description-text {
  color: #cbd5e1;
}

.body--dark .details-footer {
  background: #18212f;
}

</style>
