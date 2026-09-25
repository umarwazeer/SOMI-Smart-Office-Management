<template>
  <div class="leave-page q-pa-md q-pa-lg-lg">
    <!-- Page Header -->
    <div class="row items-center justify-between q-col-gutter-md q-mb-lg">
      <div class="col-12 col-md">
        <div class="row items-center no-wrap">
          <div class="page-icon q-mr-md">
            <q-icon name="event_available" size="27px" />
          </div>

          <div>
            <div class="text-h5 text-weight-bold text-grey-9">
              Leave Request
            </div>

            <div class="text-body2 text-grey-6 q-mt-xs">
              Submit and manage employee leave applications.
            </div>
          </div>
        </div>
      </div>

      <div class="col-auto">
        <q-chip
          v-if="currentUserRole"
          dense
          outline
          color="primary"
          icon="verified_user"
        >
          {{ formattedRole }}
        </q-chip>
      </div>
    </div>

    <!-- Error Banner -->
    <q-banner
      v-if="errorMessage"
      rounded
      class="bg-red-1 text-negative q-mb-md"
    >
      <template v-slot:avatar>
        <q-icon name="error_outline" />
      </template>

      {{ errorMessage }}

      <template v-slot:action>
        <q-btn
          flat
          dense
          label="Dismiss"
          color="negative"
          @click="errorMessage = ''"
        />
      </template>
    </q-banner>

    <!-- Leave Form -->
    <q-card flat bordered class="leave-form-card">
      <q-card-section class="form-header">
        <div class="row items-center">
          <q-icon
            name="description"
            color="primary"
            size="22px"
            class="q-mr-sm"
          />

          <div>
            <div class="text-subtitle1 text-weight-bold">
              Leave Information
            </div>

            <div class="text-caption text-grey-6">
              Enter the leave details below.
            </div>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-section class="q-pa-md q-pa-lg-lg">
        <div class="row q-col-gutter-lg">
          <!-- Employee -->
          <div class="col-12 col-md-6">
            <q-select
              v-if="isAdminOrManager"
              v-model="form.employee"
              :options="filteredEmployees"
              option-value="id"
              option-label="display_name"
              emit-value
              map-options
              outlined
              dense
              clearable
              use-input
              input-debounce="250"
              label="Employee"
              placeholder="Select employee"
              :loading="employeesLoading"
              :disable="loading || employeesLoading"
              @filter="filterEmployees"
            >
              <template v-slot:prepend>
                <q-icon name="person_outline" color="primary" />
              </template>

              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No employees found
                  </q-item-section>
                </q-item>
              </template>
            </q-select>

            <q-input
              v-else
              :model-value="currentEmployeeDisplay"
              outlined
              dense
              readonly
              label="Employee"
            >
              <template v-slot:prepend>
                <q-icon name="person_outline" color="primary" />
              </template>
            </q-input>
          </div>

          <!-- Leave Type -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="form.leave_type"
              :options="leaveTypes"
              option-value="id"
              option-label="name"
              emit-value
              map-options
              outlined
              dense
              clearable
              label="Leave Type"
              placeholder="Select leave type"
              :loading="leaveTypesLoading"
              :disable="loading || leaveTypesLoading"
            >
              <template v-slot:prepend>
                <q-icon name="category" color="primary" />
              </template>

              <template v-slot:after>
                <q-btn
                  v-if="canManageLeaveTypes"
                  round
                  flat
                  dense
                  color="primary"
                  icon="add"
                  aria-label="Add leave type"
                  @click="openDialog"
                >
                  <q-tooltip>
                    Add Leave Type
                  </q-tooltip>
                </q-btn>
              </template>

              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No active leave types available
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>

          <!-- Request Date -->
          <div class="col-12 col-md-4">
            <q-input
              v-model="form.request_date"
              outlined
              dense
              readonly
              label="Request Date"
            >
              <template v-slot:prepend>
                <q-icon name="today" color="primary" />
              </template>
            </q-input>
          </div>

          <!-- From Date -->
          <div class="col-12 col-md-4">
            <q-input
              v-model="form.from_date"
              outlined
              dense
              clearable
              label="From Date"
              placeholder="YYYY-MM-DD"
              mask="####-##-##"
              :rules="[dateRule]"
              @update:model-value="calculateTotalDays"
            >
              <template v-slot:prepend>
                <q-icon name="event" color="primary" />
              </template>

              <template v-slot:append>
                <q-icon
                  name="event"
                  class="cursor-pointer"
                  color="grey-7"
                >
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date
                      v-model="form.from_date"
                      mask="YYYY-MM-DD"
                      @update:model-value="calculateTotalDays"
                    >
                      <div class="row items-center justify-end q-pa-sm">
                        <q-btn
                          v-close-popup
                          label="Close"
                          color="primary"
                          flat
                        />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>

          <!-- To Date -->
          <div class="col-12 col-md-4">
            <q-input
              v-model="form.to_date"
              outlined
              dense
              clearable
              label="To Date"
              placeholder="YYYY-MM-DD"
              mask="####-##-##"
              :rules="[dateRule]"
              @update:model-value="calculateTotalDays"
            >
              <template v-slot:prepend>
                <q-icon name="event" color="primary" />
              </template>

              <template v-slot:append>
                <q-icon
                  name="event"
                  class="cursor-pointer"
                  color="grey-7"
                >
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date
                      v-model="form.to_date"
                      mask="YYYY-MM-DD"
                      @update:model-value="calculateTotalDays"
                    >
                      <div class="row items-center justify-end q-pa-sm">
                        <q-btn
                          v-close-popup
                          label="Close"
                          color="primary"
                          flat
                        />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>

          <!-- Duration -->
          <div class="col-12">
            <div class="duration-box">
              <div class="row items-center justify-between">
                <div class="row items-center">
                  <div class="duration-icon">
                    <q-icon name="schedule" size="21px" />
                  </div>

                  <div class="q-ml-md">
                    <div class="text-caption text-grey-6">
                      Leave Duration
                    </div>

                    <div class="text-subtitle1 text-weight-bold text-grey-9">
                      {{ durationText }}
                    </div>
                  </div>
                </div>

                <div class="duration-number">
                  {{ form.total_days || 0 }}

                  <span>
                    {{ form.total_days === 1 ? 'day' : 'days' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="col-12">
            <q-input
              v-model="form.description"
              type="textarea"
              outlined
              autogrow
              rows="4"
              label="Reason / Description"
              placeholder="Briefly explain the reason for the leave..."
              maxlength="1000"
              counter
            >
              <template v-slot:prepend>
                <q-icon name="notes" color="primary" />
              </template>
            </q-input>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- Actions -->
      <q-card-actions
        align="right"
        class="q-pa-md q-pa-lg-lg"
      >
        <q-btn
          flat
          no-caps
          label="Clear"
          icon="restart_alt"
          color="grey-7"
          :disable="loading"
          @click="resetForm"
        />

        <q-btn
          unelevated
          no-caps
          label="Submit Request"
          icon="send"
          color="primary"
          :loading="loading"
          :disable="!canSubmit"
          @click="saveRequest"
        />
      </q-card-actions>
    </q-card>

    <!-- Add Leave Type -->
    <add-leave-type-dialog
      v-model="dialogVisible"
      ref="addLeaveTypeDialog"
      @add-leave-type="handleAddLeaveType"
    />
  </div>
</template>

<script>
import api from 'src/services/api'
import AddLeaveTypeDialog from '../Leave/AddLeaveTypeDialog.vue'

export default {
  name: 'LeavePage',

  components: {
    AddLeaveTypeDialog
  },

  props: {
    leaveData: {
      type: Object,
      default: null
    }
  },

  data () {
    return {
      dialogVisible: false,
      loading: false,
      employeesLoading: false,
      leaveTypesLoading: false,
      errorMessage: '',

      currentUser: null,

      employees: [],
      filteredEmployees: [],

      leaveTypes: [],

      form: {
        employee: null,
        leave_type: null,
        request_date: this.getToday(),
        from_date: '',
        to_date: '',
        total_days: 0,
        description: ''
      }
    }
  },

  computed: {
    currentUserRole () {
      return String(this.currentUser?.role || '').toUpperCase()
    },

    formattedRole () {
      const role = this.currentUserRole

      if (!role) {
        return ''
      }

      return role.charAt(0) + role.slice(1).toLowerCase()
    },

    isAdminOrManager () {
      return ['ADMIN', 'MANAGER'].includes(
        this.currentUserRole
      )
    },

    canManageLeaveTypes () {
      return ['ADMIN', 'MANAGER'].includes(
        this.currentUserRole
      )
    },

    currentEmployee () {
      if (!this.currentUser) {
        return null
      }

      if (this.currentUser.employee_profile) {
        return this.currentUser.employee_profile
      }

      return this.employees.find(
        employee =>
          employee.user === this.currentUser.id
      ) || null
    },

    currentEmployeeDisplay () {
      const employee = this.currentEmployee

      if (!employee) {
        return 'Current employee'
      }

      const name =
        employee.full_name ||
        employee.name ||
        employee.username ||
        'Current employee'

      const employeeId = employee.employee_id
        ? ` (${employee.employee_id})`
        : ''

      return `${name}${employeeId}`
    },

    durationText () {
      if (
        !this.form.from_date ||
        !this.form.to_date
      ) {
        return 'Select start and end dates'
      }

      if (!this.form.total_days) {
        return 'Invalid date range'
      }

      return `${this.form.from_date} → ${this.form.to_date}`
    },

    canSubmit () {
      const hasEmployee =
        !this.isAdminOrManager ||
        Boolean(this.form.employee)

      return (
        hasEmployee &&
        Boolean(this.form.leave_type) &&
        Boolean(this.form.from_date) &&
        Boolean(this.form.to_date) &&
        this.form.total_days > 0 &&
        !this.loading
      )
    }
  },

  mounted () {
    this.loadPageData()
  },

  methods: {
    getToday () {
      const date = new Date()

      const year = date.getFullYear()
      const month = String(
        date.getMonth() + 1
      ).padStart(2, '0')
      const day = String(
        date.getDate()
      ).padStart(2, '0')

      return `${year}-${month}-${day}`
    },

    async loadPageData () {
      this.errorMessage = ''

      /*
       * Load the current user FIRST.
       *
       * Employee loading depends on the user's role.
       * Previously these calls were made together with
       * Promise.all(), which meant loadEmployees() could
       * execute before currentUser was available.
       */
      await this.loadCurrentUser()

      await Promise.all([
        this.loadLeaveTypes(),
        this.loadEmployees()
      ])

      this.applyLeaveData()
      this.calculateTotalDays()
    },

    async loadCurrentUser () {
      try {
        const response = await api.get('/auth/me/')

        this.currentUser = response.data

        console.log(
          'SOMI current user:',
          this.currentUser
        )

        console.log(
          'SOMI current role:',
          this.currentUserRole
        )
      } catch (error) {
        console.error(
          'Failed to load current user:',
          error
        )

        const storedUser =
          localStorage.getItem('user')

        if (storedUser) {
          try {
            this.currentUser =
              JSON.parse(storedUser)
          } catch (parseError) {
            console.error(
              'Failed to parse stored user:',
              parseError
            )
          }
        }
      }
    },

    async loadLeaveTypes () {
      this.leaveTypesLoading = true

      try {
        const response =
          await api.get('/leave/types/')

        const data = Array.isArray(
          response.data
        )
          ? response.data
          : response.data?.results || []

        this.leaveTypes = data.filter(
          leaveType =>
            leaveType.is_active !== false
        )
      } catch (error) {
        console.error(
          'Failed to load leave types:',
          error
        )

        this.errorMessage =
          this.getApiErrorMessage(
            error,
            'Unable to load leave types.'
          )
      } finally {
        this.leaveTypesLoading = false
      }
    },

    async loadEmployees () {
      /*
       * Only Admin and Manager need to choose
       * an employee manually.
       */
      if (!this.isAdminOrManager) {
        this.employees = []
        this.filteredEmployees = []
        return
      }

      this.employeesLoading = true

      try {
        const response =
          await api.get('/employees/')

        const data = Array.isArray(
          response.data
        )
          ? response.data
          : response.data?.results || []

        this.employees = data.map(
          employee => ({
            ...employee,
            display_name:
              this.getEmployeeDisplayName(
                employee
              )
          })
        )

        this.filteredEmployees =
          [...this.employees]

        console.log(
          'SOMI employees loaded:',
          this.employees.length
        )
      } catch (error) {
        console.error(
          'Failed to load employees:',
          error
        )

        this.errorMessage =
          this.getApiErrorMessage(
            error,
            'Unable to load employees.'
          )
      } finally {
        this.employeesLoading = false
      }
    },

    getEmployeeDisplayName (employee) {
      const name =
        employee.full_name ||
        employee.name ||
        employee.username ||
        'Unnamed Employee'

      const employeeId =
        employee.employee_id
          ? ` • ${employee.employee_id}`
          : ''

      return `${name}${employeeId}`
    },

    filterEmployees (value, update) {
      update(() => {
        if (!value) {
          this.filteredEmployees =
            [...this.employees]
          return
        }

        const needle =
          String(value).toLowerCase()

        this.filteredEmployees =
          this.employees.filter(
            employee => {
              const text = [
                employee.full_name,
                employee.name,
                employee.username,
                employee.employee_id,
                employee.email,
                employee.job_title,
                employee.department_name
              ]
                .filter(Boolean)
                .join(' ')
                .toLowerCase()

              return text.includes(needle)
            }
          )
      })
    },

    applyLeaveData () {
      if (!this.leaveData) {
        return
      }

      this.form.employee =
        this.leaveData.employee || null

      this.form.leave_type =
        this.leaveData.leave_type || null

      this.form.request_date =
        this.leaveData.request_date ||
        this.getToday()

      this.form.from_date =
        this.leaveData.from_date || ''

      this.form.to_date =
        this.leaveData.to_date || ''

      this.form.total_days =
        this.leaveData.total_days || 0

      this.form.description =
        this.leaveData.description || ''
    },

    openDialog () {
      if (!this.canManageLeaveTypes) {
        return
      }

      this.dialogVisible = true
    },

    async handleAddLeaveType (newLeaveType) {
      if (!this.canManageLeaveTypes) {
        this.$q.notify({
          type: 'warning',
          message:
            'You do not have permission to add leave types.'
        })

        return
      }

      if (!newLeaveType) {
        return
      }

      const payload = {
        name:
          typeof newLeaveType === 'object'
            ? String(newLeaveType.name || '').trim()
            : String(newLeaveType).trim(),

        description:
          typeof newLeaveType === 'object'
            ? String(newLeaveType.description || '').trim()
            : '',

        default_days:
          typeof newLeaveType === 'object'
            ? Number(newLeaveType.default_days || 0)
            : 0,

        is_active:
          typeof newLeaveType === 'object'
            ? newLeaveType.is_active !== false
            : true
      }

      if (!payload.name) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please enter a leave type name.'
        })

        return
      }

      if (
        !Number.isInteger(payload.default_days) ||
        payload.default_days < 0
      ) {
        this.$q.notify({
          type: 'warning',
          message:
            'Default days must be a valid non-negative number.'
        })

        return
      }

      try {
        this.errorMessage = ''
        this.leaveTypesLoading = true

        const response =
          await api.post(
            '/leave/types/',
            payload
          )

        const createdLeaveType =
          response.data

        if (
          createdLeaveType &&
          createdLeaveType.id &&
          createdLeaveType.is_active !== false
        ) {
          const existingIndex =
            this.leaveTypes.findIndex(
              item =>
                item.id ===
                createdLeaveType.id
            )

          if (existingIndex === -1) {
            this.leaveTypes.push(
              createdLeaveType
            )
          } else {
            this.leaveTypes.splice(
              existingIndex,
              1,
              createdLeaveType
            )
          }

          this.form.leave_type =
            createdLeaveType.id
        } else {
          await this.loadLeaveTypes()
        }

        this.dialogVisible = false

        this.$q.notify({
          type: 'positive',
          icon: 'check_circle',
          message:
            'Leave type created successfully.'
        })
      } catch (error) {
        console.error(
          'Failed to create leave type:',
          error
        )

        const message =
          this.getApiErrorMessage(
            error,
            'Failed to create leave type.'
          )

        this.errorMessage = message

        this.$q.notify({
          type: 'negative',
          icon: 'error_outline',
          message
        })
      } finally {
        this.leaveTypesLoading = false
      }
    },

    dateRule (value) {
      if (!value) {
        return true
      }

      const validDate =
        /^\d{4}-\d{2}-\d{2}$/.test(
          value
        )

      return (
        validDate ||
        'Use YYYY-MM-DD format.'
      )
    },

    calculateTotalDays () {
      if (
        !this.form.from_date ||
        !this.form.to_date
      ) {
        this.form.total_days = 0
        return
      }

      const fromDate =
        this.parseDate(
          this.form.from_date
        )

      const toDate =
        this.parseDate(
          this.form.to_date
        )

      if (!fromDate || !toDate) {
        this.form.total_days = 0
        return
      }

      const difference =
        toDate.getTime() -
        fromDate.getTime()

      const days =
        Math.floor(
          difference /
          (1000 * 60 * 60 * 24)
        ) + 1

      this.form.total_days =
        days > 0 ? days : 0
    },

    parseDate (value) {
      if (
        !/^\d{4}-\d{2}-\d{2}$/.test(
          value
        )
      ) {
        return null
      }

      const [
        year,
        month,
        day
      ] = value
        .split('-')
        .map(Number)

      const date = new Date(
        year,
        month - 1,
        day
      )

      if (
        date.getFullYear() !== year ||
        date.getMonth() !== month - 1 ||
        date.getDate() !== day
      ) {
        return null
      }

      return date
    },

    validateForm () {
      if (
        this.isAdminOrManager &&
        !this.form.employee
      ) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please select an employee.'
        })

        return false
      }

      if (!this.form.leave_type) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please select a leave type.'
        })

        return false
      }

      if (!this.form.from_date) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please select a start date.'
        })

        return false
      }

      if (!this.form.to_date) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please select an end date.'
        })

        return false
      }

      const fromDate =
        this.parseDate(
          this.form.from_date
        )

      const toDate =
        this.parseDate(
          this.form.to_date
        )

      if (!fromDate || !toDate) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please enter valid dates.'
        })

        return false
      }

      if (toDate < fromDate) {
        this.$q.notify({
          type: 'warning',
          message:
            'To date cannot be earlier than from date.'
        })

        return false
      }

      this.calculateTotalDays()

      if (!this.form.total_days) {
        this.$q.notify({
          type: 'warning',
          message:
            'Leave duration is invalid.'
        })

        return false
      }

      return true
    },

    async saveRequest () {
      this.errorMessage = ''

      if (!this.validateForm()) {
        return
      }

      this.loading = true

      try {
        const payload = {
          leave_type:
            this.form.leave_type,

          request_date:
            this.form.request_date,

          from_date:
            this.form.from_date,

          to_date:
            this.form.to_date,

          description:
            this.form.description.trim()
        }

        if (this.isAdminOrManager) {
          payload.employee =
            this.form.employee
        }

        if (this.leaveData?.id) {
          const response =
            await api.patch(
              `/leave/requests/${this.leaveData.id}/`,
              payload
            )

          this.$q.notify({
            type: 'positive',
            message:
              'Leave request updated successfully.'
          })

          this.$emit(
            'saved',
            response.data
          )
        } else {
          const response =
            await api.post(
              '/leave/requests/',
              payload
            )

          this.$q.notify({
            type: 'positive',
            message:
              'Leave request submitted successfully.'
          })

          this.$emit(
            'saved',
            response.data
          )

          this.resetForm()
        }
      } catch (error) {
        console.error(
          'Failed to save leave request:',
          error
        )

        const message =
          this.getApiErrorMessage(
            error,
            'Failed to save leave request.'
          )

        this.errorMessage = message

        this.$q.notify({
          type: 'negative',
          message
        })
      } finally {
        this.loading = false
      }
    },

    resetForm () {
      this.form = {
        employee: null,
        leave_type: null,
        request_date: this.getToday(),
        from_date: '',
        to_date: '',
        total_days: 0,
        description: ''
      }

      this.errorMessage = ''
    },

    getApiErrorMessage (
      error,
      fallback
    ) {
      const data =
        error?.response?.data

      if (!data) {
        return fallback
      }

      if (
        typeof data.detail === 'string'
      ) {
        return data.detail
      }

      if (typeof data === 'string') {
        return data
      }

      const messages = []

      Object.entries(data).forEach(
        ([field, value]) => {
          if (Array.isArray(value)) {
            messages.push(
              `${field}: ${value.join(', ')}`
            )
          } else if (
            typeof value === 'string'
          ) {
            messages.push(
              `${field}: ${value}`
            )
          }
        }
      )

      return messages.length
        ? messages.join(' | ')
        : fallback
    }
  }
}
</script>

<style scoped>
.leave-page {
  min-height: 100%;
  background: #f7f9fc;
}

.page-icon {
  width: 50px;
  height: 50px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.leave-form-card {
  border-radius: 16px;
  background: #ffffff;
  overflow: hidden;
}

.form-header {
  padding: 19px 24px;
  background: #ffffff;
}

.duration-box {
  border: 1px solid rgba(25, 118, 210, 0.15);
  background: rgba(25, 118, 210, 0.035);
  border-radius: 13px;
  padding: 15px 17px;
}

.duration-icon {
  width: 40px;
  height: 40px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.duration-number {
  font-size: 23px;
  font-weight: 700;
  color: #1976d2;
  white-space: nowrap;
}

.duration-number span {
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
}

@media (max-width: 599px) {
  .leave-page {
    padding: 12px;
  }

  .page-icon {
    width: 44px;
    height: 44px;
  }

  .form-header {
    padding: 16px;
  }

  .duration-box {
    padding: 14px;
  }

  .duration-number {
    font-size: 20px;
  }
}
</style>
