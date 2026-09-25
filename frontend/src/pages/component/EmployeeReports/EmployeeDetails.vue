<template>
  <q-dialog
    :model-value="visible"
    @update:model-value="updateVisible"
  >
    <q-card class="leave-details-card">
      <!-- Header -->
      <q-card-section class="dialog-header">
        <div class="header-left">
          <div class="header-icon">
            <q-icon name="event_note" size="24px" />
          </div>

          <div class="header-text">
            <div class="dialog-title">
              Leave Details
            </div>

            <div class="dialog-subtitle">
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
          aria-label="Close"
          @click="closeDialog"
        />
      </q-card-section>

      <q-separator />

      <q-card-section class="dialog-content">
        <!-- Employee Summary -->
        <div class="employee-card">
          <q-avatar
            size="56px"
            class="employee-avatar"
          >
            {{ getInitials(leave.employee_name) }}
          </q-avatar>

          <div class="employee-info">
            <div class="employee-name">
              {{ leave.employee_name || 'Unknown Employee' }}
            </div>

            <div class="employee-meta">
              <span>
                {{ leave.employee_id || 'Employee ID unavailable' }}
              </span>

              <span
                v-if="leave.department_name"
                class="meta-divider"
              >
                •
              </span>

              <span v-if="leave.department_name">
                {{ leave.department_name }}
              </span>
            </div>
          </div>

          <div class="employee-status">
            <div class="status-label">
              REQUEST STATUS
            </div>

            <div
              :class="[
                'status-badge',
                statusClass(leave.status)
              ]"
            >
              <q-icon
                :name="getStatusIcon(leave.status)"
                size="15px"
              />

              <span>
                {{ formatStatus(leave.status) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Leave Information -->
        <section class="content-section">
          <div class="section-heading">
            <div class="section-icon">
              <q-icon name="event" size="18px" />
            </div>

            <div>
              <div class="section-title">
                Leave Information
              </div>

              <div class="section-subtitle">
                Dates, type, duration and department details
              </div>
            </div>
          </div>

          <div class="info-grid">
            <div class="info-box">
              <div class="info-icon">
                <q-icon name="category" size="18px" />
              </div>

              <div class="info-content">
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

              <div class="info-content">
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

              <div class="info-content">
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

              <div class="info-content">
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

              <div class="info-content">
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

              <div class="info-content">
                <div class="info-label">
                  Department
                </div>

                <div class="info-value">
                  {{ leave.department_name || 'No Department' }}
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Description -->
        <section class="content-section">
          <div class="section-heading">
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
              <q-icon name="notes" size="20px" />

              <span>
                No description was provided.
              </span>
            </div>
          </div>
        </section>

        <!-- Review Information -->
        <section
          v-if="
            leave.reviewed_by_name ||
            leave.reviewed_at ||
            leave.reviewer_remarks
          "
          class="content-section review-section"
        >
          <div class="section-heading">
            <div class="section-icon review-section-icon">
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
              <div class="review-label">
                Reviewed By
              </div>

              <div class="review-value">
                {{ leave.reviewed_by_name }}
              </div>
            </div>

            <div
              v-if="leave.reviewed_at"
              class="review-item"
            >
              <div class="review-label">
                Reviewed At
              </div>

              <div class="review-value">
                {{ formatDateTime(leave.reviewed_at) }}
              </div>
            </div>

            <div
              v-if="leave.reviewer_remarks"
              class="review-remarks"
            >
              <div class="review-label">
                Reviewer Remarks
              </div>

              <div class="remarks-text">
                {{ leave.reviewer_remarks }}
              </div>
            </div>
          </div>
        </section>
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

        <template v-if="isPending">
          <q-btn
            flat
            no-caps
            color="negative"
            icon="cancel"
            label="Reject"
            @click="rejectLeave"
          />

          <q-btn
            unelevated
            no-caps
            color="positive"
            icon="check_circle"
            label="Approve"
            @click="approveLeave"
          />
        </template>
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
    isPending() {
      return String(
        this.leave?.status || ''
      ).toUpperCase() === 'PENDING'
    }
  },

  methods: {
    updateVisible(value) {
      this.$emit('update:visible', value)
    },

    closeDialog() {
      this.$emit('close')
    },

    approveLeave() {
      if (!this.leave?.id || !this.isPending) {
        return
      }

      this.$emit('approve', this.leave)
    },

    rejectLeave() {
      if (!this.leave?.id || !this.isPending) {
        return
      }

      this.$emit('reject', this.leave)
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

    formatDateTime(value) {
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

    formatStatus(status) {
      if (!status) {
        return 'Unknown'
      }

      return String(status)
        .toLowerCase()
        .replace(/_/g, ' ')
        .replace(/\b\w/g, letter => letter.toUpperCase())
    },

    statusClass(status) {
      switch (String(status || '').toUpperCase()) {
        case 'APPROVED':
          return 'status-approved'

        case 'REJECTED':
          return 'status-rejected'

        case 'CANCELLED':
          return 'status-cancelled'

        case 'PENDING':
        default:
          return 'status-pending'
      }
    },

    getStatusIcon(status) {
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
    }
  }
}
</script>

<style scoped>
.leave-details-card {
  width: 780px;
  max-width: 94vw;
  max-height: 90vh;
  overflow: hidden;
  border-radius: 18px;
  background: #ffffff;
}

.dialog-header {
  min-height: 76px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.header-left {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 13px;
}

.header-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #eaf2ff;
  color: #1976d2;
}

.header-text {
  min-width: 0;
}

.dialog-title {
  color: #172033;
  font-size: 17px;
  font-weight: 700;
  line-height: 1.25;
}

.dialog-subtitle {
  margin-top: 3px;
  color: #7a8699;
  font-size: 11px;
  line-height: 1.4;
}

.dialog-content {
  max-height: calc(90vh - 140px);
  overflow-y: auto;
  padding: 20px;
}

.employee-card {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 15px;
  border: 1px solid #e4e9f0;
  border-radius: 14px;
  background: #f8fafc;
}

.employee-avatar {
  flex-shrink: 0;
  background: #e7f0ff;
  color: #1976d2;
  font-size: 16px;
  font-weight: 700;
}

.employee-info {
  min-width: 0;
  flex: 1;
}

.employee-name {
  color: #1e293b;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.3;
}

.employee-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
  color: #718096;
  font-size: 11px;
}

.meta-divider {
  color: #b4becb;
}

.employee-status {
  flex-shrink: 0;
  text-align: right;
}

.status-label {
  margin-bottom: 5px;
  color: #98a2b3;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.status-badge {
  min-height: 27px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 5px 9px;
  border-radius: 7px;
  font-size: 10px;
  font-weight: 700;
}

.status-pending {
  background: #fff4dc;
  color: #b66b00;
}

.status-approved {
  background: #e7f7ee;
  color: #087443;
}

.status-rejected {
  background: #ffe9e9;
  color: #c62828;
}

.status-cancelled {
  background: #edf0f3;
  color: #667085;
}

.content-section {
  margin-top: 22px;
}

.section-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 13px;
}

.section-icon {
  width: 33px;
  height: 33px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  background: #edf4ff;
  color: #1976d2;
}

.section-title {
  color: #344054;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.25;
}

.section-subtitle {
  margin-top: 2px;
  color: #98a2b3;
  font-size: 10px;
  line-height: 1.35;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.info-box {
  min-height: 67px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px;
  border: 1px solid #e6ebf1;
  border-radius: 11px;
  background: #ffffff;
}

.info-icon {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  background: #f2f5f8;
  color: #667085;
}

.info-content {
  min-width: 0;
}

.info-label {
  color: #98a2b3;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.info-value {
  margin-top: 3px;
  color: #344054;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.35;
  word-break: break-word;
}

.description-box {
  min-height: 70px;
  padding: 14px;
  border: 1px solid #e6ebf1;
  border-radius: 11px;
  background: #f8fafc;
}

.description-text {
  color: #475467;
  font-size: 12px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-description {
  min-height: 40px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #98a2b3;
  font-size: 12px;
}

.review-section {
  margin-top: 22px;
}

.review-section-icon {
  background: #f1f3f6;
  color: #667085;
}

.review-card {
  padding: 13px 14px;
  border: 1px solid #e6ebf1;
  border-radius: 11px;
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
  color: #98a2b3;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.review-value {
  color: #344054;
  font-size: 12px;
  font-weight: 600;
  text-align: right;
}

.review-remarks {
  margin-top: 9px;
  padding-top: 11px;
  border-top: 1px solid #e2e8f0;
}

.remarks-text {
  margin-top: 5px;
  color: #475467;
  font-size: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.dialog-footer {
  min-height: 62px;
  padding: 10px 18px;
  background: #ffffff;
}

.dialog-footer :deep(.q-btn) {
  min-height: 36px;
  border-radius: 8px;
}

@media (max-width: 650px) {
  .leave-details-card {
    max-width: 96vw;
    max-height: 92vh;
    border-radius: 15px;
  }

  .dialog-header {
    padding: 14px;
  }

  .dialog-content {
    padding: 14px;
  }

  .employee-card {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .employee-info {
    max-width: calc(100% - 72px);
  }

  .employee-status {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 5px;
    padding-top: 10px;
    border-top: 1px solid #e4e9f0;
    text-align: left;
  }

  .status-label {
    margin-bottom: 0;
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
    padding: 9px 12px;
  }
}

@media (max-width: 430px) {
  .dialog-title {
    font-size: 15px;
  }

  .dialog-subtitle {
    font-size: 10px;
  }

  .header-icon {
    width: 40px;
    height: 40px;
  }

  .dialog-footer {
    flex-wrap: wrap;
  }
}

.body--dark .leave-details-card {
  background: #18212f;
}

.body--dark .dialog-header,
.body--dark .dialog-footer {
  background: #18212f;
}

.body--dark .dialog-title {
  color: #f1f5f9;
}

.body--dark .dialog-subtitle,
.body--dark .employee-meta,
.body--dark .section-subtitle,
.body--dark .status-label,
.body--dark .info-label,
.body--dark .review-label,
.body--dark .empty-description {
  color: #94a3b8;
}

.body--dark .header-icon {
  background: #172554;
  color: #60a5fa;
}

.body--dark .employee-card,
.body--dark .description-box,
.body--dark .review-card {
  background: #202a38;
  border-color: #303b4d;
}

.body--dark .employee-name,
.body--dark .section-title,
.body--dark .info-value,
.body--dark .review-value {
  color: #e5e7eb;
}

.body--dark .employee-avatar {
  background: #172554;
  color: #60a5fa;
}

.body--dark .section-icon {
  background: #172554;
  color: #60a5fa;
}

.body--dark .info-box {
  background: #18212f;
  border-color: #303b4d;
}

.body--dark .info-icon {
  background: #202a38;
  color: #94a3b8;
}

.body--dark .description-text,
.body--dark .remarks-text {
  color: #cbd5e1;
}

.body--dark .review-section-icon {
  background: #252d38;
  color: #94a3b8;
}

.body--dark .review-remarks {
  border-color: #303b4d;
}

.body--dark .employee-status {
  border-color: #303b4d;
}
</style>
