<template>
  <div class="attendance-page q-pa-md q-pa-lg-lg">
    <!-- Page Header -->
    <div class="page-header q-mb-lg">
      <div>
        <div class="text-overline text-primary text-weight-bold">
          OFFICE MANAGEMENT
        </div>

        <h1 class="page-title q-my-none">
          Attendance
        </h1>

        <p class="page-subtitle q-mt-sm q-mb-none">
          Monitor attendance, working hours, and daily check-in activity.
        </p>
      </div>

      <div class="header-actions">
        <q-btn
          flat
          round
          icon="refresh"
          :loading="loading"
          @click="fetchAttendance"
        >
          <q-tooltip>Refresh attendance</q-tooltip>
        </q-btn>

        <q-btn
          outline
          color="primary"
          icon="print"
          label="Print"
          class="q-ml-sm"
          @click="printAttendance"
        />
      </div>
    </div>

    <!-- Error -->
    <q-banner
      v-if="errorMessage"
      rounded
      class="bg-red-1 text-negative q-mb-lg"
    >
      <template #avatar>
        <q-icon name="error_outline" />
      </template>

      {{ errorMessage }}

      <template #action>
        <q-btn
          flat
          color="negative"
          label="Retry"
          @click="fetchAttendance"
        />
      </template>
    </q-banner>

    <!-- Summary Cards -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon icon-primary">
                <q-icon name="event_available" size="22px" />
              </div>

              <q-icon
                name="trending_up"
                size="18px"
                class="text-positive"
              />
            </div>

            <div class="summary-value">
              {{ summary.total }}
            </div>

            <div class="summary-label">
              Total Records
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon icon-positive">
                <q-icon name="check_circle" size="22px" />
              </div>

              <span class="summary-percent text-positive">
                {{ summary.presentPercentage }}%
              </span>
            </div>

            <div class="summary-value">
              {{ summary.present }}
            </div>

            <div class="summary-label">
              Present
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon icon-warning">
                <q-icon name="schedule" size="22px" />
              </div>

              <span class="summary-percent text-warning">
                {{ summary.latePercentage }}%
              </span>
            </div>

            <div class="summary-value">
              {{ summary.late }}
            </div>

            <div class="summary-label">
              Late
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="summary-card">
          <q-card-section>
            <div class="summary-top">
              <div class="summary-icon icon-negative">
                <q-icon name="event_busy" size="22px" />
              </div>

              <span class="summary-percent text-negative">
                {{ summary.absentOrLeavePercentage }}%
              </span>
            </div>

            <div class="summary-value">
              {{ summary.absentOrLeave }}
            </div>

            <div class="summary-label">
              Absent / Leave
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Today Action Card -->
    <q-card class="today-card q-mb-lg">
      <q-card-section class="q-pa-md q-pa-lg-lg">
        <div class="row items-center q-col-gutter-lg">
          <div class="col-12 col-md">
            <div class="row items-center no-wrap">
              <div class="today-icon">
                <q-icon name="today" size="25px" />
              </div>

              <div class="q-ml-md">
                <div class="text-subtitle1 text-weight-bold">
                  Today's Attendance
                </div>

                <div class="text-caption text-grey-6">
                  {{ todayLabel }}
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-auto">
            <div class="today-status q-mb-sm q-mb-md-none">
              <span class="status-dot" :class="todayStatusClass"></span>

              <span class="text-body2 text-weight-medium">
                {{ todayStatusText }}
              </span>

              <span
                v-if="todayAttendance?.check_in_time"
                class="text-caption text-grey-6 q-ml-sm"
              >
                In {{ formatTime(todayAttendance.check_in_time) }}
              </span>

              <span
                v-if="todayAttendance?.check_out_time"
                class="text-caption text-grey-6 q-ml-sm"
              >
                · Out {{ formatTime(todayAttendance.check_out_time) }}
              </span>
            </div>

            <div class="row q-gutter-sm">
              <q-btn
                v-if="canCheckIn"
                unelevated
                color="primary"
                icon="login"
                label="Check In"
                :loading="checkInLoading"
                @click="checkIn"
              />

              <q-btn
                v-if="canCheckOut"
                unelevated
                color="dark"
                icon="logout"
                label="Check Out"
                :loading="checkOutLoading"
                @click="checkOut"
              />

              <q-chip
                v-if="!canCheckIn && !canCheckOut && todayAttendance"
                dense
                color="positive"
                text-color="white"
                icon="task_alt"
              >
                Attendance completed
              </q-chip>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Filters -->
    <q-card class="filter-card q-mb-lg">
      <q-card-section>
        <div class="row items-center q-mb-md">
          <div>
            <div class="text-subtitle1 text-weight-bold">
              Attendance Records
            </div>

            <div class="text-caption text-grey-6">
              Search and filter attendance records.
            </div>
          </div>

          <q-space />

          <q-btn
            v-if="hasFilters"
            flat
            dense
            color="primary"
            icon="filter_alt_off"
            label="Clear filters"
            @click="clearFilters"
          />
        </div>

        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-4">
            <q-input
              v-model="filters.search"
              outlined
              dense
              clearable
              label="Search employee"
              placeholder="Name, username or employee ID"
              @keyup.enter="applyFilters"
            >
              <template #prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-select
              v-model="filters.month"
              outlined
              dense
              clearable
              emit-value
              map-options
              label="Month"
              :options="monthOptions"
            />
          </div>

          <div class="col-12 col-sm-6 col-md-2">
            <q-input
              v-model="filters.year"
              outlined
              dense
              clearable
              type="number"
              label="Year"
              min="2000"
              max="2100"
            >
              <template #prepend>
                <q-icon name="calendar_today" />
              </template>
            </q-input>
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
            />
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
              :loading="departmentsLoading"
            />
          </div>
        </div>

        <div class="row justify-end q-mt-md">
          <q-btn
            unelevated
            color="primary"
            icon="filter_alt"
            label="Apply Filters"
            :loading="loading"
            @click="applyFilters"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Loading -->
    <q-card
      v-if="loading && !rows.length"
      class="table-card"
    >
      <q-card-section class="q-pa-xl text-center">
        <q-spinner-dots
          color="primary"
          size="40px"
        />

        <div class="text-body2 text-grey-6 q-mt-md">
          Loading attendance records...
        </div>
      </q-card-section>
    </q-card>

    <!-- Empty -->
    <q-card
      v-else-if="!loading && !filteredRows.length"
      class="table-card"
    >
      <q-card-section class="empty-state q-pa-xl">
        <div class="empty-icon">
          <q-icon name="event_busy" size="42px" />
        </div>

        <div class="text-h6 text-weight-bold q-mt-md">
          No attendance records found
        </div>

        <div class="text-body2 text-grey-6 q-mt-sm">
          Try changing your filters or refresh the attendance records.
        </div>

        <q-btn
          flat
          color="primary"
          label="Clear Filters"
          class="q-mt-md"
          @click="clearFilters"
        />
      </q-card-section>
    </q-card>

    <!-- Attendance Table -->
    <q-card
      v-else
      class="table-card"
    >
      <q-table
        :rows="filteredRows"
        :columns="columns"
        row-key="id"
        flat
        :loading="loading"
        :pagination="pagination"
        :rows-per-page-options="[10, 20, 50, 0]"
        no-data-label="No attendance records found"
        class="attendance-table"
      >
        <template #loading>
          <q-inner-loading showing color="primary" />
        </template>

        <template #body-cell-employee="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-avatar
                size="38px"
                class="employee-avatar"
              >
                {{ getInitials(props.row.employee_name) }}
              </q-avatar>

              <div class="q-ml-sm">
                <div class="text-body2 text-weight-bold">
                  {{ props.row.employee_name || 'Unknown Employee' }}
                </div>

                <div class="text-caption text-grey-6">
                  {{ props.row.employee_id || '—' }}
                </div>
              </div>
            </div>
          </q-td>
        </template>

        <template #body-cell-date="props">
          <q-td :props="props">
            <div class="text-body2 text-weight-medium">
              {{ formatDate(props.row.date) }}
            </div>

            <div class="text-caption text-grey-6">
              {{ getDayName(props.row.date) }}
            </div>
          </q-td>
        </template>

        <template #body-cell-check_in_time="props">
          <q-td :props="props">
            <span
              v-if="props.row.check_in_time"
              class="time-value"
            >
              <q-icon
                name="login"
                size="16px"
                class="q-mr-xs text-positive"
              />
              {{ formatTime(props.row.check_in_time) }}
            </span>

            <span
              v-else
              class="text-grey-5"
            >
              —
            </span>
          </q-td>
        </template>

        <template #body-cell-check_out_time="props">
          <q-td :props="props">
            <span
              v-if="props.row.check_out_time"
              class="time-value"
            >
              <q-icon
                name="logout"
                size="16px"
                class="q-mr-xs text-grey-7"
              />
              {{ formatTime(props.row.check_out_time) }}
            </span>

            <span
              v-else
              class="text-grey-5"
            >
              —
            </span>
          </q-td>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <q-badge
              rounded
              :color="statusColor(props.row.status)"
              :text-color="statusTextColor(props.row.status)"
              class="status-badge"
            >
              <q-icon
                :name="statusIcon(props.row.status)"
                size="14px"
                class="q-mr-xs"
              />

              {{ formatStatus(props.row.status) }}
            </q-badge>
          </q-td>
        </template>

        <template #body-cell-notes="props">
          <q-td :props="props">
            <span
              v-if="props.row.notes"
              class="notes-text"
            >
              {{ props.row.notes }}
              <q-tooltip>
                {{ props.row.notes }}
              </q-tooltip>
            </span>

            <span
              v-else
              class="text-grey-5"
            >
              —
            </span>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { computed, onMounted, reactive, ref } from 'vue'
import { Notify } from 'quasar'

import api from 'src/services/api'

export default {
  name: 'AttendanceReport',

  setup () {
    const rows = ref([])
    const loading = ref(false)
    const departmentsLoading = ref(false)
    const checkInLoading = ref(false)
    const checkOutLoading = ref(false)
    const errorMessage = ref('')

    const departments = ref([])

    const filters = reactive({
      search: '',
      month: null,
      year: '',
      status: null,
      department: null
    })

    const pagination = ref({
      sortBy: 'date',
      descending: true,
      page: 1,
      rowsPerPage: 10
    })

    const columns = [
      {
        name: 'employee',
        label: 'Employee',
        align: 'left',
        field: 'employee_name',
        sortable: true
      },
      {
        name: 'department_name',
        label: 'Department',
        align: 'left',
        field: 'department_name',
        sortable: true
      },
      {
        name: 'date',
        label: 'Date',
        align: 'left',
        field: 'date',
        sortable: true
      },
      {
        name: 'check_in_time',
        label: 'Check In',
        align: 'left',
        field: 'check_in_time',
        sortable: true
      },
      {
        name: 'check_out_time',
        label: 'Check Out',
        align: 'left',
        field: 'check_out_time',
        sortable: true
      },
      {
        name: 'status',
        label: 'Status',
        align: 'left',
        field: 'status',
        sortable: true
      },
      {
        name: 'notes',
        label: 'Notes',
        align: 'left',
        field: 'notes'
      }
    ]

    const monthOptions = [
      { label: 'January', value: '01' },
      { label: 'February', value: '02' },
      { label: 'March', value: '03' },
      { label: 'April', value: '04' },
      { label: 'May', value: '05' },
      { label: 'June', value: '06' },
      { label: 'July', value: '07' },
      { label: 'August', value: '08' },
      { label: 'September', value: '09' },
      { label: 'October', value: '10' },
      { label: 'November', value: '11' },
      { label: 'December', value: '12' }
    ]

    const statusOptions = [
      { label: 'Present', value: 'PRESENT' },
      { label: 'Absent', value: 'ABSENT' },
      { label: 'Late', value: 'LATE' },
      { label: 'On Leave', value: 'ON_LEAVE' }
    ]

    const departmentOptions = computed(() => {
      return departments.value.map(department => ({
        label: department.name,
        value: department.id
      }))
    })

    const filteredRows = computed(() => {
      return rows.value.filter(row => {
        const searchValue = filters.search.trim().toLowerCase()

        const matchesSearch = !searchValue ||
          String(row.employee_name || '').toLowerCase().includes(searchValue) ||
          String(row.employee_id || '').toLowerCase().includes(searchValue)

        const matchesStatus =
          !filters.status ||
          row.status === filters.status

        const matchesDepartment =
          !filters.department ||
          String(row.department_id || '') === String(filters.department)

        const matchesMonth =
          !filters.month ||
          String(row.date || '').slice(5, 7) === String(filters.month)

        const matchesYear =
          !filters.year ||
          String(row.date || '').slice(0, 4) === String(filters.year)

        return (
          matchesSearch &&
          matchesStatus &&
          matchesDepartment &&
          matchesMonth &&
          matchesYear
        )
      })
    })

    const summary = computed(() => {
      const records = filteredRows.value

      const total = records.length
      const present = records.filter(
        row => row.status === 'PRESENT'
      ).length

      const late = records.filter(
        row => row.status === 'LATE'
      ).length

      const absentOrLeave = records.filter(
        row =>
          row.status === 'ABSENT' ||
          row.status === 'ON_LEAVE'
      ).length

      return {
        total,
        present,
        late,
        absentOrLeave,
        presentPercentage: total
          ? Math.round((present / total) * 100)
          : 0,
        latePercentage: total
          ? Math.round((late / total) * 100)
          : 0,
        absentOrLeavePercentage: total
          ? Math.round((absentOrLeave / total) * 100)
          : 0
      }
    })

    const todayAttendance = computed(() => {
      const today = getLocalDateString()

      return rows.value.find(
        row => row.date === today
      ) || null
    })

    const canCheckIn = computed(() => {
      if (!todayAttendance.value) {
        return true
      }

      return !todayAttendance.value.check_in_time
    })

    const canCheckOut = computed(() => {
      if (!todayAttendance.value) {
        return false
      }

      return Boolean(todayAttendance.value.check_in_time) &&
        !todayAttendance.value.check_out_time
    })

    const todayStatusText = computed(() => {
      if (!todayAttendance.value) {
        return 'Not checked in'
      }

      if (todayAttendance.value.check_out_time) {
        return 'Checked out'
      }

      if (todayAttendance.value.check_in_time) {
        return 'Checked in'
      }

      return 'Not checked in'
    })

    const todayStatusClass = computed(() => {
      if (todayAttendance.value?.check_out_time) {
        return 'status-complete'
      }

      if (todayAttendance.value?.check_in_time) {
        return 'status-active'
      }

      return 'status-idle'
    })

    const todayLabel = computed(() => {
      return new Intl.DateTimeFormat('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      }).format(new Date())
    })

    const hasFilters = computed(() => {
      return Boolean(
        filters.search ||
        filters.month ||
        filters.year ||
        filters.status ||
        filters.department
      )
    })

    function getLocalDateString () {
      const now = new Date()

      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')

      return `${year}-${month}-${day}`
    }

    function formatDate (date) {
      if (!date) {
        return '—'
      }

      const parts = String(date).split('-')

      if (parts.length !== 3) {
        return date
      }

      const [year, month, day] = parts

      return `${day}/${month}/${year}`
    }

    function getDayName (date) {
      if (!date) {
        return ''
      }

      const parsedDate = new Date(`${date}T00:00:00`)

      if (Number.isNaN(parsedDate.getTime())) {
        return ''
      }

      return new Intl.DateTimeFormat('en-US', {
        weekday: 'long'
      }).format(parsedDate)
    }

    function formatTime (time) {
      if (!time) {
        return '—'
      }

      const parts = String(time).split(':')

      if (parts.length < 2) {
        return time
      }

      let hour = Number(parts[0])
      const minute = parts[1]

      if (Number.isNaN(hour)) {
        return time
      }

      const suffix = hour >= 12 ? 'PM' : 'AM'

      hour = hour % 12 || 12

      return `${String(hour).padStart(2, '0')}:${minute} ${suffix}`
    }

    function formatStatus (status) {
      const labels = {
        PRESENT: 'Present',
        ABSENT: 'Absent',
        LATE: 'Late',
        ON_LEAVE: 'On Leave'
      }

      return labels[status] || status || 'Unknown'
    }

    function statusColor (status) {
      const colors = {
        PRESENT: 'green-1',
        ABSENT: 'red-1',
        LATE: 'orange-1',
        ON_LEAVE: 'blue-1'
      }

      return colors[status] || 'grey-2'
    }

    function statusTextColor (status) {
      const colors = {
        PRESENT: 'positive',
        ABSENT: 'negative',
        LATE: 'warning',
        ON_LEAVE: 'primary'
      }

      return colors[status] || 'grey-8'
    }

    function statusIcon (status) {
      const icons = {
        PRESENT: 'check_circle',
        ABSENT: 'cancel',
        LATE: 'schedule',
        ON_LEAVE: 'event_busy'
      }

      return icons[status] || 'help_outline'
    }

    function getInitials (name) {
      if (!name) {
        return 'U'
      }

      const parts = String(name)
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (!parts.length) {
        return 'U'
      }

      if (parts.length === 1) {
        return parts[0].slice(0, 2).toUpperCase()
      }

      return (
        parts[0].charAt(0) +
        parts[parts.length - 1].charAt(0)
      ).toUpperCase()
    }

    function extractList (responseData) {
      if (Array.isArray(responseData)) {
        return responseData
      }

      if (Array.isArray(responseData?.results)) {
        return responseData.results
      }

      return []
    }

    async function fetchAttendance () {
      loading.value = true
      errorMessage.value = ''

      try {
        const response = await api.get('/attendance/')
        rows.value = extractList(response.data)
      } catch (error) {
        console.error('Error fetching attendance:', error)

        errorMessage.value =
          error.response?.data?.detail ||
          'Unable to load attendance records. Please try again.'
      } finally {
        loading.value = false
      }
    }

    async function fetchDepartments () {
      departmentsLoading.value = true

      try {
        const response = await api.get('/departments/')
        departments.value = extractList(response.data)
      } catch (error) {
        console.error('Error fetching departments:', error)
        departments.value = []
      } finally {
        departmentsLoading.value = false
      }
    }

    function applyFilters () {
      pagination.value.page = 1
    }

    function clearFilters () {
      filters.search = ''
      filters.month = null
      filters.year = ''
      filters.status = null
      filters.department = null

      pagination.value.page = 1
    }

    async function checkIn () {
      checkInLoading.value = true

      try {
        const response = await api.post('/attendance/check-in/')

        Notify.create({
          type: 'positive',
          message: 'You have successfully checked in.',
          icon: 'login'
        })

        const updatedAttendance = response.data

        const existingIndex = rows.value.findIndex(
          row => row.id === updatedAttendance.id
        )

        if (existingIndex >= 0) {
          rows.value[existingIndex] = updatedAttendance
        } else {
          rows.value.unshift(updatedAttendance)
        }
      } catch (error) {
        console.error('Check-in error:', error)

        Notify.create({
          type: 'negative',
          message:
            error.response?.data?.detail ||
            'Unable to check in. Please try again.',
          icon: 'error_outline'
        })
      } finally {
        checkInLoading.value = false
      }
    }

    async function checkOut () {
      checkOutLoading.value = true

      try {
        const response = await api.post('/attendance/check-out/')

        Notify.create({
          type: 'positive',
          message: 'You have successfully checked out.',
          icon: 'logout'
        })

        const updatedAttendance = response.data

        const existingIndex = rows.value.findIndex(
          row => row.id === updatedAttendance.id
        )

        if (existingIndex >= 0) {
          rows.value[existingIndex] = updatedAttendance
        } else {
          rows.value.unshift(updatedAttendance)
        }
      } catch (error) {
        console.error('Check-out error:', error)

        Notify.create({
          type: 'negative',
          message:
            error.response?.data?.detail ||
            'Unable to check out. Please try again.',
          icon: 'error_outline'
        })
      } finally {
        checkOutLoading.value = false
      }
    }

    function printAttendance () {
      window.print()
    }

    onMounted(() => {
      fetchAttendance()
      fetchDepartments()
    })

    return {
      rows,
      loading,
      departmentsLoading,
      checkInLoading,
      checkOutLoading,
      errorMessage,
      filters,
      pagination,
      columns,
      monthOptions,
      statusOptions,
      departmentOptions,
      filteredRows,
      summary,
      todayAttendance,
      canCheckIn,
      canCheckOut,
      todayStatusText,
      todayStatusClass,
      todayLabel,
      hasFilters,
      fetchAttendance,
      applyFilters,
      clearFilters,
      checkIn,
      checkOut,
      printAttendance,
      formatDate,
      getDayName,
      formatTime,
      formatStatus,
      statusColor,
      statusTextColor,
      statusIcon,
      getInitials
    }
  }
}
</script>

<style scoped>
.attendance-page {
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.page-title {
  font-size: 30px;
  line-height: 1.2;
  font-weight: 750;
  letter-spacing: -0.5px;
}

.page-subtitle {
  color: #6b7280;
  font-size: 14px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.summary-card {
  border: 1px solid rgba(0, 0, 0, 0.07);
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
  height: 100%;
}

.summary-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.summary-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-primary {
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.icon-positive {
  background: rgba(33, 150, 83, 0.1);
  color: #219653;
}

.icon-warning {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
}

.icon-negative {
  background: rgba(211, 47, 47, 0.1);
  color: #d32f2f;
}

.summary-value {
  margin-top: 18px;
  font-size: 28px;
  line-height: 1;
  font-weight: 750;
  color: #1f2937;
}

.summary-label {
  margin-top: 7px;
  font-size: 13px;
  color: #6b7280;
}

.summary-percent {
  font-size: 12px;
  font-weight: 700;
}

.today-card {
  border-radius: 16px;
  border: 1px solid rgba(25, 118, 210, 0.12);
  box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
}

.today-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.today-status {
  display: flex;
  align-items: center;
}

.status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  margin-right: 8px;
}

.status-active {
  background: #21ba45;
}

.status-complete {
  background: #1976d2;
}

.status-idle {
  background: #9e9e9e;
}

.filter-card,
.table-card {
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.07);
  box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
}

.attendance-table :deep(thead tr) {
  background: rgba(15, 23, 42, 0.025);
}

.attendance-table :deep(th) {
  font-weight: 700;
  color: #4b5563;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.attendance-table :deep(td) {
  height: 66px;
}

.employee-avatar {
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
  font-size: 13px;
  font-weight: 700;
}

.time-value {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
}

.status-badge {
  padding: 6px 9px;
  font-weight: 700;
  font-size: 11px;
}

.notes-text {
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-state {
  text-align: center;
}

.empty-icon {
  width: 78px;
  height: 78px;
  margin: 0 auto;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.08);
  color: #1976d2;
}

@media (max-width: 700px) {
  .attendance-page {
    padding: 12px !important;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .page-title {
    font-size: 26px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .today-status {
    align-items: flex-start;
    flex-wrap: wrap;
  }
}

@media print {
  .page-header,
  .today-card,
  .filter-card,
  .q-banner {
    display: none !important;
  }

  .attendance-page {
    padding: 0 !important;
    max-width: none;
  }

  .table-card {
    border: none;
    box-shadow: none;
  }
}
</style>
