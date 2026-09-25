<template>
  <q-dialog
    :model-value="visible"
    @update:model-value="updateVisible"
  >
    <q-card class="leave-details-card">
      <!-- Header -->
      <q-card-section class="dialog-header">
        <div class="row items-center justify-between no-wrap">
          <div class="row items-center no-wrap">
            <div class="header-icon">
              <q-icon name="event_note" size="24px" />
            </div>

            <div class="q-ml-md">
              <div class="text-h6 text-weight-bold text-grey-9">
                Leave Details
              </div>

              <div class="text-caption text-grey-6 q-mt-xs">
                Complete information about this leave request
              </div>
            </div>
          </div>

          <q-btn
            round
            flat
            dense
            icon="close"
            color="grey-7"
            @click="closeDialog"
          />
        </div>
      </q-card-section>

      <q-separator />

      <q-card-section class="dialog-content">
        <!-- Employee Header -->
        <div class="employee-card">
          <q-avatar
            size="54px"
            class="employee-avatar"
          >
            {{ getInitials(leave.employee_name) }}
          </q-avatar>

          <div class="employee-info">
            <div class="employee-name">
              {{ leave.employee_name || 'Unknown Employee' }}
            </div>

            <div class="employee-id">
              {{ leave.employee_id || 'Employee ID unavailable' }}
            </div>

            <div class="employee-department">
              <q-icon
                name="business"
                size="14px"
                class="q-mr-xs"
              />
              {{ leave.department_name || 'No Department' }}
            </div>
          </div>

          <q-space />

          <q-badge
            rounded
            :color="getStatusColor(leave.status)"
            class="status-badge"
          >
            <q-icon
              :name="getStatusIcon(leave.status)"
              size="14px"
              class="q-mr-xs"
            />

            {{ formatStatus(leave.status) }}
          </q-badge>
        </div>

        <!-- Leave Information -->
        <div class="section-heading">
          <div class="section-icon">
            <q-icon name="event" size="18px" />
          </div>

          <div>
            <div class="section-title">
              Leave Information
            </div>

            <div class="section-subtitle">
              Dates and type of requested leave
            </div>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-box">
            <div class="info-icon">
              <q-icon name="category" size="18px" />
            </div>

            <div>
              <div class="info-label">
                Leave Type
              </div>

              <div class="info-value">
                {{ leave.leave_type_name || '—' }}
              </div>
            </div>
          </div>

          <div class="info-box">
            <div class="info-icon">
              <q-icon name="schedule" size="18px" />
            </div>

            <div>
              <div class="info-label">
                Duration
              </div>

              <div class="info-value">
                {{ leave.total_days || 0 }}
                {{ Number(leave.total_days) === 1 ? 'Day' : 'Days' }}
              </div>
            </div>
          </div>

          <div class="info-box">
            <div class="info-icon">
              <q-icon name="event_available" size="18px" />
            </div>

            <div>
              <div class="info-label">
                From Date
              </div>

              <div class="info-value">
                {{ formatDate(leave.from_date) }}
              </div>
            </div>
          </div>

          <div class="info-box">
            <div class="info-icon">
              <q-icon name="event_busy" size="18px" />
            </div>

            <div>
              <div class="info-label">
                To Date
              </div>

              <div class="info-value">
                {{ formatDate(leave.to_date) }}
              </div>
            </div>
          </div>

          <div class="info-box">
            <div class="info-icon">
              <q-icon name="today" size="18px" />
            </div>

            <div>
              <div class="info-label">
                Requested On
              </div>

              <div class="info-value">
                {{ formatDate(leave.request_date) }}
              </div>
            </div>
          </div>

          <div class="info-box">
            <div class="info-icon">
              <q-icon name="business" size="18px" />
            </div>

            <div>
              <div class="info-label">
                Department
              </div>

              <div class="info-value">
                {{ leave.department_name || 'No Department' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="section-heading q-mt-lg">
          <div class="section-icon">
            <q-icon name="notes" size="18px" />
          </div>

          <div>
            <div class="section-title">
              Reason / Description
            </div>

            <div class="section-subtitle">
              Employee's explanation for the leave request
            </div>
          </div>
        </div>

        <div class="description-box">
          <div
            v-if="leave.description"
            class="description-text"
          >
            {{ leave.description }}
          </div>

          <div
            v-else
            class="empty-description"
          >
            <q-icon
              name="notes"
              size="20px"
              class="q-mr-sm"
            />
            No description was provided.
          </div>
        </div>

        <!-- Review Information -->
        <div
          v-if="
            leave.reviewed_by_name ||
            leave.reviewed_at ||
            leave.reviewer_remarks
          "
          class="review-section"
        >
          <div class="section-heading">
            <div class="section-icon review-icon">
              <q-icon name="rate_review" size="18px" />
            </div>

            <div>
              <div class="section-title">
                Review Information
              </div>

              <div class="section-subtitle">
                Approval or rejection details
              </div>
            </div>
          </div>

          <div class="review-card">
            <div
              v-if="leave.reviewed_by_name"
              class="review-item"
            >
              <span class="review-label">
                Reviewed By
              </span>

              <span class="review-value">
                {{ leave.reviewed_by_name }}
              </span>
            </div>

            <div
              v-if="leave.reviewed_at"
              class="review-item"
            >
              <span class="review-label">
                Reviewed At
              </span>

              <span class="review-value">
                {{ formatDateTime(leave.reviewed_at) }}
              </span>
            </div>

            <div
              v-if="leave.reviewer_remarks"
              class="review-remarks"
            >
              <div class="review-label q-mb-xs">
                Reviewer Remarks
              </div>

              <div class="remarks-text">
                {{ leave.reviewer_remarks }}
              </div>
            </div>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- Footer -->
      <q-card-actions class="dialog-footer">
        <q-btn
          flat
          no-caps
          color="grey-7"
          label="Close"
          @click="closeDialog"
        />

        <q-space />

        <q-btn
          v-if="isPending"
          flat
          no-caps
          color="negative"
          icon="cancel"
          label="Reject"
          @click="rejectLeave"
        />

        <q-btn
          v-if="isPending"
          unelevated
          no-caps
          color="positive"
          icon="check_circle"
          label="Approve"
          @click="approveLeave"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'LeaveDetailsDialog',

  props: {
    visible: {
      type: Boolean,
      default: false
    },

    leave: {
      type: Object,
      default: () => ({})
    }
  },

  computed: {
    isPending () {
      return String(
        this.leave?.status || ''
      ).toUpperCase() === 'PENDING'
    }
  },

  methods: {
    updateVisible (value) {
      this.$emit('update:visible', value)
    },

    closeDialog () {
      this.$emit('close')
    },

    approveLeave () {
      if (!this.leave?.id || !this.isPending) {
        return
      }

      this.$emit('approve', this.leave)
    },

    rejectLeave () {
      if (!this.leave?.id || !this.isPending) {
        return
      }

      this.$emit('reject', this.leave)
    },

    formatDate (value) {
      if (!value) {
        return '—'
      }

      const parts = String(value).split('-')

      if (parts.length !== 3) {
        return value
      }

      return `${parts[2]}-${parts[1]}-${parts[0]}`
    },

    formatDateTime (value) {
      if (!value) {
        return '—'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    formatStatus (status) {
      if (!status) {
        return 'Unknown'
      }

      return String(status)
        .toLowerCase()
        .replace(/_/g, ' ')
        .replace(/\b\w/g, letter => letter.toUpperCase())
    },

    getStatusColor (status) {
      switch (String(status || '').toUpperCase()) {
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
      switch (String(status || '').toUpperCase()) {
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
    }
  }
}
</script>

<style scoped>
.leave-details-card {
  width: 760px;
  max-width: 94vw;
  max-height: 90vh;
  border-radius: 18px;
  overflow: hidden;
  background: #ffffff;
}

.dialog-header {
  padding: 20px 22px;
}

.header-icon {
  width: 46px;
  height: 46px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.dialog-content {
  max-height: calc(90vh - 145px);
  overflow-y: auto;
  padding: 22px;
}

.employee-card {
  display: flex;
  align-items: center;
  padding: 17px;
  border-radius: 15px;
  background: #f8fafc;
  border: 1px solid #e8edf3;
}

.employee-avatar {
  flex-shrink: 0;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
  font-size: 16px;
  font-weight: 700;
}

.employee-info {
  min-width: 0;
  margin-left: 14px;
}

.employee-name {
  color: #1e293b;
  font-size: 16px;
  font-weight: 700;
}

.employee-id {
  margin-top: 2px;
  color: #64748b;
  font-size: 12px;
}

.employee-department {
  display: flex;
  align-items: center;
  margin-top: 5px;
  color: #64748b;
  font-size: 12px;
}

.status-badge {
  flex-shrink: 0;
  padding: 7px 10px;
  font-size: 11px;
  font-weight: 600;
}

.section-heading {
  display: flex;
  align-items: center;
  margin-bottom: 14px;
}

.section-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.09);
  color: #1976d2;
  flex-shrink: 0;
}

.section-title {
  margin-left: 10px;
  color: #334155;
  font-size: 14px;
  font-weight: 700;
}

.section-subtitle {
  margin-left: 10px;
  margin-top: 2px;
  color: #94a3b8;
  font-size: 11px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.info-box {
  display: flex;
  align-items: center;
  min-height: 70px;
  padding: 13px;
  border: 1px solid #e8edf3;
  border-radius: 12px;
  background: #ffffff;
}

.info-icon {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #f1f5f9;
  color: #64748b;
}

.info-label {
  margin-left: 10px;
  color: #94a3b8;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.info-value {
  margin-left: 10px;
  margin-top: 3px;
  color: #334155;
  font-size: 13px;
  font-weight: 600;
}

.description-box {
  padding: 15px;
  min-height: 70px;
  border-radius: 12px;
  border: 1px solid #e8edf3;
  background: #f8fafc;
}

.description-text {
  color: #475569;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre-wrap;
}

.empty-description {
  display: flex;
  align-items: center;
  color: #94a3b8;
  font-size: 13px;
}

.review-section {
  margin-top: 24px;
}

.review-icon {
  background: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

.review-card {
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #e8edf3;
  background: #f8fafc;
}

.review-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 5px 0;
}

.review-label {
  color: #94a3b8;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.review-value {
  color: #334155;
  font-size: 13px;
  font-weight: 600;
  text-align: right;
}

.review-remarks {
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.remarks-text {
  margin-top: 5px;
  color: #475569;
  font-size: 13px;
  line-height: 1.55;
}

.dialog-footer {
  min-height: 64px;
  padding: 12px 20px;
  background: #ffffff;
}

@media (max-width: 599px) {
  .leave-details-card {
    max-width: 96vw;
    border-radius: 15px;
  }

  .dialog-header {
    padding: 16px;
  }

  .dialog-content {
    padding: 16px;
  }

  .employee-card {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .employee-info {
    max-width: calc(100% - 70px);
  }

  .status-badge {
    margin-top: 12px;
    margin-left: 68px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .review-item {
    align-items: flex-start;
    flex-direction: column;
    gap: 3px;
  }

  .review-value {
    text-align: left;
  }

  .dialog-footer {
    padding: 10px 14px;
  }
}
</style>
