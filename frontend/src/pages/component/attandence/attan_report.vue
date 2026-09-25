<template>
  <div class="attendance-page q-pa-md q-pa-lg-lg">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="eyebrow">WORKFORCE MANAGEMENT</div>

        <div class="page-title">
          Attendance
        </div>

        <div class="page-subtitle">
          Monitor daily attendance, working hours, and employee status.
        </div>
      </div>

      <div class="header-actions">
        <q-btn
          flat
          round
          icon="refresh"
          color="grey-7"
          :loading="loading"
          @click="loadAttendance"
        >
          <q-tooltip>Refresh</q-tooltip>
        </q-btn>

        <q-btn
          v-if="canManage"
          unelevated
          color="primary"
          icon="add"
          label="Mark Attendance"
          no-caps
          class="mark-btn"
          @click="openCreateDialog"
        />
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row q-col-gutter-md summary-row">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon total-icon">
                <q-icon name="event_note" />
              </div>

              <span class="summary-label">TOTAL</span>
            </div>

            <div class="summary-value">
              {{ summary.total }}
            </div>

            <div class="summary-title">
              Total Records
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon present-icon">
                <q-icon name="check_circle" />
              </div>

              <span class="summary-label">PRESENT</span>
            </div>

            <div class="summary-value">
              {{ summary.present }}
            </div>

            <div class="summary-title">
              Present
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon late-icon">
                <q-icon name="schedule" />
              </div>

              <span class="summary-label">LATE</span>
            </div>

            <div class="summary-value">
              {{ summary.late }}
            </div>

            <div class="summary-title">
              Late
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon absent-icon">
                <q-icon name="cancel" />
              </div>

              <span class="summary-label">ABSENT</span>
            </div>

            <div class="summary-value">
              {{ summary.absent }}
            </div>

            <div class="summary-title">
              Absent
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Employee Self Attendance -->
    <q-card
      v-if="isEmployee"
      flat
      bordered
      class="self-attendance-card"
    >
      <q-card-section class="self-attendance-section">
        <div>
          <div class="section-label">
            TODAY'S ATTENDANCE
          </div>

          <div class="self-title">
            {{ todayAttendance ? 'Attendance marked for today' : 'Mark your attendance' }}
          </div>

          <div class="self-subtitle">
            {{
              todayAttendance
                ? todayAttendance.check_in_time
                  ? `Checked in at ${formatTime(todayAttendance.check_in_time)}`
                  : 'Attendance record exists for today'
                : 'Use check-in and check-out to record your working hours.'
            }}
          </div>
        </div>

        <div class="self-actions">
          <q-btn
            v-if="!todayAttendance"
            unelevated
            color="primary"
            icon="login"
            label="Check In"
            no-caps
            :loading="checkingIn"
            @click="checkIn"
          />

          <q-btn
            v-else-if="!todayAttendance.check_out_time"
            unelevated
            color="secondary"
            icon="logout"
            label="Check Out"
            no-caps
            :loading="checkingOut"
            @click="checkOut"
          />

          <q-chip
            v-else
            color="green-1"
            text-color="green-9"
            icon="check_circle"
          >
            Completed
          </q-chip>
        </div>
      </q-card-section>
    </q-card>

    <!-- Filters -->
    <q-card flat bordered class="filter-card">
      <q-card-section class="filter-section">
        <div class="filter-header">
          <div>
            <div class="section-title">
              Attendance History
            </div>

            <div class="section-caption">
              Search and filter attendance records.
            </div>
          </div>

          <q-btn
            v-if="hasActiveFilters"
            flat
            no-caps
            color="grey-7"
            icon="clear_all"
            label="Clear"
            @click="clearFilters"
          />
        </div>

        <div class="row q-col-gutter-sm q-mt-sm">
          <div class="col-12 col-md-3">
            <q-input
              v-model="filters.search"
              outlined
              dense
              clearable
              label="Search employee"
              placeholder="Name or employee ID"
              @keyup.enter="loadAttendance"
              @clear="loadAttendance"
            >
              <template #prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-input
              v-model="filters.from_date"
              outlined
              dense
              readonly
              label="From date"
              clearable
            >
              <template #prepend>
                <q-icon name="event" />
              </template>

              <q-popup-proxy
                cover
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="filters.from_date"
                  mask="YYYY-MM-DD"
                  @update:model-value="loadAttendance"
                />
              </q-popup-proxy>
            </q-input>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-input
              v-model="filters.to_date"
              outlined
              dense
              readonly
              label="To date"
              clearable
            >
              <template #prepend>
                <q-icon name="event" />
              </template>

              <q-popup-proxy
                cover
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="filters.to_date"
                  mask="YYYY-MM-DD"
                  @update:model-value="loadAttendance"
                />
              </q-popup-proxy>
            </q-input>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-select
              v-model="filters.department"
              outlined
              dense
              clearable
              emit-value
              map-options
              label="Department"
              :options="departmentOptions"
              option-value="id"
              option-label="name"
              @update:model-value="loadAttendance"
            />
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-select
              v-model="filters.status"
              outlined
              dense
              clearable
              emit-value
              map-options
              label="Status"
              :options="statusOptions"
              @update:model-value="loadAttendance"
            />
          </div>

          <div class="col-12 col-md-1 flex items-center justify-end">
            <q-btn
              unelevated
              color="primary"
              icon="search"
              label="Apply"
              no-caps
              class="full-width apply-btn"
              :loading="loading"
              @click="loadAttendance"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Error -->
    <q-banner
      v-if="errorMessage"
      rounded
      class="error-banner q-mb-md"
      inline-actions
    >
      <template #avatar>
        <q-icon
          name="error_outline"
          color="negative"
        />
      </template>

      {{ errorMessage }}

      <template #action>
        <q-btn
          flat
          color="negative"
          label="Dismiss"
          no-caps
          @click="errorMessage = ''"
        />
      </template>
    </q-banner>

    <!-- Attendance Table -->
    <q-card flat bordered class="table-card">
      <q-table
        flat
        :rows="filteredRows"
        :columns="columns"
        row-key="id"
        :loading="loading"
        :rows-per-page-options="[10, 20, 50]"
        no-data-label="No attendance records found"
        class="attendance-table"
      >
        <template #top>
          <div class="table-top">
            <div>
              <div class="table-title">
                Records
              </div>

              <div class="table-count">
                {{ filteredRows.length }}
                {{ filteredRows.length === 1 ? 'attendance record' : 'attendance records' }}
              </div>
            </div>

            <q-btn
              flat
              round
              icon="print"
              color="grey-7"
              @click="printReport"
            >
              <q-tooltip>Print report</q-tooltip>
            </q-btn>
          </div>
        </template>

        <template #body-cell-employee="props">
          <q-td :props="props">
            <div class="employee-cell">
              <q-avatar
                size="34px"
                color="blue-1"
                text-color="primary"
              >
                <q-img
                  v-if="profileImage(props.row)"
                  :src="profileImage(props.row)"
                  fit="cover"
                />

                <span v-else>
                  {{ initials(props.row.employee_name) }}
                </span>
              </q-avatar>

              <div>
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

        <template #body-cell-department="props">
          <q-td :props="props">
            <div class="department-cell">
              <q-icon
                name="business"
                size="15px"
              />

              {{ props.row.department_name || '—' }}
            </div>
          </q-td>
        </template>

        <template #body-cell-date="props">
          <q-td :props="props">
            <span class="date-text">
              {{ formatDate(props.row.date) }}
            </span>
          </q-td>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <q-chip
              dense
              class="status-chip"
              :class="`status-${String(props.row.status || '').toLowerCase()}`"
              :icon="statusIcon(props.row.status)"
            >
              {{ statusLabel(props.row.status) }}
            </q-chip>
          </q-td>
        </template>

        <template #body-cell-check_in="props">
          <q-td :props="props">
            <div class="time-cell">
              <q-icon name="login" size="15px" />
              {{ formatTime(props.row.check_in_time) }}
            </div>
          </q-td>
        </template>

        <template #body-cell-check_out="props">
          <q-td :props="props">
            <div class="time-cell">
              <q-icon name="logout" size="15px" />
              {{ formatTime(props.row.check_out_time) }}
            </div>
          </q-td>
        </template>

        <template #body-cell-marked_by="props">
          <q-td :props="props">
            {{ props.row.marked_by_name || '—' }}
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td
            :props="props"
            class="text-right"
          >
            <q-btn
              v-if="canManage"
              flat
              round
              dense
              icon="edit"
              color="primary"
              @click="openEditDialog(props.row)"
            >
              <q-tooltip>Edit attendance</q-tooltip>
            </q-btn>

            <q-btn
              v-if="canAdmin"
              flat
              round
              dense
              icon="delete_outline"
              color="negative"
              @click="deleteAttendance(props.row)"
            >
              <q-tooltip>Delete attendance</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Mark / Edit Attendance Dialog -->
    <q-dialog
      v-model="dialogVisible"
      persistent
    >
      <q-card class="attendance-dialog">
        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-eyebrow">
              {{ isEditMode ? 'UPDATE RECORD' : 'NEW RECORD' }}
            </div>

            <div class="dialog-title">
              {{ isEditMode ? 'Edit Attendance' : 'Mark Attendance' }}
            </div>

            <div class="dialog-subtitle">
              {{
                isEditMode
                  ? 'Update the attendance details below.'
                  : 'Record employee attendance details.'
              }}
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            color="grey-7"
            :disable="saving"
            @click="closeDialog"
          />
        </q-card-section>

        <q-separator />

        <q-form @submit.prevent="saveAttendance">
          <q-card-section class="dialog-body">
            <!-- Employee -->
            <div class="field-block">
              <q-select
                v-model="form.employee"
                outlined
                dense
                emit-value
                map-options
                label="Employee *"
                :options="employeeOptions"
                option-value="id"
                option-label="label"
                :disable="isEditMode || isEmployee || saving"
                :rules="[value => !!value || 'Employee is required']"
              >
                <template #prepend>
                  <q-icon name="person_outline" />
                </template>
              </q-select>
            </div>

            <!-- Date + Status -->
            <div class="row q-col-gutter-sm">
              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.date"
                  outlined
                  dense
                  readonly
                  label="Date *"
                  :disable="saving"
                  :rules="[value => !!value || 'Date is required']"
                >
                  <template #prepend>
                    <q-icon name="event" />
                  </template>

                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date
                      v-model="form.date"
                      mask="YYYY-MM-DD"
                    />
                  </q-popup-proxy>
                </q-input>
              </div>

              <div class="col-12 col-sm-6">
                <q-select
                  v-model="form.status"
                  outlined
                  dense
                  emit-value
                  map-options
                  label="Status *"
                  :options="statusOptions"
                  :disable="saving"
                  :rules="[value => !!value || 'Status is required']"
                >
                  <template #prepend>
                    <q-icon name="fact_check" />
                  </template>
                </q-select>
              </div>
            </div>

            <!-- Times -->
            <div class="row q-col-gutter-sm">
              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.check_in_time"
                  outlined
                  dense
                  type="time"
                  label="Check-in time"
                  :disable="saving"
                >
                  <template #prepend>
                    <q-icon name="login" />
                  </template>
                </q-input>
              </div>

              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.check_out_time"
                  outlined
                  dense
                  type="time"
                  label="Check-out time"
                  :disable="saving"
                >
                  <template #prepend>
                    <q-icon name="logout" />
                  </template>
                </q-input>
              </div>
            </div>

            <!-- Notes -->
            <q-input
              v-model="form.notes"
              outlined
              dense
              type="textarea"
              autogrow
              label="Notes"
              :disable="saving"
              class="notes-field"
            />
          </q-card-section>

          <q-separator />

          <q-card-actions class="dialog-actions">
            <q-btn
              flat
              label="Cancel"
              color="grey-7"
              no-caps
              :disable="saving"
              @click="closeDialog"
            />

            <q-btn
              unelevated
              color="primary"
              :label="isEditMode ? 'Save Changes' : 'Mark Attendance'"
              no-caps
              type="submit"
              :loading="saving"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { date, Dialog, Notify } from 'quasar'
import api from 'src/services/api'

export default {
  name: 'AttendanceReport',

  data () {
    return {
      loading: false,
      saving: false,
      checkingIn: false,
      checkingOut: false,

      errorMessage: '',

      attendance: [],
      employees: [],
      departments: [],

      dialogVisible: false,
      isEditMode: false,

      form: {
        id: null,
        employee: null,
        date: date.formatDate(new Date(), 'YYYY-MM-DD'),
        status: 'PRESENT',
        check_in_time: '',
        check_out_time: '',
        notes: ''
      },

      filters: {
        search: '',
        from_date: '',
        to_date: '',
        department: null,
        status: null
      },

      statusOptions: [
        {
          label: 'Present',
          value: 'PRESENT'
        },
        {
          label: 'Absent',
          value: 'ABSENT'
        },
        {
          label: 'Late',
          value: 'LATE'
        },
        {
          label: 'On Leave',
          value: 'ON_LEAVE'
        }
      ],

      columns: [
        {
          name: 'employee',
          label: 'EMPLOYEE',
          field: 'employee_name',
          align: 'left',
          sortable: true
        },
        {
          name: 'department',
          label: 'DEPARTMENT',
          field: 'department_name',
          align: 'left',
          sortable: true
        },
        {
          name: 'date',
          label: 'DATE',
          field: 'date',
          align: 'left',
          sortable: true
        },
        {
          name: 'status',
          label: 'STATUS',
          field: 'status',
          align: 'left',
          sortable: true
        },
        {
          name: 'check_in',
          label: 'CHECK IN',
          field: 'check_in_time',
          align: 'left'
        },
        {
          name: 'check_out',
          label: 'CHECK OUT',
          field: 'check_out_time',
          align: 'left'
        },
        {
          name: 'marked_by',
          label: 'MARKED BY',
          field: 'marked_by_name',
          align: 'left'
        },
        {
          name: 'actions',
          label: '',
          field: 'actions',
          align: 'right'
        }
      ]
    }
  },

  computed: {
    currentUser () {
      return this.$store.getters.currentUser
    },

    userRole () {
      return String(this.currentUser?.role || '').toUpperCase()
    },

    isEmployee () {
      return this.userRole === 'EMPLOYEE'
    },

    canManage () {
      return this.userRole === 'ADMIN' || this.userRole === 'MANAGER'
    },

    canAdmin () {
      return this.userRole === 'ADMIN'
    },

    departmentOptions () {
      return this.departments.map(department => ({
        id: department.id,
        name: department.name
      }))
    },

    employeeOptions () {
      return this.employees.map(employee => {
        const user = employee.user || {}

        const fullName = (
          `${user.first_name || ''} ${user.last_name || ''}`
        ).trim()

        return {
          id: employee.id,
          label: `${fullName || user.username || employee.employee_id || 'Employee'} — ${employee.employee_id || employee.id}`
        }
      })
    },

    filteredRows () {
      return this.attendance
    },

    summary () {
      return {
        total: this.attendance.length,

        present: this.attendance.filter(
          item => String(item.status).toUpperCase() === 'PRESENT'
        ).length,

        late: this.attendance.filter(
          item => String(item.status).toUpperCase() === 'LATE'
        ).length,

        absent: this.attendance.filter(
          item => String(item.status).toUpperCase() === 'ABSENT'
        ).length
      }
    },

    hasActiveFilters () {
      return !!(
        this.filters.search ||
        this.filters.from_date ||
        this.filters.to_date ||
        this.filters.department ||
        this.filters.status
      )
    },

    todayAttendance () {
      const today = date.formatDate(new Date(), 'YYYY-MM-DD')

      return this.attendance.find(item => {
        return item.date === today
      }) || null
    }
  },

  mounted () {
    this.loadInitialData()
  },

  methods: {
    async loadInitialData () {
      this.loading = true
      this.errorMessage = ''

      try {
        await Promise.all([
          this.loadDepartments(),
          this.loadEmployees(),
          this.loadAttendance()
        ])
      } catch (error) {
        console.error('Failed to load attendance page:', error)

        if (!this.errorMessage) {
          this.errorMessage = this.getErrorMessage(
            error,
            'Unable to load attendance data.'
          )
        }
      } finally {
        this.loading = false
      }
    },

    async loadAttendance () {
      this.loading = true
      this.errorMessage = ''

      try {
        const params = {}

        if (this.filters.search) {
          params.search = this.filters.search
        }

        if (this.filters.from_date) {
          params.from_date = this.filters.from_date
        }

        if (this.filters.to_date) {
          params.to_date = this.filters.to_date
        }

        if (this.filters.department) {
          params.department = this.filters.department
        }

        if (this.filters.status) {
          params.status = this.filters.status
        }

        const response = await api.get('/attendance/', {
          params
        })

        this.attendance = Array.isArray(response.data)
          ? response.data
          : response.data.results || []
      } catch (error) {
        console.error('Failed to load attendance:', error)

        this.errorMessage = this.getErrorMessage(
          error,
          'Unable to load attendance records.'
        )
      } finally {
        this.loading = false
      }
    },

    async loadDepartments () {
      const response = await api.get('/departments/')

      this.departments = Array.isArray(response.data)
        ? response.data
        : response.data.results || []
    },

    async loadEmployees () {
      const response = await api.get('/employees/')

      this.employees = Array.isArray(response.data)
        ? response.data
        : response.data.results || []

      this.setEmployeeForCurrentUser()
    },

    setEmployeeForCurrentUser () {
      if (!this.isEmployee || !this.currentUser) {
        return
      }

      const employee = this.employees.find(item => {
        return Number(item.user?.id) === Number(this.currentUser.id)
      })

      if (employee) {
        this.form.employee = employee.id
      }
    },

    openCreateDialog () {
      this.isEditMode = false

      this.form = {
        id: null,
        employee: this.isEmployee ? this.form.employee : null,
        date: date.formatDate(new Date(), 'YYYY-MM-DD'),
        status: 'PRESENT',
        check_in_time: '',
        check_out_time: '',
        notes: ''
      }

      this.dialogVisible = true
    },

    openEditDialog (row) {
      this.isEditMode = true

      this.form = {
        id: row.id,
        employee: row.employee,
        date: row.date,
        status: row.status,
        check_in_time: row.check_in_time || '',
        check_out_time: row.check_out_time || '',
        notes: row.notes || ''
      }

      this.dialogVisible = true
    },

    closeDialog () {
      if (this.saving) {
        return
      }

      this.dialogVisible = false
    },

    async saveAttendance () {
      if (!this.form.employee) {
        Notify.create({
          type: 'negative',
          message: 'Please select an employee.'
        })

        return
      }

      this.saving = true
      this.errorMessage = ''

      try {
        const payload = {
          employee: this.form.employee,
          date: this.form.date,
          status: this.form.status,
          check_in_time: this.form.check_in_time || null,
          check_out_time: this.form.check_out_time || null,
          notes: this.form.notes || ''
        }

        if (this.isEditMode) {
          await api.patch(
            `/attendance/${this.form.id}/`,
            payload
          )

          Notify.create({
            type: 'positive',
            message: 'Attendance updated successfully.'
          })
        } else {
          await api.post(
            '/attendance/',
            payload
          )

          Notify.create({
            type: 'positive',
            message: 'Attendance marked successfully.'
          })
        }

        this.dialogVisible = false

        await this.loadAttendance()
      } catch (error) {
        console.error('Failed to save attendance:', error)

        const message = this.getErrorMessage(
          error,
          'Unable to save attendance.'
        )

        this.errorMessage = message

        Notify.create({
          type: 'negative',
          message
        })
      } finally {
        this.saving = false
      }
    },

    deleteAttendance (row) {
      Dialog.create({
        title: 'Delete Attendance',
        message: `Delete attendance record for ${row.employee_name || 'this employee'}?`,
        cancel: true,
        persistent: true,
        ok: {
          label: 'Delete',
          color: 'negative',
          unelevated: true,
          noCaps: true
        },
        cancel: {
          label: 'Cancel',
          flat: true,
          noCaps: true
        }
      }).onOk(async () => {
        try {
          await api.delete(`/attendance/${row.id}/`)

          Notify.create({
            type: 'positive',
            message: 'Attendance record deleted.'
          })

          await this.loadAttendance()
        } catch (error) {
          console.error('Failed to delete attendance:', error)

          Notify.create({
            type: 'negative',
            message: this.getErrorMessage(
              error,
              'Unable to delete attendance record.'
            )
          })
        }
      })
    },

    async checkIn () {
      this.checkingIn = true

      try {
        await api.post('/attendance/check-in/')

        Notify.create({
          type: 'positive',
          message: 'Check-in recorded successfully.'
        })

        await this.loadAttendance()
      } catch (error) {
        Notify.create({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Unable to check in.'
          )
        })
      } finally {
        this.checkingIn = false
      }
    },

    async checkOut () {
      this.checkingOut = true

      try {
        await api.put('/attendance/check-out/')

        Notify.create({
          type: 'positive',
          message: 'Check-out recorded successfully.'
        })

        await this.loadAttendance()
      } catch (error) {
        Notify.create({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Unable to check out.'
          )
        })
      } finally {
        this.checkingOut = false
      }
    },

    clearFilters () {
      this.filters = {
        search: '',
        from_date: '',
        to_date: '',
        department: null,
        status: null
      }

      this.loadAttendance()
    },

    statusLabel (status) {
      const value = String(status || '').toUpperCase()

      const labels = {
        PRESENT: 'Present',
        ABSENT: 'Absent',
        LATE: 'Late',
        ON_LEAVE: 'On Leave'
      }

      return labels[value] || status || 'Unknown'
    },

    statusIcon (status) {
      const value = String(status || '').toUpperCase()

      const icons = {
        PRESENT: 'check_circle',
        ABSENT: 'cancel',
        LATE: 'schedule',
        ON_LEAVE: 'event_busy'
      }

      return icons[value] || 'help_outline'
    },

    formatDate (value) {
      if (!value) {
        return '—'
      }

      return date.formatDate(
        value,
        'DD MMM YYYY'
      )
    },

    formatTime (value) {
      if (!value) {
        return '—'
      }

      const parts = String(value).split(':')

      if (parts.length < 2) {
        return value
      }

      const hours = Number(parts[0])
      const minutes = parts[1]

      const suffix = hours >= 12 ? 'PM' : 'AM'
      const displayHour = hours % 12 || 12

      return `${displayHour}:${minutes} ${suffix}`
    },

    initials (name) {
      if (!name) {
        return '—'
      }

      const parts = String(name)
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (parts.length === 1) {
        return parts[0].slice(0, 2).toUpperCase()
      }

      return (
        parts[0][0] +
        parts[parts.length - 1][0]
      ).toUpperCase()
    },

    profileImage (row) {
      const employee = this.employees.find(
        item => Number(item.id) === Number(row.employee)
      )

      const image =
        employee?.profile_picture ||
        employee?.user?.profile_picture ||
        ''

      if (!image) {
        return ''
      }

      if (String(image).startsWith('http')) {
        return image
      }

      return `http://127.0.0.1:8000${image.startsWith('/') ? '' : '/'}${image}`
    },

    printReport () {
      window.print()
    },

    getErrorMessage (error, fallback) {
      const data = error?.response?.data

      if (!data) {
        return fallback
      }

      if (typeof data.detail === 'string') {
        return data.detail
      }

      if (typeof data === 'string') {
        return data
      }

      const firstKey = Object.keys(data)[0]

      if (firstKey && Array.isArray(data[firstKey])) {
        return data[firstKey][0]
      }

      if (firstKey && typeof data[firstKey] === 'string') {
        return data[firstKey]
      }

      return fallback
    }
  }
}
</script>

<style scoped>
.attendance-page {
  min-height: 100%;
  background: transparent;
}

/* Header */

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.eyebrow {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: var(--q-primary);
  margin-bottom: 4px;
}

.page-title {
  font-size: 28px;
  line-height: 1.15;
  font-weight: 700;
  color: #1f2937;
}

.page-subtitle {
  margin-top: 5px;
  font-size: 13px;
  color: #7b8491;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.mark-btn {
  min-height: 38px;
  padding: 0 16px;
  border-radius: 8px;
}

/* Summary */

.summary-row {
  margin-bottom: 16px;
}

.summary-card {
  min-height: 112px;
  border-radius: 12px;
  background: #ffffff;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.summary-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 18px rgba(31, 41, 55, 0.07);
}

.summary-card .q-card__section {
  padding: 13px 15px;
}

.summary-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.summary-icon {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 19px;
}

.total-icon {
  background: #eef4ff;
  color: #3975d5;
}

.present-icon {
  background: #eaf8ef;
  color: #21874c;
}

.late-icon {
  background: #fff5e6;
  color: #d48716;
}

.absent-icon {
  background: #fff0f0;
  color: #d33a3a;
}

.summary-label {
  font-size: 9px;
  font-weight: 700;
  color: #8a929d;
  letter-spacing: 0.5px;
}

.summary-value {
  margin-top: 8px;
  font-size: 24px;
  line-height: 1;
  font-weight: 700;
  color: #202833;
}

.summary-title {
  margin-top: 4px;
  font-size: 12px;
  color: #747d89;
}

/* Self attendance */

.self-attendance-card {
  border-radius: 12px;
  margin-bottom: 16px;
}

.self-attendance-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 15px 18px;
}

.section-label {
  font-size: 9px;
  font-weight: 700;
  color: var(--q-primary);
  letter-spacing: 0.7px;
}

.self-title {
  margin-top: 3px;
  font-size: 15px;
  font-weight: 600;
  color: #26303b;
}

.self-subtitle {
  margin-top: 3px;
  font-size: 12px;
  color: #7d8792;
}

.self-actions {
  flex-shrink: 0;
}

/* Filters */

.filter-card {
  border-radius: 12px;
  margin-bottom: 16px;
}

.filter-section {
  padding: 13px 15px 15px;
}

.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.section-title {
  font-size: 14px;
  font-weight: 650;
  color: #28323d;
}

.section-caption {
  margin-top: 2px;
  font-size: 11px;
  color: #8a929c;
}

.apply-btn {
  min-height: 40px;
  border-radius: 7px;
}

/* Table */

.table-card {
  border-radius: 12px;
  overflow: hidden;
}

.table-top {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1px 0;
}

.table-title {
  font-size: 14px;
  font-weight: 650;
  color: #28323d;
}

.table-count {
  margin-top: 2px;
  font-size: 11px;
  color: #89919c;
}

.attendance-table :deep(.q-table__top) {
  padding: 12px 15px;
}

.attendance-table :deep(thead tr) {
  background: #fafbfc;
}

.attendance-table :deep(th) {
  height: 38px;
  padding: 7px 12px;
  font-size: 10px;
  font-weight: 700;
  color: #697482;
  letter-spacing: 0.25px;
}

.attendance-table :deep(td) {
  height: 56px;
  padding: 7px 12px;
  font-size: 12px;
  color: #404a56;
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.employee-name {
  font-size: 12px;
  font-weight: 600;
  color: #2d3742;
}

.employee-id {
  margin-top: 2px;
  font-size: 10px;
  color: #8a939e;
}

.department-cell {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #596472;
}

.date-text {
  font-weight: 550;
  color: #3e4854;
}

.status-chip {
  min-width: 68px;
  justify-content: center;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 600;
}

.status-present {
  background: #eaf8ef;
  color: #23814a;
}

.status-absent {
  background: #fff0f0;
  color: #c93636;
}

.status-late {
  background: #fff5e6;
  color: #c47a12;
}

.status-on_leave {
  background: #f0edff;
  color: #6957b8;
}

.time-cell {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #596472;
  white-space: nowrap;
}

/* Dialog */

.attendance-dialog {
  width: 680px;
  max-width: calc(100vw - 32px);
  max-height: 90vh;
  border-radius: 14px;
  overflow: hidden;
  background: #ffffff;
}

.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 15px;
  padding: 17px 20px 15px;
}

.dialog-eyebrow {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.7px;
  color: var(--q-primary);
}

.dialog-title {
  margin-top: 3px;
  font-size: 19px;
  line-height: 1.2;
  font-weight: 700;
  color: #202a35;
}

.dialog-subtitle {
  margin-top: 4px;
  font-size: 11px;
  color: #8a929c;
}

.dialog-body {
  max-height: calc(90vh - 150px);
  overflow-y: auto;
  padding: 16px 20px 18px;
}

.field-block {
  margin-bottom: 12px;
}

.notes-field {
  margin-top: 12px;
}

.dialog-actions {
  justify-content: flex-end;
  gap: 4px;
  padding: 11px 20px;
}

.dialog-actions .q-btn {
  min-height: 36px;
  border-radius: 7px;
}

/* Error */

.error-banner {
  background: #fff3f3;
  color: #b52d2d;
}

/* Dark mode */

.body--dark .page-title,
.body--dark .summary-value,
.body--dark .section-title,
.body--dark .self-title,
.body--dark .table-title,
.body--dark .dialog-title,
.body--dark .employee-name {
  color: #f1f4f7;
}

.body--dark .page-subtitle,
.body--dark .summary-title,
.body--dark .section-caption,
.body--dark .self-subtitle,
.body--dark .table-count,
.body--dark .employee-id,
.body--dark .department-cell,
.body--dark .time-cell {
  color: #9ca6b2;
}

.body--dark .summary-card,
.body--dark .filter-card,
.body--dark .table-card,
.body--dark .self-attendance-card,
.body--dark .attendance-dialog {
  background: #1c222a;
  border-color: #303843;
}

.body--dark .summary-card :deep(.q-card__section) {
  background: #1c222a;
}

.body--dark .attendance-table :deep(thead tr) {
  background: #202730;
}

.body--dark .attendance-table :deep(th) {
  color: #aab3bf;
}

.body--dark .attendance-table :deep(td) {
  color: #c3cad3;
}

.body--dark .dialog-header,
.body--dark .dialog-body,
.body--dark .dialog-actions {
  background: #1c222a;
}

.body--dark .error-banner {
  background: #3a2022;
  color: #ffb5b5;
}

/* Responsive */

@media (max-width: 767px) {
  .attendance-page {
    padding: 12px !important;
  }

  .page-header {
    align-items: flex-start;
  }

  .page-title {
    font-size: 24px;
  }

  .page-subtitle {
    max-width: 270px;
  }

  .header-actions {
    margin-top: 2px;
  }

  .mark-btn {
    padding: 0 11px;
  }

  .self-attendance-section {
    align-items: flex-start;
    flex-direction: column;
  }

  .self-actions {
    width: 100%;
  }

  .self-actions .q-btn {
    width: 100%;
  }

  .filter-section {
    padding: 12px;
  }

  .filter-header {
    align-items: flex-start;
  }

  .apply-btn {
    margin-top: 2px;
  }

  .attendance-dialog {
    max-width: calc(100vw - 20px);
  }

  .dialog-header {
    padding: 14px 15px 13px;
  }

  .dialog-body {
    padding: 14px 15px 16px;
  }

  .dialog-actions {
    padding: 10px 15px;
  }
}

@media print {
  .page-header .header-actions,
  .self-attendance-card,
  .filter-card,
  .table-top .q-btn,
  .attendance-table :deep(th:last-child),
  .attendance-table :deep(td:last-child) {
    display: none !important;
  }

  .attendance-page {
    padding: 0 !important;
  }

  .summary-card,
  .table-card {
    box-shadow: none !important;
  }
}
</style>
