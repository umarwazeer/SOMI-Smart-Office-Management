<template>
  <q-page class="intelligence-page q-pa-md q-pa-lg-xl">
    <!-- Header -->
    <section class="page-header q-mb-lg">
      <div>
        <div class="eyebrow">
          <q-icon name="auto_awesome" size="16px" />
          SOMI INTELLIGENCE
        </div>

        <h1 class="page-title">
          Office Intelligence
        </h1>

        <p class="page-subtitle">
          Understand your office through real-time workforce,
          attendance, leave, task, performance and payroll insights.
        </p>
      </div>

      <div class="header-actions">
        <q-chip
          outline
          icon="schedule"
          color="primary"
          class="period-chip"
        >
          Last {{ analysisDays }} Days
        </q-chip>

        <q-btn
          unelevated
          no-caps
          icon="refresh"
          label="Refresh Intelligence"
          color="primary"
          :loading="loading"
          @click="loadIntelligence"
        />
      </div>
    </section>

    <!-- Error -->
    <q-banner
      v-if="errorMessage"
      rounded
      class="error-banner q-mb-lg"
      icon="error_outline"
    >
      <div class="text-weight-medium">
        Intelligence data could not be loaded.
      </div>

      <div class="text-caption q-mt-xs">
        {{ errorMessage }}
      </div>

      <template v-slot:action>
        <q-btn
          flat
          no-caps
          label="Retry"
          @click="loadIntelligence"
        />
      </template>
    </q-banner>

    <!-- Loading -->
    <template v-if="loading && !intelligence">
      <div class="row q-col-gutter-md">
        <div
          v-for="index in 4"
          :key="index"
          class="col-12 col-sm-6 col-lg-3"
        >
          <q-skeleton
            type="rect"
            height="132px"
            class="skeleton-card"
          />
        </div>
      </div>

      <div class="row q-col-gutter-lg q-mt-sm">
        <div class="col-12 col-lg-8">
          <q-skeleton
            type="rect"
            height="350px"
            class="skeleton-card"
          />
        </div>

        <div class="col-12 col-lg-4">
          <q-skeleton
            type="rect"
            height="350px"
            class="skeleton-card"
          />
        </div>
      </div>
    </template>

    <template v-else-if="intelligence">
      <!-- Overview Cards -->
      <section class="overview-grid q-mb-lg">
        <div
          v-for="card in overviewCards"
          :key="card.key"
          class="overview-card"
          :class="`overview-${card.tone}`"
        >
          <div class="card-icon">
            <q-icon
              :name="card.icon"
              size="24px"
            />
          </div>

          <div class="card-content">
            <div class="card-label">
              {{ card.label }}
            </div>

            <div class="card-value">
              {{ formatNumber(card.value) }}
            </div>

            <div class="card-description">
              {{ card.description }}
            </div>
          </div>
        </div>
      </section>

      <!-- Intelligence Status -->
      <section class="intelligence-status q-mb-lg">
        <div class="status-left">
          <div class="status-icon">
            <q-icon name="psychology" size="25px" />
          </div>

          <div>
            <div class="status-title">
              SOMI Intelligence Engine
            </div>

            <div class="status-description">
              Deterministic analysis is active across your office data.
            </div>
          </div>
        </div>

        <div class="status-right">
          <q-badge
            color="positive"
            rounded
            class="status-badge"
          >
            <q-icon name="check_circle" size="14px" class="q-mr-xs" />
            ANALYSIS ACTIVE
          </q-badge>

          <span class="generated-time">
            Updated {{ generatedTime }}
          </span>
        </div>
      </section>

      <!-- Visual Intelligence -->
      <div class="row q-col-gutter-lg q-mb-lg">
        <!-- Attendance Chart -->
        <div class="col-12 col-lg-6">
          <section class="intelligence-card chart-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  WORKFORCE
                </div>

                <h2>
                  Attendance Distribution
                </h2>

                <p>
                  Workforce attendance distribution during the selected period.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon attendance-icon"
              >
                <q-icon name="donut_large" size="24px" />
              </q-avatar>
            </div>

            <div class="chart-wrapper doughnut-chart-wrapper">
              <canvas ref="attendanceChart"></canvas>
            </div>

            <div class="chart-footer-stats">
              <div>
                <span>Attendance Rate</span>
                <strong>
                  {{ formatPercent(attendance.attendance_rate) }}
                </strong>
              </div>

              <div>
                <span>Total Records</span>
                <strong>
                  {{ attendanceTotal }}
                </strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Task Chart -->
        <div class="col-12 col-lg-6">
          <section class="intelligence-card chart-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  PRODUCTIVITY
                </div>

                <h2>
                  Task Status Overview
                </h2>

                <p>
                  Current task distribution across the office.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon task-icon"
              >
                <q-icon name="bar_chart" size="24px" />
              </q-avatar>
            </div>

            <div class="chart-wrapper doughnut-chart-wrapper">
              <canvas ref="taskChart"></canvas>
            </div>

            <div class="chart-footer-stats">
              <div>
                <span>Completion Rate</span>
                <strong>
                  {{ formatPercent(tasks.completion_rate) }}
                </strong>
              </div>

              <div>
                <span>High Priority Open</span>
                <strong>
                  {{ tasks.high_priority_open }}
                </strong>
              </div>

              <div>
                <span>Overdue</span>
                <strong>
                  {{ tasks.overdue }}
                </strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Leave Chart -->
        <div class="col-12 col-lg-6">
          <section class="intelligence-card chart-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  TIME OFF
                </div>

                <h2>
                  Leave by Department
                </h2>

                <p>
                  Approved leave days distributed across departments.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon leave-icon"
              >
                <q-icon name="event_available" size="23px" />
              </q-avatar>
            </div>

            <div
              v-if="leave.department_breakdown.length"
              class="chart-wrapper bar-chart-wrapper"
            >
              <canvas ref="leaveChart"></canvas>
            </div>

            <div
              v-else
              class="chart-empty"
            >
              <q-icon name="event_available" size="38px" />
              <span>No department leave data available.</span>
            </div>

            <div class="chart-footer-stats">
              <div>
                <span>Total Requests</span>
                <strong>{{ leave.total_requests }}</strong>
              </div>

              <div>
                <span>Approved</span>
                <strong>{{ leave.approved }}</strong>
              </div>

              <div>
                <span>Leave Days</span>
                <strong>{{ leave.approved_leave_days }}</strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Performance Chart -->
        <div class="col-12 col-lg-6">
          <section class="intelligence-card chart-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  PEOPLE
                </div>

                <h2>
                  Performance Profile
                </h2>

                <p>
                  Average scores across key performance dimensions.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon performance-icon"
              >
                <q-icon name="radar" size="23px" />
              </q-avatar>
            </div>

            <div class="chart-wrapper radar-chart-wrapper">
              <canvas ref="performanceChart"></canvas>
            </div>

            <div class="chart-footer-stats">
              <div>
                <span>Average Rating</span>
                <strong>
                  {{ performanceAverage }} / 5
                </strong>
              </div>

              <div>
                <span>Total Reviews</span>
                <strong>
                  {{ performance.total_reviews }}
                </strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Payroll Chart -->
        <div
          v-if="payroll.available"
          class="col-12"
        >
          <section class="intelligence-card chart-card payroll-chart-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  FINANCE
                </div>

                <h2>
                  Payroll Cost by Department
                </h2>

                <p>
                  Department-level payroll distribution for authorized users.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon payroll-icon"
              >
                <q-icon name="payments" size="23px" />
              </q-avatar>
            </div>

            <div
              v-if="payroll.department_breakdown.length"
              class="chart-wrapper payroll-bar-wrapper"
            >
              <canvas ref="payrollChart"></canvas>
            </div>

            <div
              v-else
              class="chart-empty"
            >
              <q-icon name="payments" size="38px" />
              <span>No department payroll data available.</span>
            </div>

            <div class="payroll-total-footer">
              <span>Total Payroll</span>

              <strong>
                {{ formatCurrency(payroll.total_salary) }}
              </strong>
            </div>
          </section>
        </div>
      </div>

      <!-- Main Intelligence -->
      <div class="row q-col-gutter-lg">
        <!-- Attendance Intelligence -->
        <div class="col-12 col-lg-8">
          <section class="intelligence-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  WORKFORCE
                </div>

                <h2>
                  Attendance Intelligence
                </h2>

                <p>
                  Attendance patterns detected during the selected period.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon attendance-icon"
              >
                <q-icon name="fact_check" size="24px" />
              </q-avatar>
            </div>

            <div class="metric-row">
              <div class="metric-box">
                <span class="metric-label">Attendance Rate</span>
                <strong>
                  {{ formatPercent(attendance.attendance_rate) }}
                </strong>
              </div>

              <div class="metric-box">
                <span class="metric-label">Present</span>
                <strong>
                  {{ attendance.present }}
                </strong>
              </div>

              <div class="metric-box">
                <span class="metric-label">Late</span>
                <strong>
                  {{ attendance.late }}
                </strong>
              </div>

              <div class="metric-box">
                <span class="metric-label">Absent</span>
                <strong>
                  {{ attendance.absent }}
                </strong>
              </div>
            </div>

            <div class="progress-section">
              <div class="progress-heading">
                <span>Attendance performance</span>
                <strong>
                  {{ formatPercent(attendance.attendance_rate) }}
                </strong>
              </div>

              <q-linear-progress
                rounded
                size="10px"
                :value="attendance.attendance_rate / 100"
                color="primary"
                track-color="grey-3"
              />
            </div>

            <div
              v-if="attendance.department_breakdown.length"
              class="breakdown-section"
            >
              <div class="breakdown-title">
                Department Breakdown
              </div>

              <div
                v-for="department in attendance.department_breakdown"
                :key="`attendance-${department.department_id}`"
                class="breakdown-row"
              >
                <div class="breakdown-name">
                  <span>
                    {{ department.department_name }}
                  </span>

                  <small>
                    {{ department.attendance_records }} records
                  </small>
                </div>

                <div class="breakdown-values">
                  <q-badge
                    color="negative"
                    outline
                  >
                    {{ department.absent }} absent
                  </q-badge>

                  <q-badge
                    color="warning"
                    outline
                  >
                    {{ department.late }} late
                  </q-badge>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Smart Alerts -->
        <div class="col-12 col-lg-4">
          <section class="intelligence-card alerts-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  MONITORING
                </div>

                <h2>
                  Smart Alerts
                </h2>

                <p>
                  Items that may need attention.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon alert-icon"
              >
                <q-icon name="notifications_active" size="23px" />
              </q-avatar>
            </div>

            <div
              v-if="smartAlerts.length"
              class="alerts-list"
            >
              <div
                v-for="(alert, index) in smartAlerts"
                :key="`${alert.type}-${index}`"
                class="alert-item"
                :class="`alert-${String(alert.severity).toLowerCase()}`"
              >
                <div class="alert-indicator">
                  <q-icon
                    :name="alertIcon(alert.type)"
                    size="18px"
                  />
                </div>

                <div class="alert-content">
                  <div class="alert-top">
                    <span>
                      {{ alert.type }}
                    </span>

                    <q-badge
                      :color="severityColor(alert.severity)"
                      outline
                    >
                      {{ alert.severity }}
                    </q-badge>
                  </div>

                  <div class="alert-message">
                    {{ alert.message }}
                  </div>
                </div>
              </div>
            </div>

            <div
              v-else
              class="empty-state"
            >
              <q-icon
                name="verified"
                size="40px"
              />

              <div class="empty-title">
                No active alerts
              </div>

              <div class="empty-text">
                SOMI did not detect any items requiring attention.
              </div>
            </div>
          </section>
        </div>

        <!-- Leave -->
        <div class="col-12 col-md-6">
          <section class="intelligence-card compact-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  TIME OFF
                </div>

                <h2>
                  Leave Intelligence
                </h2>
              </div>

              <q-avatar
                square
                size="44px"
                class="section-icon leave-icon"
              >
                <q-icon name="event_available" size="22px" />
              </q-avatar>
            </div>

            <div class="mini-stats">
              <div>
                <span>Total Requests</span>
                <strong>{{ leave.total_requests }}</strong>
              </div>

              <div>
                <span>Pending</span>
                <strong>{{ leave.pending }}</strong>
              </div>

              <div>
                <span>Approved</span>
                <strong>{{ leave.approved }}</strong>
              </div>

              <div>
                <span>Leave Days</span>
                <strong>{{ leave.approved_leave_days }}</strong>
              </div>
            </div>

            <div class="progress-section compact-progress">
              <div class="progress-heading">
                <span>Approval rate</span>
                <strong>
                  {{ formatPercent(leave.approval_rate) }}
                </strong>
              </div>

              <q-linear-progress
                rounded
                size="8px"
                :value="leave.approval_rate / 100"
                color="positive"
                track-color="grey-3"
              />
            </div>

            <div
              v-if="leave.department_breakdown.length"
              class="compact-breakdown"
            >
              <div
                v-for="department in leave.department_breakdown.slice(0, 4)"
                :key="`leave-${department.department_id}`"
                class="compact-row"
              >
                <span>
                  {{ department.department_name }}
                </span>

                <strong>
                  {{ department.leave_days }} days
                </strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Tasks -->
        <div class="col-12 col-md-6">
          <section class="intelligence-card compact-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  PRODUCTIVITY
                </div>

                <h2>
                  Task Intelligence
                </h2>
              </div>

              <q-avatar
                square
                size="44px"
                class="section-icon task-icon"
              >
                <q-icon name="task_alt" size="22px" />
              </q-avatar>
            </div>

            <div class="mini-stats">
              <div>
                <span>Total</span>
                <strong>{{ tasks.total }}</strong>
              </div>

              <div>
                <span>Completed</span>
                <strong>{{ tasks.completed }}</strong>
              </div>

              <div>
                <span>In Progress</span>
                <strong>{{ tasks.in_progress }}</strong>
              </div>

              <div>
                <span>Overdue</span>
                <strong>{{ tasks.overdue }}</strong>
              </div>
            </div>

            <div class="progress-section compact-progress">
              <div class="progress-heading">
                <span>Completion rate</span>
                <strong>
                  {{ formatPercent(tasks.completion_rate) }}
                </strong>
              </div>

              <q-linear-progress
                rounded
                size="8px"
                :value="tasks.completion_rate / 100"
                color="primary"
                track-color="grey-3"
              />
            </div>

            <div class="task-summary">
              <div>
                <q-icon name="priority_high" size="17px" />
                <span>
                  {{ tasks.high_priority_open }} high-priority open
                </span>
              </div>

              <div>
                <q-icon name="pending_actions" size="17px" />
                <span>
                  {{ tasks.todo }} waiting to start
                </span>
              </div>
            </div>
          </section>
        </div>

        <!-- Performance -->
        <div class="col-12 col-md-6">
          <section class="intelligence-card compact-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  PEOPLE
                </div>

                <h2>
                  Performance Intelligence
                </h2>
              </div>

              <q-avatar
                square
                size="44px"
                class="section-icon performance-icon"
              >
                <q-icon name="trending_up" size="22px" />
              </q-avatar>
            </div>

            <div class="performance-main">
              <div class="rating-circle">
                <strong>
                  {{ performanceAverage }}
                </strong>

                <span>
                  / 5
                </span>
              </div>

              <div>
                <div class="performance-title">
                  Average Performance Rating
                </div>

                <div class="performance-subtitle">
                  Based on {{ performance.total_reviews }} review(s)
                </div>
              </div>
            </div>

            <div class="score-grid">
              <div>
                <span>Goals</span>
                <strong>
                  {{ formatScore(performance.average_scores.goals_score) }}
                </strong>
              </div>

              <div>
                <span>Productivity</span>
                <strong>
                  {{ formatScore(performance.average_scores.productivity_score) }}
                </strong>
              </div>

              <div>
                <span>Quality</span>
                <strong>
                  {{ formatScore(performance.average_scores.quality_score) }}
                </strong>
              </div>

              <div>
                <span>Teamwork</span>
                <strong>
                  {{ formatScore(performance.average_scores.teamwork_score) }}
                </strong>
              </div>
            </div>

            <div class="review-status">
              <q-chip
                dense
                outline
                color="warning"
              >
                {{ performance.draft }} Draft
              </q-chip>

              <q-chip
                dense
                outline
                color="primary"
              >
                {{ performance.submitted }} Submitted
              </q-chip>

              <q-chip
                dense
                outline
                color="positive"
              >
                {{ performance.acknowledged }} Acknowledged
              </q-chip>
            </div>
          </section>
        </div>

        <!-- Payroll -->
        <div
          v-if="payroll.available"
          class="col-12 col-md-6"
        >
          <section class="intelligence-card compact-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  FINANCE
                </div>

                <h2>
                  Payroll Intelligence
                </h2>
              </div>

              <q-avatar
                square
                size="44px"
                class="section-icon payroll-icon"
              >
                <q-icon name="payments" size="22px" />
              </q-avatar>
            </div>

            <div class="payroll-total">
              <span>Total Payroll</span>

              <strong>
                {{ formatCurrency(payroll.total_salary) }}
              </strong>
            </div>

            <div class="payroll-grid">
              <div>
                <span>Basic Salary</span>
                <strong>
                  {{ formatCurrency(payroll.basic_salary) }}
                </strong>
              </div>

              <div>
                <span>Allowances</span>
                <strong>
                  {{ formatCurrency(payroll.allowances) }}
                </strong>
              </div>

              <div>
                <span>Deductions</span>
                <strong>
                  {{ formatCurrency(payroll.deductions) }}
                </strong>
              </div>

              <div>
                <span>Records</span>
                <strong>
                  {{ payroll.total_records }}
                </strong>
              </div>
            </div>

            <div
              v-if="payroll.department_breakdown.length"
              class="compact-breakdown"
            >
              <div
                v-for="department in payroll.department_breakdown.slice(0, 4)"
                :key="`payroll-${department.department_id}`"
                class="compact-row"
              >
                <span>
                  {{ department.department_name }}
                </span>

                <strong>
                  {{ formatCurrency(department.payroll_cost) }}
                </strong>
              </div>
            </div>
          </section>
        </div>

        <!-- Workload -->
        <div class="col-12">
          <section class="intelligence-card">
            <div class="section-heading">
              <div>
                <div class="section-kicker">
                  WORKLOAD
                </div>

                <h2>
                  Employee Task Workload
                </h2>

                <p>
                  Current task distribution across assigned employees.
                </p>
              </div>

              <q-avatar
                square
                size="46px"
                class="section-icon workload-icon"
              >
                <q-icon name="groups" size="24px" />
              </q-avatar>
            </div>

            <div
              v-if="tasks.workload.length"
              class="workload-list"
            >
              <div
                v-for="employee in tasks.workload"
                :key="employee.employee_id"
                class="workload-row"
              >
                <div class="employee-info">
                  <q-avatar
                    size="38px"
                    color="primary"
                    text-color="white"
                  >
                    {{ employeeInitials(employee.employee_name) }}
                  </q-avatar>

                  <div>
                    <div class="employee-name">
                      {{ employee.employee_name }}
                    </div>

                    <div class="employee-code">
                      {{ employee.employee_code }}
                    </div>
                  </div>
                </div>

                <div class="workload-stats">
                  <div>
                    <span>Total Tasks</span>
                    <strong>
                      {{ employee.total_tasks }}
                    </strong>
                  </div>

                  <div>
                    <span>Open Tasks</span>
                    <strong>
                      {{ employee.open_tasks }}
                    </strong>
                  </div>

                  <div class="workload-progress">
                    <q-linear-progress
                      rounded
                      size="7px"
                      :value="workloadRatio(employee)"
                      color="primary"
                      track-color="grey-3"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div
              v-else
              class="empty-state workload-empty"
            >
              <q-icon
                name="assignment_turned_in"
                size="40px"
              />

              <div class="empty-title">
                No assigned tasks yet
              </div>

              <div class="empty-text">
                Employee workload data will appear here when tasks are assigned.
              </div>
            </div>
          </section>
        </div>
      </div>
    </template>
  </q-page>
</template>

<script>
import api from 'src/services/api'
import {
  Chart,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  RadialLinearScale,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

Chart.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  RadialLinearScale,
  Tooltip,
  Legend,
  Filler
)

export default {
  name: 'IntelligenceDashboard',

  data () {
    return {
      loading: false,
      intelligence: null,
      errorMessage: '',
      analysisDays: 30,

      attendanceChartInstance: null,
      taskChartInstance: null,
      leaveChartInstance: null,
      performanceChartInstance: null,
      payrollChartInstance: null
    }
  },

  computed: {
    overview () {
      return this.intelligence?.overview || {}
    },

    attendance () {
      return this.intelligence?.attendance || {
        attendance_rate: 0,
        present: 0,
        late: 0,
        absent: 0,
        on_leave: 0,
        department_breakdown: []
      }
    },

    leave () {
      return this.intelligence?.leave || {
        total_requests: 0,
        pending: 0,
        approved: 0,
        approved_leave_days: 0,
        approval_rate: 0,
        department_breakdown: []
      }
    },

    tasks () {
      return this.intelligence?.tasks || {
        total: 0,
        completed: 0,
        in_progress: 0,
        overdue: 0,
        high_priority_open: 0,
        todo: 0,
        completion_rate: 0,
        workload: []
      }
    },

    performance () {
      return this.intelligence?.performance || {
        total_reviews: 0,
        draft: 0,
        submitted: 0,
        acknowledged: 0,
        average_scores: {
          rating: 0,
          goals_score: 0,
          productivity_score: 0,
          quality_score: 0,
          teamwork_score: 0,
          communication_score: 0
        }
      }
    },

    payroll () {
      return this.intelligence?.payroll || {
        available: false,
        total_records: 0,
        total_salary: 0,
        basic_salary: 0,
        allowances: 0,
        deductions: 0,
        department_breakdown: []
      }
    },

    smartAlerts () {
      return this.intelligence?.smart_alerts || []
    },

    generatedTime () {
      if (!this.intelligence?.generated_at) {
        return 'just now'
      }

      const date = new Date(this.intelligence.generated_at)

      if (Number.isNaN(date.getTime())) {
        return 'just now'
      }

      return date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    performanceAverage () {
      return this.formatScore(
        this.performance.average_scores?.rating
      )
    },

    attendanceTotal () {
      return (
        Number(this.attendance.present || 0) +
        Number(this.attendance.late || 0) +
        Number(this.attendance.absent || 0) +
        Number(this.attendance.on_leave || 0)
      )
    },

    overviewCards () {
      return [
        {
          key: 'employees',
          label: 'Employees',
          value: this.overview.employees || 0,
          description: 'Total workforce',
          icon: 'groups',
          tone: 'blue'
        },
        {
          key: 'departments',
          label: 'Departments',
          value: this.overview.departments || 0,
          description: 'Active office units',
          icon: 'business',
          tone: 'purple'
        },
        {
          key: 'pending-leaves',
          label: 'Pending Leaves',
          value: this.overview.pending_leaves || 0,
          description: 'Requests awaiting review',
          icon: 'event_busy',
          tone: 'orange'
        },
        {
          key: 'completed-tasks',
          label: 'Completed Tasks',
          value: this.overview.completed_tasks || 0,
          description: 'Successfully completed',
          icon: 'task_alt',
          tone: 'green'
        }
      ]
    }
  },

  mounted () {
    this.loadIntelligence()
  },

  beforeUnmount () {
    this.destroyCharts()
  },

  methods: {
    async loadIntelligence () {
      this.loading = true
      this.errorMessage = ''

      try {
        const response = await api.get('/intelligence/')

        this.intelligence = response.data

        await this.$nextTick()

        this.renderCharts()
      } catch (error) {
        console.error('Intelligence dashboard error:', error)

        this.errorMessage =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          'Unable to connect to the SOMI Intelligence API.'
      } finally {
        this.loading = false
      }
    },

    renderCharts () {
      this.destroyCharts()

      this.renderAttendanceChart()
      this.renderTaskChart()
      this.renderLeaveChart()
      this.renderPerformanceChart()
      this.renderPayrollChart()
    },

    destroyCharts () {
      const charts = [
        'attendanceChartInstance',
        'taskChartInstance',
        'leaveChartInstance',
        'performanceChartInstance',
        'payrollChartInstance'
      ]

      charts.forEach((chartName) => {
        if (this[chartName]) {
          this[chartName].destroy()
          this[chartName] = null
        }
      })
    },

    chartTextColor () {
      return this.$q.dark.isActive
        ? '#cbd5e1'
        : '#64748b'
    },

    chartGridColor () {
      return this.$q.dark.isActive
        ? '#263244'
        : '#e8edf5'
    },

    renderAttendanceChart () {
      const canvas = this.$refs.attendanceChart

      if (!canvas) {
        return
      }

      const data = [
        Number(this.attendance.present || 0),
        Number(this.attendance.late || 0),
        Number(this.attendance.absent || 0),
        Number(this.attendance.on_leave || 0)
      ]

      this.attendanceChartInstance = new Chart(canvas, {
        type: 'doughnut',

        data: {
          labels: [
            'Present',
            'Late',
            'Absent',
            'On Leave'
          ],

          datasets: [
            {
              data,
              backgroundColor: [
                '#22c55e',
                '#f59e0b',
                '#ef4444',
                '#8b5cf6'
              ],
              borderWidth: 0,
              hoverOffset: 5
            }
          ]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          cutout: '68%',

          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: this.chartTextColor(),
                usePointStyle: true,
                pointStyle: 'circle',
                padding: 16,
                font: {
                  size: 11
                }
              }
            },

            tooltip: {
              callbacks: {
                label: (context) => {
                  const value = context.raw || 0
                  return ` ${context.label}: ${value}`
                }
              }
            }
          }
        }
      })
    },

    renderTaskChart () {
      const canvas = this.$refs.taskChart

      if (!canvas) {
        return
      }

      const data = [
        Number(this.tasks.completed || 0),
        Number(this.tasks.in_progress || 0),
        Number(this.tasks.todo || 0),
        Number(this.tasks.overdue || 0)
      ]

      this.taskChartInstance = new Chart(canvas, {
        type: 'doughnut',

        data: {
          labels: [
            'Completed',
            'In Progress',
            'To Do',
            'Overdue'
          ],

          datasets: [
            {
              data,
              backgroundColor: [
                '#22c55e',
                '#3b82f6',
                '#94a3b8',
                '#ef4444'
              ],
              borderWidth: 0,
              hoverOffset: 5
            }
          ]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          cutout: '68%',

          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: this.chartTextColor(),
                usePointStyle: true,
                pointStyle: 'circle',
                padding: 15,
                font: {
                  size: 11
                }
              }
            }
          }
        }
      })
    },

    renderLeaveChart () {
      const canvas = this.$refs.leaveChart

      if (
        !canvas ||
        !this.leave.department_breakdown.length
      ) {
        return
      }

      const departments = this.leave.department_breakdown

      this.leaveChartInstance = new Chart(canvas, {
        type: 'bar',

        data: {
          labels: departments.map(
            department => department.department_name
          ),

          datasets: [
            {
              label: 'Approved Leave Days',

              data: departments.map(
                department => Number(department.leave_days || 0)
              ),

              backgroundColor: '#7257c7',
              borderRadius: 7,
              borderSkipped: false,
              barThickness: 24
            }
          ]
        },

        options: {
          indexAxis: 'y',

          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              display: false
            }
          },

          scales: {
            x: {
              beginAtZero: true,
              ticks: {
                color: this.chartTextColor(),
                font: {
                  size: 10
                },
                precision: 0
              },
              grid: {
                color: this.chartGridColor()
              }
            },

            y: {
              ticks: {
                color: this.chartTextColor(),
                font: {
                  size: 10
                }
              },
              grid: {
                display: false
              }
            }
          }
        }
      })
    },

    renderPerformanceChart () {
      const canvas = this.$refs.performanceChart

      if (!canvas) {
        return
      }

      const scores = this.performance.average_scores || {}

      this.performanceChartInstance = new Chart(canvas, {
        type: 'radar',

        data: {
          labels: [
            'Goals',
            'Productivity',
            'Quality',
            'Teamwork',
            'Communication'
          ],

          datasets: [
            {
              label: 'Average Score',

              data: [
                Number(scores.goals_score || 0),
                Number(scores.productivity_score || 0),
                Number(scores.quality_score || 0),
                Number(scores.teamwork_score || 0),
                Number(scores.communication_score || 0)
              ],

              borderColor: '#168653',
              backgroundColor: 'rgba(22, 134, 83, 0.14)',
              pointBackgroundColor: '#168653',
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: 4,
              borderWidth: 2
            }
          ]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          scales: {
            r: {
              min: 0,
              max: 5,
              ticks: {
                stepSize: 1,
                color: this.chartTextColor(),
                backdropColor: 'transparent',
                font: {
                  size: 9
                }
              },

              angleLines: {
                color: this.chartGridColor()
              },

              grid: {
                color: this.chartGridColor()
              },

              pointLabels: {
                color: this.chartTextColor(),
                font: {
                  size: 10,
                  weight: '600'
                }
              }
            }
          },

          plugins: {
            legend: {
              display: false
            }
          }
        }
      })
    },

    renderPayrollChart () {
      const canvas = this.$refs.payrollChart

      if (
        !canvas ||
        !this.payroll.department_breakdown.length
      ) {
        return
      }

      const departments = this.payroll.department_breakdown

      this.payrollChartInstance = new Chart(canvas, {
        type: 'bar',

        data: {
          labels: departments.map(
            department => department.department_name
          ),

          datasets: [
            {
              label: 'Payroll Cost',

              data: departments.map(
                department => Number(department.payroll_cost || 0)
              ),

              backgroundColor: '#d98213',
              borderRadius: 7,
              borderSkipped: false,
              barThickness: 25
            }
          ]
        },

        options: {
          indexAxis: 'y',

          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              display: false
            },

            tooltip: {
              callbacks: {
                label: (context) => {
                  return ` Rs. ${new Intl.NumberFormat('en-PK', {
                    maximumFractionDigits: 0
                  }).format(context.raw || 0)}`
                }
              }
            }
          },

          scales: {
            x: {
              beginAtZero: true,

              ticks: {
                color: this.chartTextColor(),

                font: {
                  size: 10
                },

                callback: (value) => {
                  return `Rs. ${new Intl.NumberFormat('en-PK', {
                    notation: 'compact',
                    maximumFractionDigits: 1
                  }).format(value)}`
                }
              },

              grid: {
                color: this.chartGridColor()
              }
            },

            y: {
              ticks: {
                color: this.chartTextColor(),
                font: {
                  size: 10
                }
              },

              grid: {
                display: false
              }
            }
          }
        }
      })
    },

    formatNumber (value) {
      const number = Number(value || 0)

      return new Intl.NumberFormat().format(number)
    },

    formatPercent (value) {
      const number = Number(value || 0)

      return `${number.toFixed(1)}%`
    },

    formatScore (value) {
      const number = Number(value || 0)

      return number.toFixed(2)
    },

    formatCurrency (value) {
      const number = Number(value || 0)

      return `Rs. ${new Intl.NumberFormat('en-PK', {
        maximumFractionDigits: 0
      }).format(number)}`
    },

    severityColor (severity) {
      const value = String(severity || '').toUpperCase()

      if (value === 'HIGH') {
        return 'negative'
      }

      if (value === 'MEDIUM') {
        return 'warning'
      }

      return 'primary'
    },

    alertIcon (type) {
      const icons = {
        ATTENDANCE: 'schedule',
        LEAVE: 'event_busy',
        TASK: 'assignment_late',
        PERFORMANCE: 'trending_up',
        PAYROLL: 'payments'
      }

      return icons[String(type || '').toUpperCase()] || 'info'
    },

    employeeInitials (name) {
      if (!name) {
        return 'EM'
      }

      const parts = String(name)
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (parts.length === 1) {
        return parts[0].substring(0, 2).toUpperCase()
      }

      return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    },

    workloadRatio (employee) {
      const total = Number(employee.total_tasks || 0)
      const open = Number(employee.open_tasks || 0)

      if (!total) {
        return 0
      }

      return Math.min(open / total, 1)
    }
  }
}
</script>

<style scoped>
.intelligence-page {
  min-height: 100vh;
  background: #f6f8fc;
  color: #1e293b;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.eyebrow,
.section-kicker {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #225dcc;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.2px;
}

.page-title {
  margin: 7px 0 5px;
  font-size: 31px;
  line-height: 1.15;
  font-weight: 800;
  color: #172033;
}

.page-subtitle {
  margin: 0;
  max-width: 760px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.period-chip {
  background: #ffffff;
}

.error-banner {
  background: #fff5f5;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.skeleton-card {
  border-radius: 18px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.overview-card {
  min-height: 132px;
  padding: 20px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid #e8edf5;
  box-shadow: 0 7px 22px rgba(30, 41, 59, 0.055);
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.overview-blue .card-icon {
  background: #eaf2ff;
  color: #225dcc;
}

.overview-purple .card-icon {
  background: #f2edff;
  color: #7257c7;
}

.overview-orange .card-icon {
  background: #fff4e5;
  color: #d98213;
}

.overview-green .card-icon {
  background: #eaf9f1;
  color: #168653;
}

.card-label {
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
}

.card-value {
  margin-top: 4px;
  color: #172033;
  font-size: 28px;
  line-height: 1.1;
  font-weight: 800;
}

.card-description {
  margin-top: 5px;
  color: #94a3b8;
  font-size: 11px;
}

.intelligence-status {
  min-height: 74px;
  padding: 15px 18px;
  border: 1px solid #dce8f8;
  border-radius: 17px;
  background: linear-gradient(90deg, #f4f8ff, #ffffff);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.status-left,
.status-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-icon {
  width: 44px;
  height: 44px;
  border-radius: 13px;
  background: #e8f0ff;
  color: #225dcc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-title {
  color: #172033;
  font-size: 14px;
  font-weight: 750;
}

.status-description,
.generated-time {
  color: #7b8799;
  font-size: 11px;
}

.status-badge {
  padding: 7px 10px;
  font-size: 10px;
  letter-spacing: 0.5px;
}

.intelligence-card {
  height: 100%;
  padding: 22px;
  border-radius: 19px;
  background: #ffffff;
  border: 1px solid #e8edf5;
  box-shadow: 0 7px 22px rgba(30, 41, 59, 0.05);
}

.chart-card {
  min-height: 410px;
}

.compact-card {
  min-height: 100%;
}

.section-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.section-heading h2 {
  margin: 5px 0 4px;
  color: #172033;
  font-size: 18px;
  font-weight: 780;
}

.section-heading p {
  margin: 0;
  color: #8490a3;
  font-size: 11px;
  line-height: 1.5;
}

.section-icon {
  border-radius: 13px;
  flex-shrink: 0;
}

.attendance-icon {
  background: #eaf2ff;
  color: #225dcc;
}

.alert-icon {
  background: #fff3e7;
  color: #d98213;
}

.leave-icon {
  background: #f0edff;
  color: #7257c7;
}

.task-icon {
  background: #eaf2ff;
  color: #225dcc;
}

.performance-icon {
  background: #eaf8f0;
  color: #168653;
}

.payroll-icon {
  background: #fff3e7;
  color: #c9780e;
}

.workload-icon {
  background: #edf2f8;
  color: #526276;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  margin-top: 12px;
}

.doughnut-chart-wrapper {
  height: 245px;
}

.bar-chart-wrapper {
  height: 220px;
  margin-top: 18px;
}

.radar-chart-wrapper {
  height: 245px;
}

.payroll-bar-wrapper {
  height: 230px;
  margin-top: 18px;
}

.chart-footer-stats {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chart-footer-stats > div {
  flex: 1;
  min-width: 120px;
  padding: 9px 11px;
  border-radius: 10px;
  background: #f7f9fc;
  border: 1px solid #edf1f6;
}

.chart-footer-stats span {
  display: block;
  color: #8995a7;
  font-size: 9px;
}

.chart-footer-stats strong {
  display: block;
  margin-top: 3px;
  color: #334155;
  font-size: 13px;
}

.chart-empty {
  height: 275px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  gap: 8px;
  font-size: 11px;
}

.payroll-chart-card {
  min-height: 400px;
}

.payroll-total-footer {
  margin-top: 8px;
  padding: 12px 14px;
  border-radius: 11px;
  background: #fff8ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.payroll-total-footer span {
  color: #8995a7;
  font-size: 10px;
}

.payroll-total-footer strong {
  color: #c9780e;
  font-size: 14px;
  font-weight: 800;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 22px;
}

.metric-box {
  padding: 13px;
  border-radius: 12px;
  background: #f7f9fc;
  border: 1px solid #edf1f6;
}

.metric-label {
  display: block;
  color: #7c899b;
  font-size: 10px;
  font-weight: 600;
}

.metric-box strong {
  display: block;
  margin-top: 5px;
  color: #172033;
  font-size: 20px;
}

.progress-section {
  margin-top: 19px;
}

.progress-heading {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
  color: #64748b;
  font-size: 11px;
}

.progress-heading strong {
  color: #334155;
}

.breakdown-section {
  margin-top: 22px;
}

.breakdown-title {
  margin-bottom: 10px;
  color: #334155;
  font-size: 12px;
  font-weight: 750;
}

.breakdown-row {
  min-height: 48px;
  padding: 8px 0;
  border-bottom: 1px solid #eef1f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.breakdown-row:last-child {
  border-bottom: none;
}

.breakdown-name span {
  display: block;
  color: #334155;
  font-size: 12px;
  font-weight: 650;
}

.breakdown-name small {
  display: block;
  margin-top: 2px;
  color: #94a3b8;
  font-size: 10px;
}

.breakdown-values {
  display: flex;
  gap: 5px;
}

.alerts-list {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  padding: 11px;
  border-radius: 12px;
  display: flex;
  gap: 10px;
  border: 1px solid #edf1f5;
  background: #fafbfd;
}

.alert-high {
  border-color: #ffd6d6;
  background: #fff8f8;
}

.alert-medium {
  border-color: #ffe5c0;
  background: #fffaf3;
}

.alert-indicator {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #edf2f8;
  color: #526276;
  flex-shrink: 0;
}

.alert-high .alert-indicator {
  background: #feeaea;
  color: #dc2626;
}

.alert-medium .alert-indicator {
  background: #fff0d9;
  color: #c9780e;
}

.alert-content {
  min-width: 0;
  flex: 1;
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: #526276;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.7px;
}

.alert-message {
  margin-top: 5px;
  color: #475569;
  font-size: 11px;
  line-height: 1.5;
}

.empty-state {
  min-height: 210px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #94a3b8;
}

.empty-title {
  margin-top: 10px;
  color: #475569;
  font-size: 13px;
  font-weight: 700;
}

.empty-text {
  max-width: 260px;
  margin-top: 4px;
  color: #94a3b8;
  font-size: 11px;
  line-height: 1.5;
}

.mini-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-top: 21px;
}

.mini-stats > div {
  padding: 11px;
  border-radius: 11px;
  background: #f7f9fc;
}

.mini-stats span,
.score-grid span,
.payroll-grid span {
  display: block;
  color: #8995a7;
  font-size: 9px;
}

.mini-stats strong,
.score-grid strong,
.payroll-grid strong {
  display: block;
  margin-top: 4px;
  color: #334155;
  font-size: 15px;
}

.compact-progress {
  margin-top: 16px;
}

.compact-breakdown {
  margin-top: 17px;
}

.compact-row {
  padding: 8px 0;
  border-bottom: 1px solid #eef1f5;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  color: #64748b;
  font-size: 11px;
}

.compact-row:last-child {
  border-bottom: none;
}

.compact-row strong {
  color: #334155;
}

.task-summary {
  margin-top: 17px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.task-summary > div {
  padding: 7px 9px;
  border-radius: 9px;
  background: #f7f9fc;
  color: #64748b;
  font-size: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.performance-main {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.rating-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #edf9f3;
  color: #168653;
  display: flex;
  align-items: baseline;
  justify-content: center;
  padding-top: 23px;
  flex-shrink: 0;
}

.rating-circle strong {
  font-size: 21px;
  font-weight: 800;
}

.rating-circle span {
  font-size: 10px;
  margin-left: 2px;
}

.performance-title {
  color: #334155;
  font-size: 12px;
  font-weight: 700;
}

.performance-subtitle {
  margin-top: 4px;
  color: #94a3b8;
  font-size: 10px;
}

.score-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 7px;
}

.score-grid > div {
  padding: 9px;
  border-radius: 10px;
  background: #f7f9fc;
}

.review-status {
  margin-top: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.review-status .q-chip {
  font-size: 9px;
}

.payroll-total {
  margin-top: 20px;
  padding: 15px;
  border-radius: 13px;
  background: #f7f9fc;
}

.payroll-total span {
  display: block;
  color: #8995a7;
  font-size: 10px;
}

.payroll-total strong {
  display: block;
  margin-top: 4px;
  color: #172033;
  font-size: 24px;
  font-weight: 800;
}

.payroll-grid {
  margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 7px;
}

.payroll-grid > div {
  padding: 9px;
  border-radius: 10px;
  background: #fafbfd;
  border: 1px solid #edf1f5;
}

.workload-list {
  margin-top: 19px;
}

.workload-row {
  padding: 13px 0;
  border-bottom: 1px solid #edf1f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.workload-row:last-child {
  border-bottom: none;
}

.employee-info {
  min-width: 230px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.employee-name {
  color: #334155;
  font-size: 12px;
  font-weight: 700;
}

.employee-code {
  margin-top: 2px;
  color: #94a3b8;
  font-size: 10px;
}

.workload-stats {
  flex: 1;
  display: grid;
  grid-template-columns: 100px 100px minmax(160px, 1fr);
  align-items: center;
  gap: 18px;
}

.workload-stats > div:not(.workload-progress) span {
  display: block;
  color: #94a3b8;
  font-size: 9px;
}

.workload-stats > div:not(.workload-progress) strong {
  display: block;
  margin-top: 3px;
  color: #334155;
  font-size: 13px;
}

.workload-progress {
  min-width: 120px;
}

.workload-empty {
  min-height: 160px;
}

@media (max-width: 1100px) {
  .overview-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 700px) {
  .intelligence-page {
    padding: 14px !important;
  }

  .page-title {
    font-size: 25px;
  }

  .page-subtitle {
    font-size: 12px;
  }

  .header-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .period-chip {
    justify-content: center;
  }

  .overview-grid {
    grid-template-columns: 1fr;
  }

  .intelligence-status {
    align-items: flex-start;
    flex-direction: column;
  }

  .status-right {
    width: 100%;
    justify-content: space-between;
  }

  .metric-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .mini-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .score-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .payroll-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-card {
    min-height: 380px;
  }

  .doughnut-chart-wrapper,
  .radar-chart-wrapper {
    height: 225px;
  }

  .bar-chart-wrapper,
  .payroll-bar-wrapper {
    height: 205px;
  }

  .workload-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .employee-info {
    min-width: 0;
  }

  .workload-stats {
    width: 100%;
    grid-template-columns: 1fr 1fr;
  }

  .workload-progress {
    grid-column: 1 / -1;
    width: 100%;
  }

  .breakdown-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .breakdown-values {
    width: 100%;
  }
}

.body--dark .intelligence-page {
  background: #101722;
  color: #e2e8f0;
}

.body--dark .overview-card,
.body--dark .intelligence-card {
  background: #17202d;
  border-color: #263244;
  box-shadow: none;
}

.body--dark .page-title,
.body--dark .card-value,
.body--dark .section-heading h2,
.body--dark .metric-box strong,
.body--dark .status-title,
.body--dark .payroll-total strong,
.body--dark .employee-name {
  color: #f1f5f9;
}

.body--dark .page-subtitle,
.body--dark .section-heading p,
.body--dark .card-label,
.body--dark .card-description,
.body--dark .generated-time,
.body--dark .status-description,
.body--dark .metric-label,
.body--dark .breakdown-name small,
.body--dark .alert-message,
.body--dark .empty-text,
.body--dark .performance-subtitle,
.body--dark .employee-code {
  color: #94a3b8;
}

.body--dark .metric-box,
.body--dark .mini-stats > div,
.body--dark .score-grid > div,
.body--dark .payroll-grid > div,
.body--dark .payroll-total,
.body--dark .task-summary > div,
.body--dark .workload-stats > div,
.body--dark .chart-footer-stats > div {
  background: #111a27;
  border-color: #263244;
}

.body--dark .intelligence-status {
  background: #142033;
  border-color: #263a55;
}

.body--dark .breakdown-row,
.body--dark .compact-row,
.body--dark .workload-row {
  border-color: #263244;
}

.body--dark .breakdown-name span,
.body--dark .progress-heading,
.body--dark .compact-row,
.body--dark .performance-title,
.body--dark .payroll-grid strong,
.body--dark .score-grid strong,
.body--dark .mini-stats strong,
.body--dark .workload-stats > div:not(.workload-progress) strong,
.body--dark .chart-footer-stats strong {
  color: #cbd5e1;
}

.body--dark .alert-item {
  background: #111a27;
  border-color: #263244;
}

.body--dark .period-chip {
  background: #17202d;
}

.body--dark .payroll-total-footer {
  background: #2a2114;
}

.body--dark .payroll-total-footer span {
  color: #94a3b8;
}
</style>
