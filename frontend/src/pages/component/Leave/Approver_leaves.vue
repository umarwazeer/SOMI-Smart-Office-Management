<template>
  <div class="approver-page q-pa-md q-pa-lg-lg">
    <!-- Header -->
    <div class="row items-center justify-between q-col-gutter-md q-mb-lg">
      <div class="col-12 col-md">
        <div class="row items-center no-wrap">
          <div class="page-icon q-mr-md">
            <q-icon name="fact_check" size="27px" />
          </div>

          <div>
            <div class="text-h5 text-weight-bold text-grey-9">
              Leave Approvals
            </div>

            <div class="text-body2 text-grey-6 q-mt-xs">
              Review, approve, and manage employee leave requests.
            </div>
          </div>
        </div>
      </div>

      <div class="col-auto">
        <q-btn
          outline
          no-caps
          color="primary"
          icon="refresh"
          label="Refresh"
          :loading="loading"
          @click="loadLeaveRequests"
        />
      </div>
    </div>

    <!-- Error -->
    <q-banner
      v-if="errorMessage"
      rounded
      class="bg-red-1 text-negative q-mb-lg"
    >
      <template v-slot:avatar>
        <q-icon name="error_outline" />
      </template>

      {{ errorMessage }}

      <template v-slot:action>
        <q-btn
          flat
          dense
          color="negative"
          label="Dismiss"
          @click="errorMessage = ''"
        />
      </template>
    </q-banner>

    <!-- Summary -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="row items-center justify-between">
              <div>
                <div class="text-caption text-grey-6">
                  Total Requests
                </div>

                <div class="summary-value">
                  {{ rows.length }}
                </div>
              </div>

              <div class="summary-icon primary-icon">
                <q-icon name="description" size="23px" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="row items-center justify-between">
              <div>
                <div class="text-caption text-grey-6">
                  Pending
                </div>

                <div class="summary-value">
                  {{ pendingCount }}
                </div>
              </div>

              <div class="summary-icon warning-icon">
                <q-icon name="schedule" size="23px" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="row items-center justify-between">
              <div>
                <div class="text-caption text-grey-6">
                  Approved
                </div>

                <div class="summary-value">
                  {{ approvedCount }}
                </div>
              </div>

              <div class="summary-icon positive-icon">
                <q-icon name="check_circle" size="23px" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered class="summary-card">
          <q-card-section>
            <div class="row items-center justify-between">
              <div>
                <div class="text-caption text-grey-6">
                  Rejected
                </div>

                <div class="summary-value">
                  {{ rejectedCount }}
                </div>
              </div>

              <div class="summary-icon negative-icon">
                <q-icon name="cancel" size="23px" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Main Table -->
    <q-card flat bordered class="table-card">
      <q-card-section class="table-toolbar">
        <div class="row items-center q-col-gutter-md">
          <!-- Search -->
          <div class="col-12 col-md-4">
            <q-input
              v-model="filter"
              outlined
              dense
              clearable
              placeholder="Search employee, department or leave type..."
            >
              <template v-slot:prepend>
                <q-icon name="search" color="grey-6" />
              </template>
            </q-input>
          </div>

          <!-- Status -->
          <div class="col-12 col-sm-6 col-md-2">
            <q-select
              v-model="statusFilter"
              :options="statusOptions"
              outlined
              dense
              emit-value
              map-options
              label="Status"
            />
          </div>

          <!-- Department -->
          <div class="col-12 col-sm-6 col-md-2">
            <q-select
              v-model="departmentFilter"
              :options="departmentOptions"
              outlined
              dense
              emit-value
              map-options
              label="Department"
            />
          </div>

          <!-- Spacer -->
          <div class="col-md"></div>

          <!-- Add -->
          <div class="col-12 col-sm-auto">
            <q-btn
              unelevated
              no-caps
              color="primary"
              icon="add"
              label="Leave Request"
              class="full-width"
              @click="addLeave = true"
            />
          </div>
        </div>

        <div
          v-if="hasActiveFilters"
          class="row items-center q-mt-md"
        >
          <q-chip
            dense
            outline
            color="primary"
            icon="filter_alt"
          >
            Filters applied
          </q-chip>

          <q-btn
            flat
            dense
            no-caps
            color="grey-7"
            label="Clear filters"
            class="q-ml-sm"
            @click="clearFilters"
          />
        </div>
      </q-card-section>

      <q-separator />

      <q-table
        flat
        :rows="filteredRows"
        :columns="columns"
        row-key="id"
        :loading="loading"
        :pagination="pagination"
        class="leave-table"
        no-data-label="No leave requests found"
        no-results-label="No matching leave requests"
      >
        <!-- Employee -->
        <template v-slot:body-cell-employee="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-avatar
                size="38px"
                class="employee-avatar"
              >
                <span>
                  {{ getInitials(props.row.employee_name) }}
                </span>
              </q-avatar>

              <div class="q-ml-sm">
                <div class="text-weight-medium text-grey-9">
                  {{ props.row.employee_name || 'Unknown Employee' }}
                </div>

                <div class="text-caption text-grey-6">
                  {{ props.row.employee_id || '—' }}
                </div>
              </div>
            </div>
          </q-td>
        </template>

        <!-- Leave Type -->
        <template v-slot:body-cell-leave_type="props">
          <q-td :props="props">
            <div class="text-weight-medium text-grey-9">
              {{ props.row.leave_type_name || '—' }}
            </div>

            <div class="text-caption text-grey-6">
              {{ props.row.total_days || 0 }}
              {{ Number(props.row.total_days) === 1 ? 'day' : 'days' }}
            </div>
          </q-td>
        </template>

        <!-- Department -->
        <template v-slot:body-cell-department="props">
          <q-td :props="props">
            <span class="text-grey-8">
              {{ props.row.department_name || 'No Department' }}
            </span>
          </q-td>
        </template>

        <!-- Dates -->
        <template v-slot:body-cell-dates="props">
          <q-td :props="props">
            <div class="text-weight-medium text-grey-9">
              {{ formatDate(props.row.from_date) }}
            </div>

            <div class="text-caption text-grey-6">
              to {{ formatDate(props.row.to_date) }}
            </div>
          </q-td>
        </template>

        <!-- Status -->
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge
              rounded
              :color="getStatusColor(props.row.status)"
              class="status-badge"
            >
              <q-icon
                :name="getStatusIcon(props.row.status)"
                size="14px"
                class="q-mr-xs"
              />

              {{ formatStatus(props.row.status) }}
            </q-badge>
          </q-td>
        </template>

        <!-- Actions -->
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <div class="row items-center justify-end q-gutter-xs">
              <q-btn
                round
                flat
                dense
                color="primary"
                icon="visibility"
                @click="viewLeave(props.row)"
              >
                <q-tooltip>
                  View Leave
                </q-tooltip>
              </q-btn>

              <q-btn
                v-if="props.row.status === 'PENDING'"
                round
                flat
                dense
                color="positive"
                icon="check_circle"
                :loading="processingId === props.row.id"
                @click="approveLeave(props.row)"
              >
                <q-tooltip>
                  Approve Leave
                </q-tooltip>
              </q-btn>

              <q-btn
                v-if="props.row.status === 'PENDING'"
                round
                flat
                dense
                color="negative"
                icon="cancel"
                :loading="processingId === props.row.id"
                @click="openRejectDialog(props.row)"
              >
                <q-tooltip>
                  Reject Leave
                </q-tooltip>
              </q-btn>

              <q-btn
                round
                flat
                dense
                color="negative"
                icon="delete_outline"
                :loading="deletingId === props.row.id"
                @click="deleteLeave(props.row)"
              >
                <q-tooltip>
                  Delete Leave Request
                </q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

        <!-- Loading -->
        <template v-slot:loading>
          <q-inner-loading showing color="primary" />
        </template>

        <!-- Empty -->
        <template v-slot:no-data>
          <div class="full-width column items-center q-pa-xl">
            <q-icon
              name="event_busy"
              size="52px"
              color="grey-5"
            />

            <div class="text-subtitle1 text-weight-medium text-grey-7 q-mt-md">
              No leave requests found
            </div>

            <div class="text-body2 text-grey-5 q-mt-xs">
              Try changing your filters or create a new leave request.
            </div>
          </div>
        </template>
      </q-table>
    </q-card>

    <!-- Add Leave Request -->
    <q-dialog
      v-model="addLeave"
      persistent
    >
      <q-card class="leave-dialog-card">
        <q-card-section class="dialog-header">
          <div class="row items-center justify-between">
            <div class="row items-center">
              <div class="dialog-icon">
                <q-icon name="event_available" size="22px" />
              </div>

              <div class="q-ml-md">
                <div class="text-subtitle1 text-weight-bold">
                  New Leave Request
                </div>

                <div class="text-caption text-grey-6">
                  Create a leave request for an employee.
                </div>
              </div>
            </div>

            <q-btn
              round
              flat
              dense
              icon="close"
              color="grey-7"
              v-close-popup
            />
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section class="dialog-body">
          <leave-page
            @saved="handleLeaveSaved"
          />
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Leave Details -->
    <LeaveDetailsDialog
      :visible="viewLeaveDialog"
      :leave="selectedLeave"
      @approve="approveLeaveById"
      @reject="openRejectDialog"
      @close="closeLeaveDialog"
    />

    <!-- Reject Dialog -->
    <q-dialog
      v-model="rejectDialog"
      persistent
    >
      <q-card class="reject-dialog-card">
        <q-card-section>
          <div class="text-h6 text-weight-bold">
            Reject Leave Request
          </div>

          <div class="text-body2 text-grey-6 q-mt-xs">
            Add an optional reason for rejecting this request.
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="reviewerRemarks"
            outlined
            type="textarea"
            autogrow
            rows="4"
            maxlength="500"
            counter
            label="Reviewer Remarks"
            placeholder="Enter the reason for rejection..."
          />
        </q-card-section>

        <q-card-actions
          align="right"
          class="q-pa-md"
        >
          <q-btn
            flat
            no-caps
            color="grey-7"
            label="Cancel"
            :disable="processingId !== null"
            @click="closeRejectDialog"
          />

          <q-btn
            unelevated
            no-caps
            color="negative"
            icon="cancel"
            label="Reject Leave"
            :loading="processingId !== null"
            @click="rejectLeave"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import api from 'src/services/api'
import LeavePage from './leavePage.vue'
import LeaveDetailsDialog from './LeaveDetailsDialog.vue'

export default {
  name: 'ApproverLeaves',

  components: {
    LeavePage,
    LeaveDetailsDialog
  },

  data () {
    return {
      addLeave: false,

      filter: '',
      statusFilter: 'ALL',
      departmentFilter: 'ALL',

      loading: false,
      processingId: null,
      deletingId: null,

      errorMessage: '',

      rows: [],
      selectedLeave: null,
      viewLeaveDialog: false,

      rejectDialog: false,
      reviewerRemarks: '',
      rejectTarget: null,

      pagination: {
        page: 1,
        rowsPerPage: 10
      },

      statusOptions: [
        {
          label: 'All Statuses',
          value: 'ALL'
        },
        {
          label: 'Pending',
          value: 'PENDING'
        },
        {
          label: 'Approved',
          value: 'APPROVED'
        },
        {
          label: 'Rejected',
          value: 'REJECTED'
        },
        {
          label: 'Cancelled',
          value: 'CANCELLED'
        }
      ],

      columns: [
        {
          name: 'employee',
          label: 'Employee',
          align: 'left',
          field: row => row.employee_name || 'Unknown',
          sortable: true
        },
        {
          name: 'leave_type',
          label: 'Leave Type',
          align: 'left',
          field: row => row.leave_type_name || '',
          sortable: true
        },
        {
          name: 'department',
          label: 'Department',
          align: 'left',
          field: row => row.department_name || '',
          sortable: true
        },
        {
          name: 'dates',
          label: 'Leave Dates',
          align: 'left',
          field: row => row.from_date || '',
          sortable: true
        },
        {
          name: 'request_date',
          label: 'Requested',
          align: 'left',
          field: row => row.request_date || '',
          sortable: true
        },
        {
          name: 'status',
          label: 'Status',
          align: 'left',
          field: row => row.status || '',
          sortable: true
        },
        {
          name: 'actions',
          label: 'Actions',
          align: 'right',
          field: 'actions',
          sortable: false
        }
      ]
    }
  },

  computed: {
    filteredRows () {
      const search = String(this.filter || '')
        .trim()
        .toLowerCase()

      return this.rows.filter(row => {
        const statusMatches =
          this.statusFilter === 'ALL' ||
          row.status === this.statusFilter

        const departmentMatches =
          this.departmentFilter === 'ALL' ||
          String(row.department_name || '') ===
            String(this.departmentFilter)

        const searchableText = [
          row.employee_name,
          row.employee_id,
          row.department_name,
          row.leave_type_name,
          row.description,
          row.status
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()

        const searchMatches =
          !search ||
          searchableText.includes(search)

        return (
          statusMatches &&
          departmentMatches &&
          searchMatches
        )
      })
    },

    departmentOptions () {
      const departments = [
        ...new Set(
          this.rows
            .map(row => row.department_name)
            .filter(Boolean)
        )
      ].sort((a, b) =>
        a.localeCompare(b)
      )

      return [
        {
          label: 'All Departments',
          value: 'ALL'
        },
        ...departments.map(department => ({
          label: department,
          value: department
        }))
      ]
    },

    pendingCount () {
      return this.rows.filter(
        row => row.status === 'PENDING'
      ).length
    },

    approvedCount () {
      return this.rows.filter(
        row => row.status === 'APPROVED'
      ).length
    },

    rejectedCount () {
      return this.rows.filter(
        row => row.status === 'REJECTED'
      ).length
    },

    hasActiveFilters () {
      return Boolean(
        this.filter ||
        this.statusFilter !== 'ALL' ||
        this.departmentFilter !== 'ALL'
      )
    }
  },

  mounted () {
    this.loadLeaveRequests()
  },

  methods: {
    async loadLeaveRequests () {
      this.loading = true
      this.errorMessage = ''

      try {
        const response =
          await api.get('/leave/requests/')

        const data = Array.isArray(
          response.data
        )
          ? response.data
          : response.data?.results || []

        this.rows = data.map(
          request => ({
            ...request,
            status: String(
              request.status || ''
            ).toUpperCase()
          })
        )
      } catch (error) {
        console.error(
          'Failed to load leave requests:',
          error
        )

        this.errorMessage =
          this.getApiErrorMessage(
            error,
            'Unable to load leave requests.'
          )
      } finally {
        this.loading = false
      }
    },

    async approveLeave (leave) {
      if (!leave?.id) {
        return
      }

      this.processingId = leave.id
      this.errorMessage = ''

      try {
        const response =
          await api.patch(
            `/leave/requests/${leave.id}/review/`,
            {
              status: 'APPROVED'
            }
          )

        this.updateRow(
          response.data
        )

        this.$q.notify({
          type: 'positive',
          icon: 'check_circle',
          message:
            'Leave request approved successfully.'
        })

        if (
          this.selectedLeave?.id ===
          leave.id
        ) {
          this.selectedLeave =
            response.data
        }
      } catch (error) {
        console.error(
          'Failed to approve leave:',
          error
        )

        const message =
          this.getApiErrorMessage(
            error,
            'Failed to approve leave request.'
          )

        this.errorMessage = message

        this.$q.notify({
          type: 'negative',
          icon: 'error_outline',
          message
        })
      } finally {
        this.processingId = null
      }
    },

    approveLeaveById (leaveOrId) {
      const id =
        typeof leaveOrId === 'object'
          ? leaveOrId?.id
          : leaveOrId

      const leave =
        this.rows.find(
          row => row.id === id
        )

      if (leave) {
        this.approveLeave(leave)
      }
    },

    openRejectDialog (leave) {
      this.rejectTarget = leave
      this.reviewerRemarks = ''
      this.rejectDialog = true
    },

    closeRejectDialog () {
      if (this.processingId !== null) {
        return
      }

      this.rejectDialog = false
      this.reviewerRemarks = ''
      this.rejectTarget = null
    },

    async rejectLeave () {
      const leave =
        this.rejectTarget

      if (!leave?.id) {
        return
      }

      this.processingId = leave.id
      this.errorMessage = ''

      try {
        const response =
          await api.patch(
            `/leave/requests/${leave.id}/review/`,
            {
              status: 'REJECTED',
              reviewer_remarks:
                this.reviewerRemarks.trim()
            }
          )

        this.updateRow(
          response.data
        )

        this.$q.notify({
          type: 'negative',
          icon: 'cancel',
          message:
            'Leave request rejected.'
        })

        this.rejectDialog = false
        this.reviewerRemarks = ''
        this.rejectTarget = null

        if (
          this.selectedLeave?.id ===
          leave.id
        ) {
          this.selectedLeave =
            response.data
        }
      } catch (error) {
        console.error(
          'Failed to reject leave:',
          error
        )

        const message =
          this.getApiErrorMessage(
            error,
            'Failed to reject leave request.'
          )

        this.errorMessage = message

        this.$q.notify({
          type: 'negative',
          icon: 'error_outline',
          message
        })
      } finally {
        this.processingId = null
      }
    },

    viewLeave (leave) {
      this.selectedLeave = {
        ...leave
      }

      this.viewLeaveDialog = true
    },

    closeLeaveDialog () {
      this.viewLeaveDialog = false
      this.selectedLeave = null
    },

    async deleteLeave (leave) {
      if (!leave?.id) {
        return
      }

      this.$q
        .dialog({
          title: 'Delete Leave Request',
          message:
            `Are you sure you want to permanently delete the leave request for ${leave.employee_name || 'this employee'}?`,
          cancel: {
            flat: true,
            color: 'grey-7'
          },
          ok: {
            unelevated: true,
            color: 'negative',
            label: 'Delete'
          },
          persistent: true
        })
        .onOk(async () => {
          this.deletingId = leave.id

          try {
            await api.delete(
              `/leave/requests/${leave.id}/`
            )

            this.rows =
              this.rows.filter(
                row =>
                  row.id !== leave.id
              )

            this.$q.notify({
              type: 'positive',
              icon: 'delete',
              message:
                'Leave request deleted successfully.'
            })
          } catch (error) {
            console.error(
              'Failed to delete leave:',
              error
            )

            const message =
              this.getApiErrorMessage(
                error,
                'Failed to delete leave request.'
              )

            this.$q.notify({
              type: 'negative',
              icon: 'error_outline',
              message
            })
          } finally {
            this.deletingId = null
          }
        })
    },

    handleLeaveSaved () {
      this.addLeave = false
      this.loadLeaveRequests()
    },

    updateRow (updatedLeave) {
      if (!updatedLeave?.id) {
        return
      }

      const index =
        this.rows.findIndex(
          row =>
            row.id ===
            updatedLeave.id
        )

      if (index === -1) {
        this.rows.unshift({
          ...updatedLeave,
          status: String(
            updatedLeave.status || ''
          ).toUpperCase()
        })

        return
      }

      this.rows.splice(
        index,
        1,
        {
          ...this.rows[index],
          ...updatedLeave,
          status: String(
            updatedLeave.status ||
            this.rows[index].status ||
            ''
          ).toUpperCase()
        }
      )
    },

    clearFilters () {
      this.filter = ''
      this.statusFilter = 'ALL'
      this.departmentFilter = 'ALL'
    },

    formatDate (value) {
      if (!value) {
        return '—'
      }

      const parts =
        String(value).split('-')

      if (parts.length !== 3) {
        return value
      }

      return `${parts[2]}-${parts[1]}-${parts[0]}`
    },

    formatStatus (status) {
      if (!status) {
        return 'Unknown'
      }

      return String(status)
        .toLowerCase()
        .replace(/_/g, ' ')
        .replace(/\b\w/g, letter =>
          letter.toUpperCase()
        )
    },

    getStatusColor (status) {
      switch (status) {
        case 'APPROVED':
          return 'positive'

        case 'REJECTED':
          return 'negative'

        case 'CANCELLED':
          return 'grey-7'

        case 'PENDING':
        default:
          return 'warning'
      }
    },

    getStatusIcon (status) {
      switch (status) {
        case 'APPROVED':
          return 'check_circle'

        case 'REJECTED':
          return 'cancel'

        case 'CANCELLED':
          return 'block'

        case 'PENDING':
        default:
          return 'schedule'
      }
    },

    getInitials (name) {
      if (!name) {
        return 'EM'
      }

      const words =
        String(name)
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
.approver-page {
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

.summary-card {
  border-radius: 15px;
  background: #ffffff;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
}

.summary-value {
  margin-top: 4px;
  font-size: 25px;
  line-height: 1.1;
  font-weight: 700;
  color: #1f2937;
}

.summary-icon {
  width: 43px;
  height: 43px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.primary-icon {
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.warning-icon {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
}

.positive-icon {
  background: rgba(34, 197, 94, 0.11);
  color: #16a34a;
}

.negative-icon {
  background: rgba(239, 68, 68, 0.11);
  color: #dc2626;
}

.table-card {
  border-radius: 16px;
  background: #ffffff;
  overflow: hidden;
}

.table-toolbar {
  padding: 18px;
}

.leave-table :deep(thead tr) {
  background: #f8fafc;
}

.leave-table :deep(th) {
  color: #64748b;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.leave-table :deep(td) {
  height: 68px;
  border-color: #edf1f5;
}

.employee-avatar {
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
  font-size: 13px;
  font-weight: 700;
}

.status-badge {
  padding: 6px 9px;
  font-size: 11px;
  font-weight: 600;
}

.leave-dialog-card {
  width: 850px;
  max-width: 94vw;
  max-height: 90vh;
  border-radius: 17px;
  overflow: hidden;
}

.dialog-header {
  padding: 18px 20px;
}

.dialog-icon {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.dialog-body {
  padding: 0;
  max-height: calc(90vh - 85px);
  overflow-y: auto;
}

.reject-dialog-card {
  width: 520px;
  max-width: 92vw;
  border-radius: 16px;
}

@media (max-width: 599px) {
  .approver-page {
    padding: 12px;
  }

  .page-icon {
    width: 44px;
    height: 44px;
  }

  .table-toolbar {
    padding: 14px;
  }

  .leave-table :deep(td) {
    height: 60px;
  }

  .summary-value {
    font-size: 22px;
  }
}
</style>
