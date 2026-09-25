<template>
  <q-page class="somi-dashboard q-pa-md q-pa-lg-xl">
    <!-- Loading -->
    <template v-if="loading">
      <div class="dashboard-loading">
        <q-skeleton
          type="rect"
          class="hero-skeleton"
          animation="fade"
        />

        <div class="row q-col-gutter-md q-mt-md">
          <div
            v-for="item in 8"
            :key="item"
            class="col-12 col-sm-6 col-lg-3"
          >
            <q-skeleton
              type="rect"
              height="132px"
              class="radius-18"
              animation="fade"
            />
          </div>
        </div>

        <div class="row q-col-gutter-md q-mt-md">
          <div class="col-12 col-lg-8">
            <q-skeleton
              type="rect"
              height="360px"
              class="radius-20"
              animation="fade"
            />
          </div>

          <div class="col-12 col-lg-4">
            <q-skeleton
              type="rect"
              height="360px"
              class="radius-20"
              animation="fade"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Dashboard -->
    <template v-else>
      <!-- Error -->
      <q-banner
        v-if="errorMessage"
        class="dashboard-error q-mb-md"
        rounded
      >
        <template #avatar>
          <q-icon
            name="error_outline"
            size="28px"
          />
        </template>

        <div class="text-weight-medium">
          {{ errorMessage }}
        </div>

        <template #action>
          <q-btn
            flat
            no-caps
            label="Retry"
            icon="refresh"
            @click="loadDashboard"
          />
        </template>
      </q-banner>

      <!-- Hero -->
      <section class="dashboard-hero">
        <div class="hero-content">
          <div class="hero-eyebrow">
            <q-icon
              name="auto_awesome"
              size="17px"
            />
            <span>Smart Office Management & Intelligence</span>
          </div>

          <h1 class="hero-title">
            Welcome back, {{ firstName }}!
          </h1>

          <p class="hero-description">
            Here is your current office overview. Monitor people,
            attendance, leaves, tasks and operational activity from one place.
          </p>

          <div class="hero-meta">
            <q-chip
              v-if="userRole"
              dense
              class="role-chip"
              icon="verified_user"
            >
              {{ formattedRole }}
            </q-chip>

            <span
              v-if="userEmail"
              class="hero-email"
            >
              {{ userEmail }}
            </span>
          </div>
        </div>

        <div class="hero-visual">
          <div class="hero-orbit hero-orbit-one"></div>
          <div class="hero-orbit hero-orbit-two"></div>

          <div class="hero-icon">
            <q-icon
              name="business_center"
              size="42px"
            />
          </div>

          <div class="floating-dot floating-dot-one"></div>
          <div class="floating-dot floating-dot-two"></div>
          <div class="floating-dot floating-dot-three"></div>
        </div>
      </section>

      <!-- KPI Cards -->
      <section class="q-mt-md">
        <div class="row q-col-gutter-md">
          <!-- Employees -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-blue">
                <q-icon
                  name="groups"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Total Employees
                </div>

                <div class="metric-value">
                  {{ totalEmployees }}
                </div>

                <div class="metric-caption">
                  People registered in SOMI
                </div>
              </div>

              <q-icon
                name="trending_up"
                class="metric-trend"
                size="20px"
              />
            </div>
          </div>

          <!-- Active Employees -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-green">
                <q-icon
                  name="how_to_reg"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Active Employees
                </div>

                <div class="metric-value">
                  {{ activeEmployees }}
                </div>

                <div class="metric-caption">
                  {{ activePercentage }}% of workforce active
                </div>
              </div>

              <q-icon
                name="check_circle"
                class="metric-trend metric-success"
                size="20px"
              />
            </div>
          </div>

          <!-- Departments -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-purple">
                <q-icon
                  name="account_tree"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Departments
                </div>

                <div class="metric-value">
                  {{ totalDepartments }}
                </div>

                <div class="metric-caption">
                  {{ activeDepartments }} currently active
                </div>
              </div>

              <q-icon
                name="domain"
                class="metric-trend"
                size="20px"
              />
            </div>
          </div>

          <!-- Attendance -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-cyan">
                <q-icon
                  name="fact_check"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Attendance Today
                </div>

                <div class="metric-value">
                  {{ attendancePresent }}
                </div>

                <div class="metric-caption">
                  {{ attendanceCoverage }}% present
                </div>
              </div>

              <q-icon
                name="event_available"
                class="metric-trend metric-success"
                size="20px"
              />
            </div>
          </div>

          <!-- Pending Leaves -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-orange">
                <q-icon
                  name="event_busy"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Pending Leaves
                </div>

                <div class="metric-value">
                  {{ pendingLeaves }}
                </div>

                <div class="metric-caption">
                  Awaiting review
                </div>
              </div>

              <q-icon
                name="schedule"
                class="metric-trend"
                size="20px"
              />
            </div>
          </div>

          <!-- Active Tasks -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-indigo">
                <q-icon
                  name="task_alt"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Active Tasks
                </div>

                <div class="metric-value">
                  {{ activeTasks }}
                </div>

                <div class="metric-caption">
                  Work currently in progress
                </div>
              </div>

              <q-icon
                name="pending_actions"
                class="metric-trend"
                size="20px"
              />
            </div>
          </div>

          <!-- Completed Tasks -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-teal">
                <q-icon
                  name="task_alt"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Completed Tasks
                </div>

                <div class="metric-value">
                  {{ completedTasks }}
                </div>

                <div class="metric-caption">
                  Completed task records
                </div>
              </div>

              <q-icon
                name="done_all"
                class="metric-trend metric-success"
                size="20px"
              />
            </div>
          </div>

          <!-- Role -->
          <div class="col-12 col-sm-6 col-lg-3">
            <div class="metric-card">
              <div class="metric-icon metric-icon-slate">
                <q-icon
                  name="badge"
                  size="25px"
                />
              </div>

              <div class="metric-body">
                <div class="metric-label">
                  Your Role
                </div>

                <div class="metric-value metric-role">
                  {{ formattedRole || 'User' }}
                </div>

                <div class="metric-caption">
                  Current access level
                </div>
              </div>

              <q-icon
                name="shield"
                class="metric-trend"
                size="20px"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- Operational Snapshot -->
      <section class="q-mt-md">
        <div class="dashboard-card operational-card">
          <div class="card-header">
            <div>
              <div class="card-kicker">
                Operations
              </div>

              <h2 class="card-title">
                Operational Snapshot
              </h2>

              <p class="card-subtitle">
                Current attendance, leave and task activity available to your account
              </p>
            </div>

            <q-chip
              dense
              class="snapshot-chip"
              icon="monitor_heart"
            >
              Live data
            </q-chip>
          </div>

          <div class="snapshot-grid">
            <!-- Attendance -->
            <div class="snapshot-panel">
              <div class="snapshot-panel-header">
                <div class="snapshot-icon snapshot-icon-blue">
                  <q-icon
                    name="fact_check"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="snapshot-title">
                    Attendance
                  </div>

                  <div class="snapshot-subtitle">
                    Current records
                  </div>
                </div>
              </div>

              <div class="snapshot-stat-row">
                <div>
                  <strong>{{ attendancePresent }}</strong>
                  <span>Present</span>
                </div>

                <div>
                  <strong>{{ attendanceLate }}</strong>
                  <span>Late</span>
                </div>

                <div>
                  <strong>{{ attendanceAbsent }}</strong>
                  <span>Absent</span>
                </div>

                <div>
                  <strong>{{ attendanceOnLeave }}</strong>
                  <span>On Leave</span>
                </div>
              </div>

              <div class="snapshot-progress">
                <q-linear-progress
                  rounded
                  size="7px"
                  :value="attendanceCoverage / 100"
                  class="attendance-progress"
                />

                <span>
                  {{ attendanceCoverage }}% present today
                </span>
              </div>
            </div>

            <!-- Leave -->
            <div class="snapshot-panel">
              <div class="snapshot-panel-header">
                <div class="snapshot-icon snapshot-icon-orange">
                  <q-icon
                    name="event"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="snapshot-title">
                    Leave Requests
                  </div>

                  <div class="snapshot-subtitle">
                    Request status overview
                  </div>
                </div>
              </div>

              <div class="snapshot-stat-row">
                <div>
                  <strong>{{ pendingLeaves }}</strong>
                  <span>Pending</span>
                </div>

                <div>
                  <strong>{{ approvedLeaves }}</strong>
                  <span>Approved</span>
                </div>

                <div>
                  <strong>{{ rejectedLeaves }}</strong>
                  <span>Rejected</span>
                </div>

                <div>
                  <strong>{{ totalLeaves }}</strong>
                  <span>Total</span>
                </div>
              </div>

              <div class="snapshot-progress">
                <q-linear-progress
                  rounded
                  size="7px"
                  :value="leaveApprovalRate / 100"
                  class="leave-progress"
                />

                <span>
                  {{ leaveApprovalRate }}% approved
                </span>
              </div>
            </div>

            <!-- Tasks -->
            <div class="snapshot-panel">
              <div class="snapshot-panel-header">
                <div class="snapshot-icon snapshot-icon-purple">
                  <q-icon
                    name="assignment"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="snapshot-title">
                    Tasks
                  </div>

                  <div class="snapshot-subtitle">
                    Current work distribution
                  </div>
                </div>
              </div>

              <div class="snapshot-stat-row">
                <div>
                  <strong>{{ todoTasks }}</strong>
                  <span>To Do</span>
                </div>

                <div>
                  <strong>{{ inProgressTasks }}</strong>
                  <span>Progress</span>
                </div>

                <div>
                  <strong>{{ reviewTasks }}</strong>
                  <span>Review</span>
                </div>

                <div>
                  <strong>{{ completedTasks }}</strong>
                  <span>Done</span>
                </div>
              </div>

              <div class="snapshot-progress">
                <q-linear-progress
                  rounded
                  size="7px"
                  :value="taskCompletionRate / 100"
                  class="task-progress"
                />

                <span>
                  {{ taskCompletionRate }}% completed
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Main Insights -->
      <section class="q-mt-md">
        <div class="row q-col-gutter-md">
          <!-- Employee Distribution -->
          <div class="col-12 col-lg-8">
            <div class="dashboard-card chart-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    Workforce
                  </div>

                  <h2 class="card-title">
                    Employee Distribution
                  </h2>

                  <p class="card-subtitle">
                    Employees across your organization's departments
                  </p>
                </div>

                <q-btn
                  flat
                  round
                  dense
                  icon="more_horiz"
                  class="card-menu"
                >
                  <q-tooltip>
                    Workforce overview
                  </q-tooltip>
                </q-btn>
              </div>

              <div
                v-if="hasEmployeeChartData"
                class="chart-wrapper employee-chart"
              >
                <canvas ref="employeeChartCanvas"></canvas>
              </div>

              <div
                v-else
                class="empty-chart"
              >
                <q-icon
                  name="bar_chart"
                  size="46px"
                />

                <div class="empty-title">
                  No workforce data yet
                </div>

                <div class="empty-description">
                  Employee distribution will appear here once employee
                  records are available.
                </div>
              </div>
            </div>
          </div>

          <!-- Department Distribution -->
          <div class="col-12 col-lg-4">
            <div class="dashboard-card chart-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    Organization
                  </div>

                  <h2 class="card-title">
                    Departments
                  </h2>

                  <p class="card-subtitle">
                    Current department distribution
                  </p>
                </div>
              </div>

              <div
                v-if="hasDepartmentChartData"
                class="chart-wrapper department-chart"
              >
                <canvas ref="departmentChartCanvas"></canvas>

                <div class="chart-center">
                  <strong>{{ totalEmployees }}</strong>
                  <span>Employees</span>
                </div>
              </div>

              <div
                v-else
                class="empty-chart"
              >
                <q-icon
                  name="donut_large"
                  size="46px"
                />

                <div class="empty-title">
                  No department data
                </div>

                <div class="empty-description">
                  Add departments and employees to see the distribution.
                </div>
              </div>

              <div
                v-if="hasDepartmentChartData"
                class="department-legend"
              >
                <div
                  v-for="department in departmentLegend"
                  :key="department.id"
                  class="legend-item"
                >
                  <span
                    class="legend-dot"
                    :style="{ background: department.color }"
                  ></span>

                  <span class="legend-name">
                    {{ department.name }}
                  </span>

                  <strong class="legend-value">
                    {{ department.count }}
                  </strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Department Overview + Workforce Status -->
      <section class="q-mt-md">
        <div class="row q-col-gutter-md">
          <!-- Department Overview -->
          <div class="col-12 col-lg-8">
            <div class="dashboard-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    Organization
                  </div>

                  <h2 class="card-title">
                    Department Overview
                  </h2>

                  <p class="card-subtitle">
                    Quick view of department structure and staffing
                  </p>
                </div>

                <q-btn
                  flat
                  no-caps
                  label="View all"
                  icon-right="arrow_forward"
                  class="view-all-btn"
                  @click="goToDepartments"
                />
              </div>

              <div
                v-if="departments.length"
                class="department-list"
              >
                <div
                  v-for="department in departmentRows"
                  :key="department.id"
                  class="department-row"
                >
                  <div class="department-main">
                    <div class="department-avatar">
                      {{ getDepartmentInitials(department.name) }}
                    </div>

                    <div class="department-info">
                      <div class="department-name">
                        {{ department.name }}
                      </div>

                      <div class="department-code">
                        {{ department.code || 'No code assigned' }}
                      </div>
                    </div>
                  </div>

                  <div class="department-stats">
                    <div class="staff-count">
                      <strong>
                        {{ department.employeeCount }}
                      </strong>

                      <span>
                        {{ department.employeeCount === 1 ? 'employee' : 'employees' }}
                      </span>
                    </div>

                    <q-badge
                      rounded
                      :class="[
                        'status-badge',
                        department.isActive
                          ? 'status-active'
                          : 'status-inactive'
                      ]"
                    >
                      {{ department.isActive ? 'Active' : 'Inactive' }}
                    </q-badge>
                  </div>
                </div>
              </div>

              <div
                v-else
                class="empty-state"
              >
                <div class="empty-state-icon">
                  <q-icon
                    name="account_tree"
                    size="30px"
                  />
                </div>

                <div class="empty-title">
                  No departments available
                </div>

                <div class="empty-description">
                  Create your first department to start organizing your
                  workforce.
                </div>

                <q-btn
                  v-if="canManageDepartments"
                  unelevated
                  no-caps
                  label="Add Department"
                  icon="add"
                  class="primary-btn q-mt-md"
                  @click="goToDepartments"
                />
              </div>
            </div>
          </div>

          <!-- Workforce Status -->
          <div class="col-12 col-lg-4">
            <div class="dashboard-card status-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    Workforce
                  </div>

                  <h2 class="card-title">
                    Workforce Status
                  </h2>

                  <p class="card-subtitle">
                    Employee account status
                  </p>
                </div>
              </div>

              <div class="status-summary">
                <div class="status-progress">
                  <q-circular-progress
                    show-value
                    font-size="22px"
                    :value="activePercentage"
                    size="142px"
                    :thickness="0.16"
                    class="workforce-progress"
                  >
                    {{ activePercentage }}%
                  </q-circular-progress>
                </div>

                <div class="status-details">
                  <div class="status-detail">
                    <span class="status-detail-dot active-dot"></span>

                    <div>
                      <span class="status-detail-label">
                        Active
                      </span>

                      <strong>
                        {{ activeEmployees }}
                      </strong>
                    </div>
                  </div>

                  <div class="status-detail">
                    <span class="status-detail-dot inactive-dot"></span>

                    <div>
                      <span class="status-detail-label">
                        Inactive
                      </span>

                      <strong>
                        {{ inactiveEmployees }}
                      </strong>
                    </div>
                  </div>
                </div>
              </div>

              <div class="status-note">
                <q-icon
                  name="info_outline"
                  size="18px"
                />

                <span>
                  Workforce figures are based on the latest employee
                  records available from SOMI.
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Employees + Recent Activity -->
      <section class="q-mt-md">
        <div class="row q-col-gutter-md">
          <!-- Recent Employees -->
          <div class="col-12 col-lg-8">
            <div class="dashboard-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    People
                  </div>

                  <h2 class="card-title">
                    Recent Employees
                  </h2>

                  <p class="card-subtitle">
                    Latest employee records in the organization
                  </p>
                </div>

                <q-btn
                  flat
                  no-caps
                  label="Employees"
                  icon-right="arrow_forward"
                  class="view-all-btn"
                  @click="goToEmployees"
                />
              </div>

              <div
                v-if="recentEmployees.length"
                class="recent-employees"
              >
                <div
                  v-for="employee in recentEmployees"
                  :key="employee.id || employee.employee_id"
                  class="employee-row"
                >
                  <div class="employee-avatar">
                    {{ getEmployeeInitials(employee.full_name) }}
                  </div>

                  <div class="employee-info">
                    <div class="employee-name">
                      {{ employee.full_name || 'Unnamed Employee' }}
                    </div>

                    <div class="employee-meta">
                      <span>
                        {{ employee.job_title || 'Employee' }}
                      </span>

                      <span class="meta-separator">•</span>

                      <span>
                        {{ getEmployeeDepartment(employee) }}
                      </span>
                    </div>
                  </div>

                  <q-badge
                    rounded
                    :class="[
                      'status-badge',
                      isEmployeeActive(employee)
                        ? 'status-active'
                        : 'status-inactive'
                    ]"
                  >
                    {{ isEmployeeActive(employee) ? 'Active' : 'Inactive' }}
                  </q-badge>
                </div>
              </div>

              <div
                v-else
                class="empty-state compact"
              >
                <div class="empty-state-icon">
                  <q-icon
                    name="person_outline"
                    size="30px"
                  />
                </div>

                <div class="empty-title">
                  No employees available
                </div>

                <div class="empty-description">
                  Employee records will appear here once they are added.
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="col-12 col-lg-4">
            <div class="dashboard-card activity-card">
              <div class="card-header">
                <div>
                  <div class="card-kicker">
                    Activity
                  </div>

                  <h2 class="card-title">
                    Operational Activity
                  </h2>

                  <p class="card-subtitle">
                    Current module activity
                  </p>
                </div>
              </div>

              <div class="activity-list">
                <button
                  type="button"
                  class="activity-item"
                  @click="goToAttendance"
                >
                  <span class="activity-icon activity-blue">
                    <q-icon
                      name="fact_check"
                      size="20px"
                    />
                  </span>

                  <span class="activity-content">
                    <strong>Attendance</strong>
                    <small>
                      {{ attendancePresent }} present today
                    </small>
                  </span>

                  <q-icon
                    name="chevron_right"
                    size="19px"
                  />
                </button>

                <button
                  type="button"
                  class="activity-item"
                  @click="goToLeaves"
                >
                  <span class="activity-icon activity-orange">
                    <q-icon
                      name="event_busy"
                      size="20px"
                    />
                  </span>

                  <span class="activity-content">
                    <strong>Leave Requests</strong>
                    <small>
                      {{ pendingLeaves }} awaiting review
                    </small>
                  </span>

                  <q-icon
                    name="chevron_right"
                    size="19px"
                  />
                </button>

                <button
                  type="button"
                  class="activity-item"
                  @click="goToTasks"
                >
                  <span class="activity-icon activity-purple">
                    <q-icon
                      name="task_alt"
                      size="20px"
                    />
                  </span>

                  <span class="activity-content">
                    <strong>Tasks</strong>
                    <small>
                      {{ activeTasks }} active tasks
                    </small>
                  </span>

                  <q-icon
                    name="chevron_right"
                    size="19px"
                  />
                </button>

                <button
                  type="button"
                  class="activity-item"
                  @click="goToPerformance"
                >
                  <span class="activity-icon activity-green">
                    <q-icon
                      name="trending_up"
                      size="20px"
                    />
                  </span>

                  <span class="activity-content">
                    <strong>Performance</strong>
                    <small>
                      Review employee performance
                    </small>
                  </span>

                  <q-icon
                    name="chevron_right"
                    size="19px"
                  />
                </button>

                <button
                  type="button"
                  class="activity-item"
                  @click="goToPayroll"
                >
                  <span class="activity-icon activity-teal">
                    <q-icon
                      name="payments"
                      size="20px"
                    />
                  </span>

                  <span class="activity-content">
                    <strong>Payroll</strong>
                    <small>
                      View payroll records
                    </small>
                  </span>

                  <q-icon
                    name="chevron_right"
                    size="19px"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Actions -->
      <section class="q-mt-md">
        <div class="dashboard-card quick-actions-card">
          <div class="card-header">
            <div>
              <div class="card-kicker">
                Shortcuts
              </div>

              <h2 class="card-title">
                Quick Actions
              </h2>

              <p class="card-subtitle">
                Jump directly to common SOMI operations
              </p>
            </div>
          </div>

          <div class="quick-actions quick-actions-grid">
            <button
              type="button"
              class="quick-action"
              @click="goToEmployees"
            >
              <span class="quick-action-icon icon-blue">
                <q-icon
                  name="groups"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Employees</strong>
                <small>View workforce records</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToDepartments"
            >
              <span class="quick-action-icon icon-purple">
                <q-icon
                  name="account_tree"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Departments</strong>
                <small>Manage organization structure</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToAttendance"
            >
              <span class="quick-action-icon icon-cyan">
                <q-icon
                  name="fact_check"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Attendance</strong>
                <small>Review attendance records</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToLeaves"
            >
              <span class="quick-action-icon icon-orange">
                <q-icon
                  name="event"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Leave Management</strong>
                <small>Review leave requests</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToTasks"
            >
              <span class="quick-action-icon icon-indigo">
                <q-icon
                  name="task_alt"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Tasks</strong>
                <small>Track assigned work</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToProfile"
            >
              <span class="quick-action-icon icon-green">
                <q-icon
                  name="person"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>My Profile</strong>
                <small>View account information</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              v-if="canManageEmployees"
              type="button"
              class="quick-action"
              @click="goToAddEmployee"
            >
              <span class="quick-action-icon icon-pink">
                <q-icon
                  name="person_add"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Add Employee</strong>
                <small>Create a new employee record</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>

            <button
              type="button"
              class="quick-action"
              @click="goToNotifications"
            >
              <span class="quick-action-icon icon-slate">
                <q-icon
                  name="notifications"
                  size="22px"
                />
              </span>

              <span class="quick-action-content">
                <strong>Notifications</strong>
                <small>View recent system alerts</small>
              </span>

              <q-icon
                name="chevron_right"
                size="20px"
              />
            </button>
          </div>
        </div>
      </section>

      <!-- Refresh -->
      <div class="dashboard-footer">
        <div class="footer-status">
          <span class="online-dot"></span>
          <span>Connected to SOMI services</span>
        </div>

        <q-btn
          flat
          no-caps
          icon="refresh"
          label="Refresh data"
          class="refresh-btn"
          :loading="loading"
          @click="loadDashboard"
        />
      </div>
    </template>

    <!-- Scroll to top -->
    <q-btn
      v-show="showScrollTop"
      fab
      icon="keyboard_arrow_up"
      class="scroll-top-btn"
      @click="scrollToTop"
    >
      <q-tooltip>
        Back to top
      </q-tooltip>
    </q-btn>
  </q-page>
</template>

<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref
} from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  DoughnutController,
  ArcElement,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'

import api from 'src/services/api'

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  DoughnutController,
  ArcElement,
  LinearScale,
  Tooltip,
  Legend
)

const $q = useQuasar()
const router = useRouter()
const store = useStore()

const loading = ref(true)
const errorMessage = ref('')

const employees = ref([])
const departments = ref([])
const attendance = ref([])
const leaves = ref([])
const tasks = ref([])

const employeeChartCanvas = ref(null)
const departmentChartCanvas = ref(null)

let employeeChart = null
let departmentChart = null

const showScrollTop = ref(false)

const currentUser = computed(() => store.getters.currentUser || {})

const firstName = computed(() => {
  const name = currentUser.value?.first_name?.trim()

  if (name) {
    return name
  }

  const fullName = currentUser.value?.full_name?.trim()

  if (fullName) {
    return fullName.split(' ')[0]
  }

  return currentUser.value?.username || 'there'
})

const userEmail = computed(() => {
  return currentUser.value?.email || ''
})

const userRole = computed(() => {
  return currentUser.value?.role || ''
})

const formattedRole = computed(() => {
  if (!userRole.value) {
    return ''
  }

  return String(userRole.value)
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
})

const totalEmployees = computed(() => employees.value.length)

const activeEmployees = computed(() => {
  return employees.value.filter((employee) => isEmployeeActive(employee)).length
})

const inactiveEmployees = computed(() => {
  return Math.max(
    totalEmployees.value - activeEmployees.value,
    0
  )
})

const activePercentage = computed(() => {
  if (!totalEmployees.value) {
    return 0
  }

  return Math.round(
    (activeEmployees.value / totalEmployees.value) * 100
  )
})

const totalDepartments = computed(() => departments.value.length)

const activeDepartments = computed(() => {
  return departments.value.filter((department) => {
    return department?.is_active !== false
  }).length
})

const canManageEmployees = computed(() => {
  return ['ADMIN', 'MANAGER'].includes(userRole.value)
})

const canManageDepartments = computed(() => {
  return ['ADMIN', 'MANAGER'].includes(userRole.value)
})

/* ----------------------------- */
/* Attendance                     */
/* ----------------------------- */

const attendancePresent = computed(() => {
  return attendance.value.filter((record) => {
    return String(record?.status || '').toUpperCase() === 'PRESENT'
  }).length
})

const attendanceLate = computed(() => {
  return attendance.value.filter((record) => {
    return String(record?.status || '').toUpperCase() === 'LATE'
  }).length
})

const attendanceAbsent = computed(() => {
  return attendance.value.filter((record) => {
    return String(record?.status || '').toUpperCase() === 'ABSENT'
  }).length
})

const attendanceOnLeave = computed(() => {
  return attendance.value.filter((record) => {
    return String(record?.status || '').toUpperCase() === 'ON_LEAVE'
  }).length
})

const attendanceCoverage = computed(() => {
  if (!totalEmployees.value) {
    return 0
  }

  return Math.min(
    Math.round(
      (attendancePresent.value / totalEmployees.value) * 100
    ),
    100
  )
})

/* ----------------------------- */
/* Leave                         */
/* ----------------------------- */

const pendingLeaves = computed(() => {
  return leaves.value.filter((leave) => {
    return String(leave?.status || '').toUpperCase() === 'PENDING'
  }).length
})

const approvedLeaves = computed(() => {
  return leaves.value.filter((leave) => {
    return String(leave?.status || '').toUpperCase() === 'APPROVED'
  }).length
})

const rejectedLeaves = computed(() => {
  return leaves.value.filter((leave) => {
    return String(leave?.status || '').toUpperCase() === 'REJECTED'
  }).length
})

const totalLeaves = computed(() => leaves.value.length)

const leaveApprovalRate = computed(() => {
  const reviewedLeaves =
    approvedLeaves.value + rejectedLeaves.value

  if (!reviewedLeaves) {
    return 0
  }

  return Math.round(
    (approvedLeaves.value / reviewedLeaves) * 100
  )
})

/* ----------------------------- */
/* Tasks                         */
/* ----------------------------- */

const todoTasks = computed(() => {
  return tasks.value.filter((task) => {
    return String(task?.status || '').toUpperCase() === 'TODO'
  }).length
})

const inProgressTasks = computed(() => {
  return tasks.value.filter((task) => {
    return String(task?.status || '').toUpperCase() === 'IN_PROGRESS'
  }).length
})

const reviewTasks = computed(() => {
  return tasks.value.filter((task) => {
    return String(task?.status || '').toUpperCase() === 'REVIEW'
  }).length
})

const completedTasks = computed(() => {
  return tasks.value.filter((task) => {
    return String(task?.status || '').toUpperCase() === 'COMPLETED'
  }).length
})

const cancelledTasks = computed(() => {
  return tasks.value.filter((task) => {
    return String(task?.status || '').toUpperCase() === 'CANCELLED'
  }).length
})

const activeTasks = computed(() => {
  return (
    todoTasks.value +
    inProgressTasks.value +
    reviewTasks.value
  )
})

const taskCompletionRate = computed(() => {
  const measurableTasks =
    activeTasks.value +
    completedTasks.value

  if (!measurableTasks) {
    return 0
  }

  return Math.round(
    (completedTasks.value / measurableTasks) * 100
  )
})

/* ----------------------------- */
/* Department / Employee data    */
/* ----------------------------- */

const departmentRows = computed(() => {
  return departments.value
    .map((department) => ({
      ...department,
      employeeCount: getDepartmentEmployeeCount(department),
      isActive: department?.is_active !== false
    }))
    .sort((a, b) => {
      if (b.employeeCount !== a.employeeCount) {
        return b.employeeCount - a.employeeCount
      }

      return String(a.name || '').localeCompare(
        String(b.name || '')
      )
    })
    .slice(0, 6)
})

const departmentLegend = computed(() => {
  return departments.value
    .map((department, index) => ({
      id: department.id ?? department.code ?? index,
      name: department.name || 'Unnamed',
      count: getDepartmentEmployeeCount(department),
      color:
        chartPalette[index % chartPalette.length]
    }))
    .filter((department) => department.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, 6)
})

const recentEmployees = computed(() => {
  return [...employees.value]
    .sort((a, b) => {
      const dateA = getEmployeeDate(a)
      const dateB = getEmployeeDate(b)

      if (dateA && dateB) {
        return new Date(dateB) - new Date(dateA)
      }

      return String(a.full_name || '').localeCompare(
        String(b.full_name || '')
      )
    })
    .slice(0, 5)
})

const hasEmployeeChartData = computed(() => {
  return departmentRows.value.some(
    (department) => department.employeeCount > 0
  )
})

const hasDepartmentChartData = computed(() => {
  return departmentLegend.value.length > 0
})

const chartPalette = [
  '#2563eb',
  '#7c3aed',
  '#0891b2',
  '#059669',
  '#d97706',
  '#db2777'
]

/* ----------------------------- */
/* Helpers                       */
/* ----------------------------- */

function normalizeListResponse (response) {
  const data = response?.data

  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.results)) {
    return data.results
  }

  if (Array.isArray(data?.data)) {
    return data.data
  }

  return []
}

function isEmployeeActive (employee) {
  if (employee?.is_active !== undefined) {
    return Boolean(employee.is_active)
  }

  if (employee?.active !== undefined) {
    return Boolean(employee.active)
  }

  if (employee?.status !== undefined) {
    return (
      String(employee.status).toLowerCase() === 'active'
    )
  }

  return true
}

function getDepartmentId (value) {
  if (value === null || value === undefined) {
    return null
  }

  if (typeof value === 'object') {
    return (
      value.id ??
      value.department_id ??
      value.pk ??
      null
    )
  }

  return value
}

function getEmployeeDepartmentId (employee) {
  return (
    getDepartmentId(employee?.department) ??
    employee?.department_id ??
    employee?.departmentId ??
    null
  )
}

function getDepartmentEmployeeCount (department) {
  const departmentId = getDepartmentId(department)

  return employees.value.filter((employee) => {
    const employeeDepartmentId =
      getEmployeeDepartmentId(employee)

    if (
      departmentId !== null &&
      employeeDepartmentId !== null &&
      String(employeeDepartmentId) ===
        String(departmentId)
    ) {
      return true
    }

    const employeeDepartmentName =
      typeof employee?.department === 'object'
        ? employee.department?.name
        : employee?.department_name

    return (
      employeeDepartmentName &&
      department?.name &&
      String(employeeDepartmentName).toLowerCase() ===
        String(department.name).toLowerCase()
    )
  }).length
}

function getEmployeeDepartment (employee) {
  if (typeof employee?.department === 'object') {
    return (
      employee.department?.name ||
      employee.department?.code ||
      'Unassigned'
    )
  }

  return (
    employee?.department_name ||
    employee?.department ||
    'Unassigned'
  )
}

function getEmployeeDate (employee) {
  return (
    employee?.created_at ||
    employee?.date_joined ||
    employee?.joining_date ||
    employee?.createdAt ||
    null
  )
}

function getEmployeeInitials (name) {
  const value = String(name || '').trim()

  if (!value) {
    return 'NA'
  }

  const parts = value
    .split(/\s+/)
    .filter(Boolean)

  if (parts.length === 1) {
    return parts[0]
      .slice(0, 2)
      .toUpperCase()
  }

  return `${parts[0][0]}${parts[parts.length - 1][0]}`
    .toUpperCase()
}

function getDepartmentInitials (name) {
  const value = String(name || '').trim()

  if (!value) {
    return 'DP'
  }

  const parts = value
    .split(/\s+/)
    .filter(Boolean)

  if (parts.length === 1) {
    return parts[0]
      .slice(0, 2)
      .toUpperCase()
  }

  return `${parts[0][0]}${parts[1][0]}`
    .toUpperCase()
}

/* ----------------------------- */
/* Dashboard loading             */
/* ----------------------------- */

async function loadDashboard () {
  loading.value = true
  errorMessage.value = ''

  try {
    const [
      departmentResponse,
      employeeResponse,
      attendanceResponse,
      leaveResponse,
      taskResponse
    ] = await Promise.all([
      api.get('/departments/'),
      api.get('/employees/'),
      api.get('/attendance/'),
      api.get('/leave/requests/'),
      api.get('/tasks/')
    ])

    departments.value =
      normalizeListResponse(departmentResponse)

    employees.value =
      normalizeListResponse(employeeResponse)

    attendance.value =
      normalizeListResponse(attendanceResponse)

    leaves.value =
      normalizeListResponse(leaveResponse)

    tasks.value =
      normalizeListResponse(taskResponse)

    await nextTick()

    renderCharts()
  } catch (error) {
    console.error(
      'Dashboard loading failed:',
      error
    )

    const status = error?.response?.status

    if (status === 401) {
      errorMessage.value =
        'Your session has expired. Please sign in again.'
    } else if (status === 403) {
      errorMessage.value =
        'You do not have permission to view dashboard data.'
    } else if (error?.response) {
      errorMessage.value =
        'Unable to load dashboard data from the server.'
    } else {
      errorMessage.value =
        'Unable to connect to SOMI services. Please check the backend connection.'
    }

    $q.notify({
      type: 'negative',
      message: errorMessage.value,
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

/* ----------------------------- */
/* Charts                        */
/* ----------------------------- */

function destroyCharts () {
  if (employeeChart) {
    employeeChart.destroy()
    employeeChart = null
  }

  if (departmentChart) {
    departmentChart.destroy()
    departmentChart = null
  }
}

function renderCharts () {
  destroyCharts()

  if (
    employeeChartCanvas.value &&
    hasEmployeeChartData.value
  ) {
    const rows =
      departmentRows.value.filter(
        (department) =>
          department.employeeCount > 0
      )

    employeeChart = new Chart(
      employeeChartCanvas.value,
      {
        type: 'bar',
        data: {
          labels: rows.map(
            (department) => department.name
          ),
          datasets: [
            {
              label: 'Employees',
              data: rows.map(
                (department) =>
                  department.employeeCount
              ),
              backgroundColor: rows.map(
                (_, index) =>
                  chartPalette[
                    index %
                    chartPalette.length
                  ]
              ),
              borderRadius: 8,
              borderSkipped: false,
              maxBarThickness: 42
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              displayColors: false,
              padding: 12,
              callbacks: {
                label: (context) =>
                  ` ${context.parsed.y} employees`
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                color: getChartTextColor(),
                font: {
                  size: 11
                }
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0,
                color: getChartTextColor(),
                font: {
                  size: 11
                }
              },
              grid: {
                color: getChartGridColor()
              }
            }
          }
        }
      }
    )
  }

  if (
    departmentChartCanvas.value &&
    hasDepartmentChartData.value
  ) {
    const data = departmentLegend.value

    departmentChart = new Chart(
      departmentChartCanvas.value,
      {
        type: 'doughnut',
        data: {
          labels: data.map(
            (department) => department.name
          ),
          datasets: [
            {
              data: data.map(
                (department) =>
                  department.count
              ),
              backgroundColor: data.map(
                (department) =>
                  department.color
              ),
              borderWidth: 0,
              hoverOffset: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '72%',
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              displayColors: true,
              padding: 12,
              callbacks: {
                label: (context) => {
                  const value =
                    context.parsed || 0

                  return ` ${value} employees`
                }
              }
            }
          }
        }
      }
    )
  }
}

function getChartTextColor () {
  return $q.dark.isActive
    ? '#aab4c5'
    : '#667085'
}

function getChartGridColor () {
  return $q.dark.isActive
    ? 'rgba(148, 163, 184, 0.12)'
    : 'rgba(15, 23, 42, 0.08)'
}

/* ----------------------------- */
/* Navigation                    */
/* ----------------------------- */

function goToEmployees () {
  router.push('/Empl-list')
}

function goToDepartments () {
  router.push('/list_dep')
}

function goToProfile () {
  router.push('/AccountSettings')
}

function goToAddEmployee () {
  router.push('/add_employee')
}

function goToAttendance () {
  router.push('/attan_report')
}

function goToLeaves () {
  if (['ADMIN', 'MANAGER'].includes(userRole.value)) {
    router.push('/Approver_leaves')
    return
  }

  router.push('/leavePage')
}

function goToTasks () {
  router.push('/tasks')
}

function goToPerformance () {
  router.push('/performance')
}

function goToPayroll () {
  router.push('/payroll_report')
}

function goToNotifications () {
  $q.notify({
    type: 'info',
    message:
      'Use the notification bell in the top header to view your notifications.',
    position: 'top-right'
  })
}

/* ----------------------------- */
/* Scroll / resize               */
/* ----------------------------- */

function handleScroll () {
  showScrollTop.value =
    window.scrollY > 420
}

function scrollToTop () {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

function handleResize () {
  if (loading.value) {
    return
  }

  renderCharts()
}

/* ----------------------------- */
/* Lifecycle                     */
/* ----------------------------- */

onMounted(async () => {
  window.addEventListener(
    'scroll',
    handleScroll,
    { passive: true }
  )

  window.addEventListener(
    'resize',
    handleResize
  )

  await loadDashboard()
})

onBeforeUnmount(() => {
  window.removeEventListener(
    'scroll',
    handleScroll
  )

  window.removeEventListener(
    'resize',
    handleResize
  )

  destroyCharts()
})
</script>

<style scoped>
.somi-dashboard {
  min-height: 100%;
  background: #f6f8fc;
  color: #172033;
}

.dashboard-loading {
  max-width: 1600px;
  margin: 0 auto;
}

.hero-skeleton {
  height: 250px;
  border-radius: 24px;
}

.radius-18 {
  border-radius: 18px;
}

.radius-20 {
  border-radius: 20px;
}

.dashboard-hero {
  position: relative;
  min-height: 250px;
  padding: 34px 38px;
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background:
    radial-gradient(
      circle at 90% 20%,
      rgba(96, 165, 250, 0.22),
      transparent 28%
    ),
    radial-gradient(
      circle at 65% 100%,
      rgba(124, 58, 237, 0.16),
      transparent 30%
    ),
    linear-gradient(
      135deg,
      #0f172a 0%,
      #172554 58%,
      #1e3a8a 100%
    );
  box-shadow:
    0 18px 45px rgba(15, 23, 42, 0.16);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 820px;
}

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 11px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.07);
  color: #bfdbfe;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.hero-title {
  margin: 18px 0 8px;
  color: #ffffff;
  font-size: clamp(28px, 4vw, 42px);
  line-height: 1.1;
  font-weight: 750;
  letter-spacing: -0.035em;
}

.hero-description {
  max-width: 700px;
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 14px;
  line-height: 1.7;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.role-chip {
  margin: 0;
  background: rgba(255, 255, 255, 0.11);
  color: #e0edff;
  border: 1px solid rgba(255, 255, 255, 0.13);
}

.hero-email {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.hero-visual {
  position: relative;
  width: 220px;
  height: 220px;
  flex: 0 0 220px;
  margin-right: 25px;
}

.hero-orbit {
  position: absolute;
  inset: 10px;
  border: 1px solid rgba(147, 197, 253, 0.16);
  border-radius: 50%;
}

.hero-orbit-two {
  inset: 36px;
  border-color: rgba(196, 181, 253, 0.15);
}

.hero-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 94px;
  height: 94px;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #dbeafe;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.16);
  backdrop-filter: blur(10px);
}

.floating-dot {
  position: absolute;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #93c5fd;
  box-shadow:
    0 0 0 6px rgba(147, 197, 253, 0.08);
}

.floating-dot-one {
  top: 30px;
  right: 42px;
}

.floating-dot-two {
  left: 22px;
  top: 112px;
  background: #c4b5fd;
}

.floating-dot-three {
  right: 28px;
  bottom: 35px;
  background: #67e8f9;
}

/* ----------------------------- */
/* KPI Cards                     */
/* ----------------------------- */

.metric-card {
  position: relative;
  min-height: 132px;
  padding: 21px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  overflow: hidden;
  border: 1px solid #e8edf5;
  border-radius: 18px;
  background: #ffffff;
  box-shadow:
    0 7px 25px rgba(15, 23, 42, 0.045);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  border-color: #dce5f2;
  box-shadow:
    0 12px 30px rgba(15, 23, 42, 0.075);
}

.metric-icon {
  width: 48px;
  height: 48px;
  flex: 0 0 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.metric-icon-blue {
  background: #eff6ff;
  color: #2563eb;
}

.metric-icon-green {
  background: #ecfdf5;
  color: #059669;
}

.metric-icon-purple {
  background: #f5f3ff;
  color: #7c3aed;
}

.metric-icon-orange {
  background: #fff7ed;
  color: #ea580c;
}

.metric-icon-cyan {
  background: #ecfeff;
  color: #0891b2;
}

.metric-icon-indigo {
  background: #eef2ff;
  color: #4f46e5;
}

.metric-icon-teal {
  background: #f0fdfa;
  color: #0f766e;
}

.metric-icon-slate {
  background: #f1f5f9;
  color: #475569;
}

.metric-icon-pink {
  background: #fdf2f8;
  color: #db2777;
}

.metric-body {
  min-width: 0;
}

.metric-label {
  color: #667085;
  font-size: 12px;
  font-weight: 600;
}

.metric-value {
  margin-top: 3px;
  color: #172033;
  font-size: 27px;
  line-height: 1.25;
  font-weight: 750;
  letter-spacing: -0.03em;
}

.metric-role {
  font-size: 20px;
}

.metric-caption {
  margin-top: 5px;
  color: #98a2b3;
  font-size: 11px;
  line-height: 1.4;
}

.metric-trend {
  position: absolute;
  top: 20px;
  right: 19px;
  color: #98a2b3;
}

.metric-success {
  color: #059669;
}

/* ----------------------------- */
/* Cards                         */
/* ----------------------------- */

.dashboard-card {
  height: 100%;
  padding: 24px;
  border: 1px solid #e8edf5;
  border-radius: 20px;
  background: #ffffff;
  box-shadow:
    0 7px 25px rgba(15, 23, 42, 0.045);
}

.chart-card {
  min-height: 390px;
}

.operational-card {
  min-height: 270px;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.card-kicker {
  margin-bottom: 5px;
  color: #2563eb;
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 0.11em;
  text-transform: uppercase;
}

.card-title {
  margin: 0;
  color: #172033;
  font-size: 17px;
  line-height: 1.35;
  font-weight: 700;
  letter-spacing: -0.015em;
}

.card-subtitle {
  margin: 5px 0 0;
  color: #98a2b3;
  font-size: 12px;
  line-height: 1.5;
}

.card-menu {
  color: #98a2b3;
}

.view-all-btn {
  min-height: 34px;
  color: #2563eb;
  font-size: 12px;
  font-weight: 650;
}

.snapshot-chip {
  margin: 0;
  background: #eff6ff;
  color: #2563eb;
  font-size: 10px;
  font-weight: 650;
}

/* ----------------------------- */
/* Operational Snapshot          */
/* ----------------------------- */

.snapshot-grid {
  display: grid;
  grid-template-columns:
    repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 20px;
}

.snapshot-panel {
  min-width: 0;
  padding: 17px;
  border: 1px solid #edf1f6;
  border-radius: 16px;
  background: #fbfcfe;
}

.snapshot-panel-header {
  display: flex;
  align-items: center;
  gap: 11px;
}

.snapshot-icon {
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.snapshot-icon-blue {
  background: #eff6ff;
  color: #2563eb;
}

.snapshot-icon-orange {
  background: #fff7ed;
  color: #ea580c;
}

.snapshot-icon-purple {
  background: #f5f3ff;
  color: #7c3aed;
}

.snapshot-title {
  color: #344054;
  font-size: 13px;
  font-weight: 700;
}

.snapshot-subtitle {
  margin-top: 2px;
  color: #98a2b3;
  font-size: 10px;
}

.snapshot-stat-row {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: 7px;
  margin-top: 18px;
}

.snapshot-stat-row > div {
  min-width: 0;
  padding: 8px 6px;
  border-radius: 9px;
  background: #ffffff;
  text-align: center;
}

.snapshot-stat-row strong {
  display: block;
  color: #344054;
  font-size: 16px;
  font-weight: 750;
}

.snapshot-stat-row span {
  display: block;
  margin-top: 2px;
  overflow: hidden;
  color: #98a2b3;
  font-size: 8px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.snapshot-progress {
  margin-top: 14px;
}

.snapshot-progress span {
  display: block;
  margin-top: 6px;
  color: #98a2b3;
  font-size: 9px;
}

.attendance-progress {
  color: #2563eb;
}

.leave-progress {
  color: #ea580c;
}

.task-progress {
  color: #7c3aed;
}

/* ----------------------------- */
/* Charts                        */
/* ----------------------------- */

.chart-wrapper {
  position: relative;
  width: 100%;
  margin-top: 20px;
}

.employee-chart {
  height: 285px;
}

.department-chart {
  width: 220px;
  height: 220px;
  margin: 22px auto 14px;
}

.chart-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  transform: translateY(-1px);
}

.chart-center strong {
  color: #172033;
  font-size: 26px;
  line-height: 1;
  font-weight: 750;
}

.chart-center span {
  margin-top: 5px;
  color: #98a2b3;
  font-size: 11px;
}

.department-legend {
  display: flex;
  flex-direction: column;
  gap: 9px;
  margin-top: 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
}

.legend-dot {
  width: 8px;
  height: 8px;
  flex: 0 0 8px;
  border-radius: 50%;
}

.legend-name {
  min-width: 0;
  flex: 1;
  overflow: hidden;
  color: #667085;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.legend-value {
  color: #344054;
  font-size: 11px;
}

/* ----------------------------- */
/* Empty states                  */
/* ----------------------------- */

.empty-chart,
.empty-state {
  min-height: 270px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.empty-chart {
  color: #98a2b3;
}

.empty-chart .q-icon {
  margin-bottom: 10px;
  color: #cbd5e1;
}

.empty-title {
  color: #344054;
  font-size: 13px;
  font-weight: 700;
}

.empty-description {
  max-width: 340px;
  margin-top: 5px;
  color: #98a2b3;
  font-size: 11px;
  line-height: 1.6;
}

/* ----------------------------- */
/* Departments                   */
/* ----------------------------- */

.department-list {
  margin-top: 17px;
}

.department-row {
  min-height: 66px;
  padding: 11px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  border-bottom: 1px solid #eef2f6;
}

.department-row:last-child {
  border-bottom: 0;
}

.department-main {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.department-avatar {
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 11px;
  font-weight: 750;
}

.department-info {
  min-width: 0;
}

.department-name {
  overflow: hidden;
  color: #344054;
  font-size: 13px;
  font-weight: 650;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.department-code {
  margin-top: 3px;
  color: #98a2b3;
  font-size: 10px;
}

.department-stats {
  display: flex;
  align-items: center;
  gap: 15px;
}

.staff-count {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.staff-count strong {
  color: #344054;
  font-size: 13px;
}

.staff-count span {
  color: #98a2b3;
  font-size: 9px;
}

.status-badge {
  min-width: 58px;
  justify-content: center;
  padding: 5px 9px;
  font-size: 9px;
  font-weight: 700;
}

.status-active {
  background: #ecfdf3;
  color: #027a48;
}

.status-inactive {
  background: #f2f4f7;
  color: #667085;
}

/* ----------------------------- */
/* Workforce status              */
/* ----------------------------- */

.status-summary {
  min-height: 245px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
}

.status-progress {
  flex: 0 0 auto;
}

.workforce-progress {
  color: #2563eb;
}

.status-details {
  display: flex;
  flex-direction: column;
  gap: 19px;
}

.status-detail {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-detail-dot {
  width: 9px;
  height: 9px;
  flex: 0 0 9px;
  border-radius: 50%;
}

.active-dot {
  background: #10b981;
}

.inactive-dot {
  background: #cbd5e1;
}

.status-detail > div {
  display: flex;
  flex-direction: column;
}

.status-detail-label {
  color: #98a2b3;
  font-size: 10px;
}

.status-detail strong {
  margin-top: 2px;
  color: #344054;
  font-size: 17px;
}

.status-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 11px 12px;
  border-radius: 12px;
  background: #f8fafc;
  color: #98a2b3;
  font-size: 10px;
  line-height: 1.5;
}

.status-note .q-icon {
  flex: 0 0 auto;
  color: #94a3b8;
}

/* ----------------------------- */
/* Recent employees              */
/* ----------------------------- */

.recent-employees {
  margin-top: 17px;
}

.employee-row {
  min-height: 67px;
  padding: 10px 0;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #eef2f6;
}

.employee-row:last-child {
  border-bottom: 0;
}

.employee-avatar {
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #eef2ff;
  color: #4f46e5;
  font-size: 11px;
  font-weight: 750;
}

.employee-info {
  min-width: 0;
  flex: 1;
}

.employee-name {
  overflow: hidden;
  color: #344054;
  font-size: 13px;
  font-weight: 650;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.employee-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 3px;
  overflow: hidden;
  color: #98a2b3;
  font-size: 10px;
}

.employee-meta span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-separator {
  flex: 0 0 auto;
}

.empty-state {
  min-height: 210px;
}

.empty-state.compact {
  min-height: 190px;
}

.empty-state-icon {
  width: 58px;
  height: 58px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 17px;
  background: #f8fafc;
  color: #94a3b8;
}

.primary-btn {
  min-height: 38px;
  padding: 0 16px;
  border-radius: 10px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 650;
}

/* ----------------------------- */
/* Activity                      */
/* ----------------------------- */

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-top: 18px;
}

.activity-item {
  width: 100%;
  min-height: 60px;
  padding: 8px 9px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid transparent;
  border-radius: 13px;
  background: transparent;
  color: #344054;
  text-align: left;
  cursor: pointer;
  transition:
    background 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s ease;
}

.activity-item:hover {
  background: #f8fafc;
  border-color: #e8edf5;
  transform: translateX(2px);
}

.activity-icon {
  width: 39px;
  height: 39px;
  flex: 0 0 39px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
}

.activity-blue {
  background: #eff6ff;
  color: #2563eb;
}

.activity-orange {
  background: #fff7ed;
  color: #ea580c;
}

.activity-purple {
  background: #f5f3ff;
  color: #7c3aed;
}

.activity-green {
  background: #ecfdf5;
  color: #059669;
}

.activity-teal {
  background: #f0fdfa;
  color: #0f766e;
}

.activity-content {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-content strong {
  color: #344054;
  font-size: 11px;
  font-weight: 700;
}

.activity-content small {
  margin-top: 2px;
  overflow: hidden;
  color: #98a2b3;
  font-size: 9px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.activity-item > .q-icon {
  color: #c0c8d3;
}

/* ----------------------------- */
/* Quick Actions                 */
/* ----------------------------- */

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 18px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: 9px;
}

.quick-action {
  width: 100%;
  min-height: 65px;
  padding: 9px 10px;
  display: flex;
  align-items: center;
  gap: 11px;
  border: 1px solid transparent;
  border-radius: 13px;
  background: transparent;
  color: #344054;
  text-align: left;
  cursor: pointer;
  transition:
    background 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s ease;
}

.quick-action:hover {
  background: #f8fafc;
  border-color: #e8edf5;
  transform: translateY(-1px);
}

.quick-action-icon {
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.icon-blue {
  background: #eff6ff;
  color: #2563eb;
}

.icon-purple {
  background: #f5f3ff;
  color: #7c3aed;
}

.icon-green {
  background: #ecfdf5;
  color: #059669;
}

.icon-orange {
  background: #fff7ed;
  color: #ea580c;
}

.icon-cyan {
  background: #ecfeff;
  color: #0891b2;
}

.icon-indigo {
  background: #eef2ff;
  color: #4f46e5;
}

.icon-pink {
  background: #fdf2f8;
  color: #db2777;
}

.icon-slate {
  background: #f1f5f9;
  color: #475569;
}

.quick-action-content {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.quick-action-content strong {
  color: #344054;
  font-size: 12px;
  font-weight: 700;
}

.quick-action-content small {
  margin-top: 2px;
  overflow: hidden;
  color: #98a2b3;
  font-size: 9px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.quick-action > .q-icon {
  color: #c0c8d3;
}

/* ----------------------------- */
/* Footer                        */
/* ----------------------------- */

.dashboard-footer {
  min-height: 58px;
  padding: 16px 3px 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-status {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #98a2b3;
  font-size: 10px;
}

.online-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow:
    0 0 0 4px rgba(16, 185, 129, 0.1);
}

.refresh-btn {
  min-height: 32px;
  color: #667085;
  font-size: 11px;
}

.dashboard-error {
  border: 1px solid #fecaca;
  background: #fff7f7;
  color: #b42318;
}

.scroll-top-btn {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 20;
  width: 44px;
  height: 44px;
  background: #172554;
  color: #ffffff;
  box-shadow:
    0 10px 25px rgba(15, 23, 42, 0.18);
}

/* ----------------------------- */
/* Responsive                    */
/* ----------------------------- */

@media (max-width: 1200px) {
  .quick-actions-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .dashboard-hero {
    padding: 28px;
  }

  .hero-visual {
    width: 180px;
    height: 180px;
    flex-basis: 180px;
    margin-right: 0;
  }

  .snapshot-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .dashboard-hero {
    min-height: 0;
    padding: 25px 22px;
  }

  .hero-visual {
    display: none;
  }

  .hero-title {
    font-size: 30px;
  }

  .hero-description {
    font-size: 13px;
  }

  .hero-meta {
    align-items: flex-start;
    flex-direction: column;
    gap: 7px;
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .snapshot-stat-row {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .department-stats {
    gap: 8px;
  }

  .staff-count {
    display: none;
  }

  .dashboard-footer {
    align-items: flex-start;
    flex-direction: column;
    gap: 7px;
  }
}

@media (max-width: 480px) {
  .somi-dashboard {
    padding: 10px !important;
  }

  .dashboard-card {
    padding: 18px;
    border-radius: 17px;
  }

  .metric-card {
    padding: 18px;
  }

  .card-header {
    gap: 8px;
  }

  .card-title {
    font-size: 16px;
  }

  .department-chart {
    width: 190px;
    height: 190px;
  }

  .status-summary {
    gap: 15px;
  }

  .status-progress .q-circular-progress {
    width: 120px !important;
    height: 120px !important;
  }
}

/* ----------------------------- */
/* Dark mode                     */
/* ----------------------------- */

body.body--dark .somi-dashboard {
  background: #0b1120;
  color: #e5e7eb;
}

.body--dark .dashboard-hero {
  box-shadow:
    0 18px 45px rgba(0, 0, 0, 0.25);
}

.body--dark .metric-card,
.body--dark .dashboard-card {
  border-color: rgba(148, 163, 184, 0.12);
  background: #111827;
  box-shadow:
    0 8px 30px rgba(0, 0, 0, 0.14);
}

.body--dark .metric-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
}

.body--dark .metric-label,
.body--dark .card-subtitle,
.body--dark .metric-caption,
.body--dark .legend-name,
.body--dark .department-code,
.body--dark .staff-count span,
.body--dark .status-detail-label,
.body--dark .employee-meta,
.body--dark .footer-status,
.body--dark .snapshot-subtitle,
.body--dark .snapshot-progress span,
.body--dark .activity-content small {
  color: #8893a7;
}

.body--dark .metric-value,
.body--dark .card-title,
.body--dark .chart-center strong,
.body--dark .legend-value,
.body--dark .department-name,
.body--dark .staff-count strong,
.body--dark .status-detail strong,
.body--dark .employee-name,
.body--dark .quick-action-content strong,
.body--dark .empty-title,
.body--dark .snapshot-title,
.body--dark .snapshot-stat-row strong,
.body--dark .activity-content strong {
  color: #e5e7eb;
}

.body--dark .department-row,
.body--dark .employee-row {
  border-color: rgba(148, 163, 184, 0.1);
}

.body--dark .department-avatar {
  background: rgba(37, 99, 235, 0.14);
}

.body--dark .employee-avatar {
  background: rgba(79, 70, 229, 0.15);
}

.body--dark .status-note,
.body--dark .empty-state-icon,
.body--dark .quick-action:hover,
.body--dark .activity-item:hover,
.body--dark .snapshot-panel {
  background: #0f172a;
}

.body--dark .status-note,
.body--dark .snapshot-progress span {
  color: #8893a7;
}

.body--dark .quick-action:hover,
.body--dark .activity-item:hover {
  border-color: rgba(148, 163, 184, 0.1);
}

.body--dark .status-inactive {
  background: rgba(148, 163, 184, 0.1);
  color: #98a2b3;
}

.body--dark .snapshot-stat-row > div {
  background: #111827;
}

.body--dark .snapshot-chip {
  background: rgba(37, 99, 235, 0.14);
  color: #93c5fd;
}

:global(.body--dark) .somi-dashboard {
  background: #0b1120;
  color: #e5e7eb;
}

:global(.body--dark) .dashboard-hero {
  box-shadow:
    0 18px 45px rgba(0, 0, 0, 0.25);
}

:global(.body--dark) .metric-card,
:global(.body--dark) .dashboard-card {
  border-color: rgba(148, 163, 184, 0.12);
  background: #111827;
  box-shadow:
    0 8px 30px rgba(0, 0, 0, 0.14);
}

:global(.body--dark) .metric-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
}

:global(.body--dark) .metric-label,
:global(.body--dark) .card-subtitle,
:global(.body--dark) .metric-caption,
:global(.body--dark) .legend-name,
:global(.body--dark) .department-code,
:global(.body--dark) .staff-count span,
:global(.body--dark) .status-detail-label,
:global(.body--dark) .employee-meta,
:global(.body--dark) .footer-status,
:global(.body--dark) .snapshot-subtitle,
:global(.body--dark) .snapshot-progress span,
:global(.body--dark) .activity-content small {
  color: #8893a7;
}

:global(.body--dark) .metric-value,
:global(.body--dark) .card-title,
:global(.body--dark) .chart-center strong,
:global(.body--dark) .legend-value,
:global(.body--dark) .department-name,
:global(.body--dark) .staff-count strong,
:global(.body--dark) .status-detail strong,
:global(.body--dark) .employee-name,
:global(.body--dark) .quick-action-content strong,
:global(.body--dark) .empty-title,
:global(.body--dark) .snapshot-title,
:global(.body--dark) .snapshot-stat-row strong,
:global(.body--dark) .activity-content strong {
  color: #e5e7eb;
}

:global(.body--dark) .department-row,
:global(.body--dark) .employee-row {
  border-color: rgba(148, 163, 184, 0.1);
}

:global(.body--dark) .department-avatar {
  background: rgba(37, 99, 235, 0.14);
}

:global(.body--dark) .employee-avatar {
  background: rgba(79, 70, 229, 0.15);
}

:global(.body--dark) .status-note,
:global(.body--dark) .empty-state-icon,
:global(.body--dark) .quick-action:hover,
:global(.body--dark) .activity-item:hover,
:global(.body--dark) .snapshot-panel {
  background: #0f172a;
}

:global(.body--dark) .status-note,
:global(.body--dark) .snapshot-progress span {
  color: #8893a7;
}

:global(.body--dark) .quick-action:hover,
:global(.body--dark) .activity-item:hover {
  border-color: rgba(148, 163, 184, 0.1);
}

:global(.body--dark) .status-inactive {
  background: rgba(148, 163, 184, 0.1);
  color: #98a2b3;
}

:global(.body--dark) .snapshot-stat-row > div {
  background: #111827;
}

:global(.body--dark) .snapshot-chip {
  background: rgba(37, 99, 235, 0.14);
  color: #93c5fd;
}

:global(.body--dark) .dashboard-error {
  border-color: rgba(248, 113, 113, 0.25);
  background: rgba(127, 29, 29, 0.18);
  color: #fca5a5;
}

:global(.body--dark) .refresh-btn {
  color: #98a2b3;
}
</style>
