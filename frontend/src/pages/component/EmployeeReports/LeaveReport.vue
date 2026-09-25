<template>
  <div class="leave-report-page">
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <q-icon name="event_note" size="28px" />
        </div>

        <div>
          <div class="page-title">Leave Reports</div>
          <div class="page-subtitle">
            {{ isManagement
              ? 'Review employee leave requests, statuses, and history.'
              : 'Review your leave history, status, and request details.' }}
          </div>
        </div>
      </div>

      <q-btn
        outline
        color="primary"
        icon="refresh"
        label="Refresh"
        no-caps
        :loading="loading"
        @click="loadReport"
      />
    </div>

    <q-banner
      v-if="errorMessage"
      class="error-banner"
      rounded
      inline-actions
    >
      <template #avatar>
        <q-icon name="error_outline" color="negative" size="30px" />
      </template>

      <div class="error-text">
        {{ errorMessage }}
      </div>

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

    <div class="summary-grid">
      <div class="summary-card">
        <div>
          <div class="summary-label">Total Requests</div>
          <div class="summary-value">{{ leaveData.length }}</div>
        </div>

        <div class="summary-icon summary-icon-blue">
          <q-icon name="description" />
        </div>
      </div>

      <div class="summary-card">
        <div>
          <div class="summary-label">Pending</div>
          <div class="summary-value">{{ pendingCount }}</div>
        </div>

        <div class="summary-icon summary-icon-orange">
          <q-icon name="schedule" />
        </div>
      </div>

      <div class="summary-card">
        <div>
          <div class="summary-label">Approved</div>
          <div class="summary-value">{{ approvedCount }}</div>
        </div>

        <div class="summary-icon summary-icon-green">
          <q-icon name="check_circle" />
        </div>
      </div>

      <div class="summary-card">
        <div>
          <div class="summary-label">Rejected</div>
          <div class="summary-value">{{ rejectedCount }}</div>
        </div>

        <div class="summary-icon summary-icon-red">
          <q-icon name="cancel" />
        </div>
      </div>
    </div>

    <q-card class="report-card" flat bordered>
      <div class="filter-bar">
        <q-input
          v-model="search"
          outlined
          dense
          clearable
          placeholder="Search"
          class="search-input"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-select
          v-model="statusFilter"
          :options="statusOptions"
          outlined
          dense
          emit-value
          map-options
          label="Status"
          class="filter-select"
        />

        <q-select
          v-model="leaveTypeFilter"
          :options="leaveTypeOptions"
          outlined
          dense
          emit-value
          map-options
          label="Leave Type"
          class="filter-select"
        />
      </div>

      <q-separator />

      <div class="table-wrapper">
        <q-table
          :rows="filteredLeaveData"
          :columns="columns"
          row-key="id"
          flat
          :loading="loading"
          :rows-per-page-options="[10, 20, 50]"
          class="leave-table"
          no-data-label=""
        >
          <template #loading>
            <q-inner-loading showing color="primary">
              <q-spinner color="primary" size="32px" />
            </q-inner-loading>
          </template>

          <template #body-cell-leave_type="props">
            <q-td :props="props">
              <div class="leave-type-cell">
                <div class="leave-type-icon">
                  <q-icon name="event_available" />
                </div>

                <div>
                  <div class="leave-type-name">
                    {{ props.row.leave_type_name || '—' }}
                  </div>

                  <div
                    v-if="isManagement && props.row.employee_name"
                    class="employee-name"
                  >
                    {{ props.row.employee_name }}
                  </div>
                </div>
              </div>
            </q-td>
          </template>

          <template #body-cell-description="props">
            <q-td :props="props">
              <div class="description-cell">
                {{ props.row.description || 'No description provided' }}
              </div>
            </q-td>
          </template>

          <template #body-cell-dates="props">
            <q-td :props="props">
              <div class="date-cell">
                <div class="date-range">
                  {{ formatDate(props.row.from_date) }}
                  <span>→</span>
                  {{ formatDate(props.row.to_date) }}
                </div>

                <div class="days-count">
                  {{ props.row.total_days || 0 }}
                  {{ Number(props.row.total_days) === 1 ? 'day' : 'days' }}
                </div>
              </div>
            </q-td>
          </template>

          <template #body-cell-requested_on="props">
            <q-td :props="props">
              <div class="requested-date">
                {{ formatDate(props.row.request_date) }}
              </div>
            </q-td>
          </template>

          <template #body-cell-status="props">
            <q-td :props="props">
              <q-badge
                :class="['status-badge', statusClass(props.row.status)]"
                rounded
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

          <template #no-data>
            <div class="empty-state">
              <div class="empty-icon">
                <q-icon name="event_busy" size="30px" />
              </div>

              <div class="empty-title">
                {{ search || statusFilter !== 'ALL' || leaveTypeFilter !== 'ALL'
                  ? 'No matching leave requests'
                  : 'No leave requests found' }}
              </div>

              <div class="empty-subtitle">
                {{ search || statusFilter !== 'ALL' || leaveTypeFilter !== 'ALL'
                  ? 'Try changing your search or filter options.'
                  : isManagement
                    ? 'Employee leave requests will appear here.'
                    : 'Your submitted leave requests will appear here.' }}
              </div>
            </div>
          </template>
        </q-table>
      </div>
    </q-card>
  </div>
</template>

<script>
import api from 'src/services/api'

export default {
  name: 'LeaveReport',

  data() {
    return {
      loading: false,
      errorMessage: '',

      currentUser: null,
      currentEmployee: null,

      leaveData: [],

      search: '',
      statusFilter: 'ALL',
      leaveTypeFilter: 'ALL',

      statusOptions: [
        { label: 'All Statuses', value: 'ALL' },
        { label: 'Pending', value: 'PENDING' },
        { label: 'Approved', value: 'APPROVED' },
        { label: 'Rejected', value: 'REJECTED' },
        { label: 'Cancelled', value: 'CANCELLED' }
      ],

      columns: [
        {
          name: 'leave_type',
          label: 'LEAVE TYPE',
          field: 'leave_type_name',
          align: 'left',
          sortable: true
        },
        {
          name: 'description',
          label: 'DESCRIPTION',
          field: 'description',
          align: 'left'
        },
        {
          name: 'dates',
          label: 'LEAVE DATES',
          field: 'from_date',
          align: 'left',
          sortable: true
        },
        {
          name: 'requested_on',
          label: 'REQUESTED ON',
          field: 'request_date',
          align: 'left',
          sortable: true
        },
        {
          name: 'status',
          label: 'STATUS',
          field: 'status',
          align: 'left',
          sortable: true
        }
      ]
    }
  },

  computed: {
    role() {
      return String(this.currentUser?.role || '').toUpperCase()
    },

    isManagement() {
      return this.role === 'ADMIN' || this.role === 'MANAGER'
    },

    pendingCount() {
      return this.leaveData.filter(
        item => String(item.status || '').toUpperCase() === 'PENDING'
      ).length
    },

    approvedCount() {
      return this.leaveData.filter(
        item => String(item.status || '').toUpperCase() === 'APPROVED'
      ).length
    },

    rejectedCount() {
      return this.leaveData.filter(
        item => String(item.status || '').toUpperCase() === 'REJECTED'
      ).length
    },

    leaveTypeOptions() {
      const types = [...new Set(
        this.leaveData
          .map(item => item.leave_type_name)
          .filter(Boolean)
      )]

      return [
        { label: 'All Leave Types', value: 'ALL' },
        ...types.map(type => ({
          label: type,
          value: type
        }))
      ]
    },

    filteredLeaveData() {
      const searchText = this.search.trim().toLowerCase()

      return this.leaveData.filter(item => {
        const status = String(item.status || '').toUpperCase()
        const leaveType = String(item.leave_type_name || '')
        const description = String(item.description || '')
        const employeeName = String(item.employee_name || '')
        const employeeId = String(item.employee_id || '')

        const matchesSearch =
          !searchText ||
          leaveType.toLowerCase().includes(searchText) ||
          description.toLowerCase().includes(searchText) ||
          employeeName.toLowerCase().includes(searchText) ||
          employeeId.toLowerCase().includes(searchText)

        const matchesStatus =
          this.statusFilter === 'ALL' ||
          status === this.statusFilter

        const matchesLeaveType =
          this.leaveTypeFilter === 'ALL' ||
          leaveType === this.leaveTypeFilter

        return matchesSearch && matchesStatus && matchesLeaveType
      })
    }
  },

  mounted() {
    this.loadReport()
  },

  methods: {
    async loadReport() {
      this.loading = true
      this.errorMessage = ''

      try {
        const userResponse = await api.get('/auth/me/')
        this.currentUser = userResponse.data

        /*
         * ADMIN and MANAGER do not need an Employee profile.
         * They can view the management leave report directly.
         */
        if (this.isManagement) {
          this.currentEmployee = this.currentUser?.employee_profile || null
        } else {
          this.currentEmployee = this.currentUser?.employee_profile || null

          if (!this.currentEmployee) {
            const employeesResponse = await api.get('/employees/')

            const employees = Array.isArray(employeesResponse.data)
              ? employeesResponse.data
              : Array.isArray(employeesResponse.data?.results)
                ? employeesResponse.data.results
                : []

            this.currentEmployee = employees.find(employee =>
              Number(employee.user) === Number(this.currentUser?.id)
            ) || null
          }

          if (!this.currentEmployee) {
            this.leaveData = []
            this.errorMessage = 'No employee profile is linked to the current user.'
            return
          }
        }

        const leaveResponse = await api.get('/leave/requests/')

        const requests = Array.isArray(leaveResponse.data)
          ? leaveResponse.data
          : Array.isArray(leaveResponse.data?.results)
            ? leaveResponse.data.results
            : []

        /*
         * Management users see all available leave requests.
         * Normal employees see only their own requests.
         */
        if (this.isManagement) {
          this.leaveData = requests.map(request => ({
            ...request,
            status: String(request.status || '').toUpperCase()
          }))
        } else {
          const employeeId = Number(this.currentEmployee.id)

          this.leaveData = requests
            .filter(request => {
              const requestEmployee = request.employee

              if (
                requestEmployee &&
                typeof requestEmployee === 'object'
              ) {
                return Number(requestEmployee.id) === employeeId
              }

              return Number(requestEmployee) === employeeId
            })
            .map(request => ({
              ...request,
              status: String(request.status || '').toUpperCase()
            }))
        }
      } catch (error) {
        console.error('Leave report loading error:', error)

        this.leaveData = []

        this.errorMessage =
          error?.response?.data?.detail ||
          error?.response?.data?.message ||
          'Unable to load leave reports. Please try again.'
      } finally {
        this.loading = false
      }
    },

    formatDate(date) {
      if (!date) {
        return '—'
      }

      const parsedDate = new Date(date)

      if (Number.isNaN(parsedDate.getTime())) {
        return date
      }

      return parsedDate.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
    },

    formatStatus(status) {
      const normalized = String(status || '').toUpperCase()

      if (!normalized) {
        return 'Unknown'
      }

      return normalized.charAt(0) + normalized.slice(1).toLowerCase()
    },

    statusClass(status) {
      const normalized = String(status || '').toUpperCase()

      return {
        'status-pending': normalized === 'PENDING',
        'status-approved': normalized === 'APPROVED',
        'status-rejected': normalized === 'REJECTED',
        'status-cancelled': normalized === 'CANCELLED'
      }
    },

    statusIcon(status) {
      const normalized = String(status || '').toUpperCase()

      const icons = {
        PENDING: 'schedule',
        APPROVED: 'check_circle',
        REJECTED: 'cancel',
        CANCELLED: 'block'
      }

      return icons[normalized] || 'help_outline'
    }
  }
}
</script>

<style scoped>
.leave-report-page {
  min-height: 100%;
  padding: 16px;
  background: #f5f7fb;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e7f0ff;
  color: #1976d2;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #172033;
  line-height: 1.2;
}

.page-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #667085;
}

.error-banner {
  margin-bottom: 18px;
  border: 1px solid #ffcdd2;
  background: #fff4f4;
  color: #c62828;
}

.error-text {
  font-size: 13px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.summary-card {
  min-height: 68px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid #dfe4ec;
  border-radius: 13px;
  background: #ffffff;
}

.summary-label {
  font-size: 11px;
  color: #667085;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 20px;
  line-height: 1;
  font-weight: 700;
  color: #101828;
}

.summary-icon {
  width: 36px;
  height: 36px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 18px;
}

.summary-icon-blue {
  background: #e8f2ff;
  color: #1976d2;
}

.summary-icon-orange {
  background: #fff4df;
  color: #f59e0b;
}

.summary-icon-green {
  background: #e7f8ee;
  color: #16a05d;
}

.summary-icon-red {
  background: #ffebeb;
  color: #e53935;
}

.report-card {
  overflow: hidden;
  border-radius: 14px;
  background: #ffffff;
  border-color: #dfe4ec;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
}

.search-input {
  flex: 1;
  min-width: 220px;
}

.filter-select {
  width: 245px;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
}

.leave-table {
  min-width: 800px;
}

.leave-table :deep(thead tr) {
  background: #f8fafc;
}

.leave-table :deep(th) {
  height: 38px;
  padding: 0 14px;
  color: #526071;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.leave-table :deep(td) {
  height: 62px;
  padding: 8px 14px;
  border-color: #edf0f4;
}

.leave-type-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.leave-type-icon {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #edf4ff;
  color: #1976d2;
  flex-shrink: 0;
}

.leave-type-name {
  color: #1d2939;
  font-size: 13px;
  font-weight: 600;
}

.employee-name {
  margin-top: 2px;
  color: #667085;
  font-size: 11px;
}

.description-cell {
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #667085;
  font-size: 12px;
}

.date-cell {
  white-space: nowrap;
}

.date-range {
  color: #344054;
  font-size: 12px;
  font-weight: 600;
}

.date-range span {
  margin: 0 4px;
  color: #98a2b3;
}

.days-count {
  margin-top: 3px;
  color: #98a2b3;
  font-size: 10px;
}

.requested-date {
  color: #667085;
  font-size: 12px;
}

.status-badge {
  padding: 6px 9px;
  font-size: 10px;
  font-weight: 600;
}

.status-pending {
  background: #fff3d9;
  color: #b76e00;
}

.status-approved {
  background: #e5f7ed;
  color: #087443;
}

.status-rejected {
  background: #ffe8e8;
  color: #c62828;
}

.status-cancelled {
  background: #eef1f5;
  color: #667085;
}

.empty-state {
  width: 100%;
  min-height: 195px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 30px 20px;
}

.empty-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f4f9;
  color: #94a3b8;
  margin-bottom: 12px;
}

.empty-title {
  color: #344054;
  font-size: 13px;
  font-weight: 600;
}

.empty-subtitle {
  margin-top: 5px;
  color: #98a2b3;
  font-size: 11px;
}

@media (max-width: 900px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .filter-bar {
    flex-wrap: wrap;
  }

  .search-input,
  .filter-select {
    width: calc(50% - 6px);
    min-width: 0;
  }
}

@media (max-width: 600px) {
  .leave-report-page {
    padding: 12px;
  }

  .page-header {
    align-items: flex-start;
  }

  .page-header :deep(.q-btn) {
    flex-shrink: 0;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .search-input,
  .filter-select {
    width: 100%;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
}

.body--dark .leave-report-page {
  background: #111827;
}

.body--dark .page-title {
  color: #f1f5f9;
}

.body--dark .page-subtitle {
  color: #94a3b8;
}

.body--dark .header-icon {
  background: #172554;
  color: #60a5fa;
}

.body--dark .summary-card,
.body--dark .report-card {
  background: #18212f;
  border-color: #2d3748;
}

.body--dark .summary-label,
.body--dark .requested-date,
.body--dark .employee-name,
.body--dark .description-cell {
  color: #94a3b8;
}

.body--dark .summary-value,
.body--dark .leave-type-name,
.body--dark .date-range {
  color: #f1f5f9;
}

.body--dark .leave-table :deep(thead tr) {
  background: #202a38;
}

.body--dark .leave-table :deep(th) {
  color: #aab6c5;
}

.body--dark .leave-table :deep(td) {
  border-color: #2d3748;
}

.body--dark .empty-icon {
  background: #202a38;
  color: #94a3b8;
}

.body--dark .empty-title {
  color: #e2e8f0;
}

.body--dark .empty-subtitle {
  color: #94a3b8;
}

.body--dark .error-banner {
  background: #321d20;
  border-color: #5f292d;
}
</style>
