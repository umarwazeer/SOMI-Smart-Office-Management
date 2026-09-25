<template>
  <q-page class="performance-page">
    <div class="page-shell">

      <!-- Header -->
      <div class="page-header">
        <div>
          <div class="eyebrow">
            <q-icon name="insights" />
            PERFORMANCE MANAGEMENT
          </div>

          <h1>Performance Reviews</h1>

          <p>
            Track employee performance, goals, productivity and review progress.
          </p>
        </div>

        <div class="header-actions">
          <q-btn
            flat
            round
            icon="refresh"
            :loading="loading"
            @click="loadData"
          >
            <q-tooltip>Refresh</q-tooltip>
          </q-btn>

          <q-btn
            v-if="canManage"
            unelevated
            no-caps
            icon="add"
            label="Create Review"
            class="primary-action"
            @click="openCreateDialog"
          />
        </div>
      </div>

      <!-- Error -->
      <q-banner
        v-if="errorMessage"
        rounded
        class="error-banner q-mb-lg"
      >
        <template #avatar>
          <q-icon name="error_outline" />
        </template>

        {{ errorMessage }}

        <template #action>
          <q-btn
            flat
            label="Dismiss"
            no-caps
            @click="errorMessage = ''"
          />
        </template>
      </q-banner>

      <!-- Summary -->
      <div class="summary-grid">
        <div class="summary-card">
          <div class="summary-icon blue">
            <q-icon name="rate_review" />
          </div>

          <div class="summary-content">
            <span>Total Reviews</span>
            <strong>{{ summary.total }}</strong>
            <small>All performance reviews</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon green">
            <q-icon name="task_alt" />
          </div>

          <div class="summary-content">
            <span>Submitted</span>
            <strong>{{ summary.submitted }}</strong>
            <small>Reviews submitted</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon orange">
            <q-icon name="edit_note" />
          </div>

          <div class="summary-content">
            <span>Draft Reviews</span>
            <strong>{{ summary.draft }}</strong>
            <small>Still in progress</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon purple">
            <q-icon name="star" />
          </div>

          <div class="summary-content">
            <span>Average Rating</span>
            <strong>{{ summary.averageRating }}</strong>
            <small>Out of 10</small>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="content-card">
        <div class="filter-toolbar">

          <q-input
            v-model="filters.search"
            outlined
            dense
            clearable
            debounce="300"
            placeholder="Search employee, ID or department..."
            class="search-field"
          >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <q-select
            v-model="filters.period"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="periodOptions"
            label="Review Period"
            class="filter-field"
          />

          <q-select
            v-model="filters.status"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="statusOptions"
            label="Status"
            class="filter-field"
          />

          <q-select
            v-if="canManage"
            v-model="filters.department"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="departmentOptions"
            label="Department"
            class="filter-field"
          />

          <q-btn
            v-if="hasFilters"
            flat
            no-caps
            icon="filter_alt_off"
            label="Clear"
            class="clear-btn"
            @click="clearFilters"
          />
        </div>

        <!-- Table -->
        <q-table
          flat
          :rows="filteredReviews"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :pagination="{ rowsPerPage: 10 }"
          class="performance-table"
          no-data-label="No performance reviews found"
          no-results-label="No matching reviews found"
        >
          <template #loading>
            <q-inner-loading showing>
              <q-spinner-dots size="40px" />
            </q-inner-loading>
          </template>

          <!-- Employee -->
          <template #body-cell-employee="props">
            <q-td :props="props">
              <div class="employee-cell">
                <q-avatar size="38px" class="employee-avatar">
                  <q-icon name="person" />
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

          <!-- Rating -->
          <template #body-cell-rating="props">
            <q-td :props="props">
              <div class="rating-cell">
                <q-icon name="star" size="17px" />
                <strong>{{ formatScore(props.row.rating) }}</strong>
                <span>/10</span>
              </div>
            </q-td>
          </template>

          <!-- Period -->
          <template #body-cell-review_period="props">
            <q-td :props="props">
              <q-chip
                dense
                square
                class="period-chip"
              >
                {{ formatPeriod(props.row.review_period) }}
              </q-chip>
            </q-td>
          </template>

          <!-- Status -->
          <template #body-cell-status="props">
            <q-td :props="props">
              <q-chip
                dense
                :class="['status-chip', statusClass(props.row.status)]"
              >
                <q-icon
                  :name="statusIcon(props.row.status)"
                  size="15px"
                  class="q-mr-xs"
                />
                {{ formatStatus(props.row.status) }}
              </q-chip>
            </q-td>
          </template>

          <!-- Scores -->
          <template #body-cell-scores="props">
            <q-td :props="props">
              <div class="score-mini-grid">
                <span>
                  <b>P</b>
                  {{ formatScore(props.row.productivity_score) }}
                </span>

                <span>
                  <b>G</b>
                  {{ formatScore(props.row.goals_score) }}
                </span>

                <span>
                  <b>Q</b>
                  {{ formatScore(props.row.quality_score) }}
                </span>
              </div>
            </q-td>
          </template>

          <!-- Date -->
          <template #body-cell-review_date="props">
            <q-td :props="props">
              <div class="date-cell">
                <q-icon name="event" size="16px" />
                {{ formatDate(props.row.review_date) }}
              </div>
            </q-td>
          </template>

          <!-- Actions -->
          <template #body-cell-actions="props">
            <q-td :props="props">
              <div class="action-buttons">
                <q-btn
                  flat
                  round
                  dense
                  icon="visibility"
                  @click="openDetails(props.row)"
                >
                  <q-tooltip>View Details</q-tooltip>
                </q-btn>

                <q-btn
                  v-if="canManage"
                  flat
                  round
                  dense
                  icon="edit"
                  @click="openEditDialog(props.row)"
                >
                  <q-tooltip>Edit Review</q-tooltip>
                </q-btn>

                <q-btn
                  v-if="canDelete"
                  flat
                  round
                  dense
                  icon="delete_outline"
                  class="delete-action"
                  @click="confirmDelete(props.row)"
                >
                  <q-tooltip>Delete Review</q-tooltip>
                </q-btn>
              </div>
            </q-td>
          </template>

          <!-- Empty -->
          <template #no-data>
            <div class="empty-state">
              <q-icon name="insights" size="58px" />

              <div class="empty-title">
                No performance reviews found
              </div>

              <div class="empty-text">
                Create a performance review to start tracking employee progress.
              </div>

              <q-btn
                v-if="canManage"
                unelevated
                no-caps
                icon="add"
                label="Create Review"
                class="primary-action q-mt-md"
                @click="openCreateDialog"
              />
            </div>
          </template>
        </q-table>
      </q-card>
    </div>

    <!-- Create/Edit Dialog -->
    <q-dialog
      v-model="showFormDialog"
      persistent
      @hide="resetForm"
    >
      <q-card class="form-dialog">

        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-eyebrow">
              PERFORMANCE REVIEW
            </div>

            <div class="dialog-title">
              {{ editingReview ? 'Edit Performance Review' : 'Create Performance Review' }}
            </div>

            <div class="dialog-subtitle">
              Record employee performance and review feedback.
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            v-close-popup
          />
        </q-card-section>

        <q-separator />

        <q-card-section class="dialog-body">

          <!-- Employee & Review Info -->
          <div class="section-title">
            <q-icon name="person_search" />
            Review Information
          </div>

          <div class="form-grid">

            <q-select
              v-model="form.employee"
              outlined
              emit-value
              map-options
              :options="employeeOptions"
              label="Employee *"
              :disable="editingReview"
              :error="!!formErrors.employee"
              :error-message="formErrors.employee"
            />

            <q-select
              v-model="form.review_period"
              outlined
              emit-value
              map-options
              :options="periodOptions"
              label="Review Period *"
            />

            <q-input
              v-model="form.review_date"
              outlined
              type="date"
              label="Review Date *"
            />

            <q-select
              v-model="form.status"
              outlined
              emit-value
              map-options
              :options="statusOptions"
              label="Status"
            />

          </div>

          <!-- Performance Scores -->
          <div class="section-title q-mt-lg">
            <q-icon name="analytics" />
            Performance Scores
            <span class="section-hint">0 – 10</span>
          </div>

          <div class="score-form-grid">

            <div class="score-input">
              <q-input
                v-model.number="form.rating"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Overall Rating"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.rating)"
              />
            </div>

            <div class="score-input">
              <q-input
                v-model.number="form.goals_score"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Goals Score"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.goals_score)"
              />
            </div>

            <div class="score-input">
              <q-input
                v-model.number="form.productivity_score"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Productivity Score"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.productivity_score)"
              />
            </div>

            <div class="score-input">
              <q-input
                v-model.number="form.quality_score"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Quality Score"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.quality_score)"
              />
            </div>

            <div class="score-input">
              <q-input
                v-model.number="form.teamwork_score"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Teamwork Score"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.teamwork_score)"
              />
            </div>

            <div class="score-input">
              <q-input
                v-model.number="form.communication_score"
                outlined
                type="number"
                min="0"
                max="10"
                step="0.1"
                label="Communication Score"
              />
              <q-linear-progress
                rounded
                size="5px"
                :value="scoreValue(form.communication_score)"
              />
            </div>

          </div>

          <!-- Feedback -->
          <div class="section-title q-mt-lg">
            <q-icon name="forum" />
            Review Feedback
          </div>

          <div class="feedback-grid">

            <q-input
              v-model="form.strengths"
              outlined
              type="textarea"
              autogrow
              label="Strengths"
              placeholder="Key strengths and positive contributions..."
            />

            <q-input
              v-model="form.improvement_areas"
              outlined
              type="textarea"
              autogrow
              label="Improvement Areas"
              placeholder="Areas where the employee can improve..."
            />

            <q-input
              v-model="form.manager_feedback"
              outlined
              type="textarea"
              autogrow
              label="Manager Feedback"
              placeholder="Manager's overall feedback..."
            />

            <q-input
              v-model="form.employee_comments"
              outlined
              type="textarea"
              autogrow
              label="Employee Comments"
              placeholder="Employee response or comments..."
            />

          </div>

        </q-card-section>

        <q-separator />

        <q-card-actions align="right" class="dialog-actions">
          <q-btn
            flat
            no-caps
            label="Cancel"
            v-close-popup
          />

          <q-btn
            unelevated
            no-caps
            :label="editingReview ? 'Update Review' : 'Create Review'"
            :loading="saving"
            class="primary-action"
            @click="saveReview"
          />
        </q-card-actions>

      </q-card>
    </q-dialog>

    <!-- Details Dialog -->
    <q-dialog v-model="showDetailsDialog">
      <q-card class="details-dialog" v-if="selectedReview">

        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-eyebrow">
              PERFORMANCE DETAILS
            </div>

            <div class="dialog-title">
              {{ selectedReview.employee_name }}
            </div>

            <div class="dialog-subtitle">
              {{ selectedReview.employee_id }} ·
              {{ selectedReview.department_name || 'No Department' }}
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            v-close-popup
          />
        </q-card-section>

        <q-separator />

        <q-card-section>

          <div class="details-summary">
            <div class="overall-score">
              <div class="score-number">
                {{ formatScore(selectedReview.rating) }}
              </div>

              <div class="score-label">
                Overall Rating / 10
              </div>
            </div>

            <div class="detail-meta">
              <q-chip class="period-chip">
                {{ formatPeriod(selectedReview.review_period) }}
              </q-chip>

              <q-chip
                :class="[
                  'status-chip',
                  statusClass(selectedReview.status)
                ]"
              >
                {{ formatStatus(selectedReview.status) }}
              </q-chip>

              <div class="detail-date">
                <q-icon name="event" />
                {{ formatDate(selectedReview.review_date) }}
              </div>
            </div>
          </div>

          <div class="detail-score-grid">

            <div class="detail-score">
              <span>Goals</span>
              <strong>{{ formatScore(selectedReview.goals_score) }}</strong>
              <q-linear-progress
                rounded
                :value="scoreValue(selectedReview.goals_score)"
              />
            </div>

            <div class="detail-score">
              <span>Productivity</span>
              <strong>{{ formatScore(selectedReview.productivity_score) }}</strong>
              <q-linear-progress
                rounded
                :value="scoreValue(selectedReview.productivity_score)"
              />
            </div>

            <div class="detail-score">
              <span>Quality</span>
              <strong>{{ formatScore(selectedReview.quality_score) }}</strong>
              <q-linear-progress
                rounded
                :value="scoreValue(selectedReview.quality_score)"
              />
            </div>

            <div class="detail-score">
              <span>Teamwork</span>
              <strong>{{ formatScore(selectedReview.teamwork_score) }}</strong>
              <q-linear-progress
                rounded
                :value="scoreValue(selectedReview.teamwork_score)"
              />
            </div>

            <div class="detail-score">
              <span>Communication</span>
              <strong>{{ formatScore(selectedReview.communication_score) }}</strong>
              <q-linear-progress
                rounded
                :value="scoreValue(selectedReview.communication_score)"
              />
            </div>

          </div>

          <div class="details-feedback">

            <div
              v-if="selectedReview.strengths"
              class="feedback-block"
            >
              <div class="feedback-title">
                <q-icon name="thumb_up" />
                Strengths
              </div>

              <p>{{ selectedReview.strengths }}</p>
            </div>

            <div
              v-if="selectedReview.improvement_areas"
              class="feedback-block"
            >
              <div class="feedback-title">
                <q-icon name="trending_up" />
                Improvement Areas
              </div>

              <p>{{ selectedReview.improvement_areas }}</p>
            </div>

            <div
              v-if="selectedReview.manager_feedback"
              class="feedback-block"
            >
              <div class="feedback-title">
                <q-icon name="supervisor_account" />
                Manager Feedback
              </div>

              <p>{{ selectedReview.manager_feedback }}</p>
            </div>

            <div
              v-if="selectedReview.employee_comments"
              class="feedback-block"
            >
              <div class="feedback-title">
                <q-icon name="comment" />
                Employee Comments
              </div>

              <p>{{ selectedReview.employee_comments }}</p>
            </div>

          </div>

        </q-card-section>

      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE
})

export default {
  name: 'PerformancePage',

  data () {
    return {
      loading: false,
      saving: false,
      errorMessage: '',

      reviews: [],
      employees: [],
      departments: [],

      showFormDialog: false,
      showDetailsDialog: false,

      editingReview: null,
      selectedReview: null,

      currentUser: null,

      filters: {
        search: '',
        period: null,
        status: null,
        department: null
      },

      form: this.getEmptyForm(),

      formErrors: {},

      periodOptions: [
        {
          label: 'Monthly',
          value: 'MONTHLY'
        },
        {
          label: 'Quarterly',
          value: 'QUARTERLY'
        },
        {
          label: 'Half-Yearly',
          value: 'HALF_YEARLY'
        },
        {
          label: 'Yearly',
          value: 'YEARLY'
        }
      ],

      statusOptions: [
        {
          label: 'Draft',
          value: 'DRAFT'
        },
        {
          label: 'Submitted',
          value: 'SUBMITTED'
        },
        {
          label: 'Acknowledged',
          value: 'ACKNOWLEDGED'
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
          name: 'review_period',
          label: 'PERIOD',
          field: 'review_period',
          align: 'left',
          sortable: true
        },
        {
          name: 'rating',
          label: 'RATING',
          field: 'rating',
          align: 'left',
          sortable: true
        },
        {
          name: 'scores',
          label: 'KEY SCORES',
          field: 'productivity_score',
          align: 'left'
        },
        {
          name: 'status',
          label: 'STATUS',
          field: 'status',
          align: 'left',
          sortable: true
        },
        {
          name: 'review_date',
          label: 'REVIEW DATE',
          field: 'review_date',
          align: 'left',
          sortable: true
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
    role () {
      return (
        this.currentUser?.role ||
        this.currentUser?.user?.role ||
        ''
      ).toUpperCase()
    },

    canManage () {
      return this.role === 'ADMIN' || this.role === 'MANAGER'
    },

    canDelete () {
      return this.role === 'ADMIN'
    },

    employeeOptions () {
      return this.employees
        .filter(employee => employee.status !== 'INACTIVE')
        .map(employee => ({
          label: `${employee.full_name || employee.username} (${employee.employee_id})`,
          value: employee.id
        }))
    },

    departmentOptions () {
      return this.departments.map(department => ({
        label: department.name,
        value: department.id
      }))
    },

    hasFilters () {
      return Boolean(
        this.filters.search ||
        this.filters.period ||
        this.filters.status ||
        this.filters.department
      )
    },

    filteredReviews () {
      let rows = [...this.reviews]

      const search = this.filters.search
        ? this.filters.search.trim().toLowerCase()
        : ''

      if (search) {
        rows = rows.filter(review => {
          const values = [
            review.employee_name,
            review.employee_id,
            review.department_name
          ]

          return values.some(value =>
            String(value || '')
              .toLowerCase()
              .includes(search)
          )
        })
      }

      if (this.filters.period) {
        rows = rows.filter(
          review => review.review_period === this.filters.period
        )
      }

      if (this.filters.status) {
        rows = rows.filter(
          review => review.status === this.filters.status
        )
      }

      if (this.filters.department) {
        rows = rows.filter(
          review => {
            const departmentId = review.department
            return String(departmentId) === String(this.filters.department) ||
              String(review.department_id) === String(this.filters.department)
          }
        )
      }

      return rows
    },

    summary () {
      const rows = this.reviews

      const total = rows.length

      const submitted = rows.filter(
        review => review.status === 'SUBMITTED'
      ).length

      const draft = rows.filter(
        review => review.status === 'DRAFT'
      ).length

      const ratings = rows
        .map(review => Number(review.rating))
        .filter(value => !Number.isNaN(value))

      const averageRating = ratings.length
        ? (
            ratings.reduce((sum, value) => sum + value, 0) /
            ratings.length
          ).toFixed(1)
        : '0.0'

      return {
        total,
        submitted,
        draft,
        averageRating
      }
    }
  },

  async mounted () {
    await this.loadCurrentUser()
    await this.loadData()
  },

  methods: {
    getEmptyForm () {
      return {
        employee: null,
        review_period: 'QUARTERLY',
        review_date: new Date().toISOString().slice(0, 10),
        rating: 0,
        goals_score: 0,
        productivity_score: 0,
        quality_score: 0,
        teamwork_score: 0,
        communication_score: 0,
        strengths: '',
        improvement_areas: '',
        manager_feedback: '',
        employee_comments: '',
        status: 'DRAFT'
      }
    },

    getAuthConfig () {
      const token =
        localStorage.getItem('access') ||
        localStorage.getItem('access_token') ||
        localStorage.getItem('token')

      return token
        ? {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        : {}
    },

    async loadData () {
  this.loading = true
  this.errorMessage = ''

  try {
    const config = this.getAuthConfig()

    const performanceResponse = await api.get(
      '/performance/',
      config
    )

    this.reviews = Array.isArray(performanceResponse.data)
      ? performanceResponse.data
      : []

    if (this.canManage) {
      try {
        const employeeResponse = await api.get(
          '/employees/',
          config
        )

        this.employees = Array.isArray(employeeResponse.data)
          ? employeeResponse.data
          : []
      } catch (error) {
        console.error(
          'Employee data load error:',
          error
        )

        this.employees = []
      }

      try {
        const departmentResponse = await api.get(
          '/departments/',
          config
        )

        this.departments = Array.isArray(departmentResponse.data)
          ? departmentResponse.data
          : []
      } catch (error) {
        console.error(
          'Department data load error:',
          error
        )

        this.departments = []
      }
    }
  } catch (error) {
    console.error(
      'Performance load error:',
      error
    )

    this.errorMessage =
      error?.response?.data?.detail ||
      'Unable to load performance data.'
  } finally {
      this.loading = false
    }
  },

    async loadCurrentUser () {
      try {
        const config = this.getAuthConfig()

        const response = await api.get(
          '/auth/me/',
          config
        )

        this.currentUser = response.data
      } catch (error) {
        console.error('Current user error:', error)
      }
    },

    openCreateDialog () {
      if (!this.canManage) return

      this.editingReview = null
      this.form = this.getEmptyForm()
      this.formErrors = {}
      this.showFormDialog = true
    },

    openEditDialog (review) {
      if (!this.canManage) return

      this.editingReview = review

      this.form = {
        employee: review.employee,
        review_period: review.review_period,
        review_date: review.review_date,
        rating: Number(review.rating || 0),
        goals_score: Number(review.goals_score || 0),
        productivity_score: Number(review.productivity_score || 0),
        quality_score: Number(review.quality_score || 0),
        teamwork_score: Number(review.teamwork_score || 0),
        communication_score: Number(review.communication_score || 0),
        strengths: review.strengths || '',
        improvement_areas: review.improvement_areas || '',
        manager_feedback: review.manager_feedback || '',
        employee_comments: review.employee_comments || '',
        status: review.status || 'DRAFT'
      }

      this.formErrors = {}
      this.showFormDialog = true
    },

    async saveReview () {
      if (!this.validateForm()) {
        return
      }

      this.saving = true
      this.errorMessage = ''

      try {
        const config = {
          ...this.getAuthConfig(),
          headers: {
            ...this.getAuthConfig().headers,
            'Content-Type': 'application/json'
          }
        }

        const payload = {
          employee: this.form.employee,
          review_period: this.form.review_period,
          review_date: this.form.review_date,
          rating: this.cleanScore(this.form.rating),
          goals_score: this.cleanScore(this.form.goals_score),
          productivity_score: this.cleanScore(this.form.productivity_score),
          quality_score: this.cleanScore(this.form.quality_score),
          teamwork_score: this.cleanScore(this.form.teamwork_score),
          communication_score: this.cleanScore(this.form.communication_score),
          strengths: this.form.strengths || '',
          improvement_areas: this.form.improvement_areas || '',
          manager_feedback: this.form.manager_feedback || '',
          employee_comments: this.form.employee_comments || '',
          status: this.form.status
        }

        if (this.editingReview) {
          await api.patch(
            `/performance/${this.editingReview.id}/`,
            payload,
            config
          )

          this.$q.notify({
            type: 'positive',
            message: 'Performance review updated successfully.',
            icon: 'check_circle'
          })
        } else {
          await api.post(
            '/performance/',
            payload,
            config
          )

          this.$q.notify({
            type: 'positive',
            message: 'Performance review created successfully.',
            icon: 'check_circle'
          })
        }

        this.showFormDialog = false
        await this.loadData()
      } catch (error) {
        console.error('Performance save error:', error)

        const data = error?.response?.data

        if (data && typeof data === 'object') {
          const firstError = Object.values(data)
            .flat()
            .find(value => typeof value === 'string')

          this.errorMessage =
            firstError ||
            data.detail ||
            'Unable to save performance review.'
        } else {
          this.errorMessage = 'Unable to save performance review.'
        }
      } finally {
        this.saving = false
      }
    },

    validateForm () {
      this.formErrors = {}

      if (!this.form.employee) {
        this.formErrors.employee = 'Please select an employee.'
      }

      const scores = [
        'rating',
        'goals_score',
        'productivity_score',
        'quality_score',
        'teamwork_score',
        'communication_score'
      ]

      scores.forEach(field => {
        const value = Number(this.form[field])

        if (
          Number.isNaN(value) ||
          value < 0 ||
          value > 10
        ) {
          this.errorMessage =
            'All performance scores must be between 0 and 10.'

          this.formErrors[field] = 'Score must be between 0 and 10.'
        }
      })

      return Object.keys(this.formErrors).length === 0 &&
        !this.errorMessage
    },

    cleanScore (value) {
      const number = Number(value)

      if (Number.isNaN(number)) {
        return 0
      }

      return Math.min(
        10,
        Math.max(0, number)
      )
    },

    openDetails (review) {
      this.selectedReview = review
      this.showDetailsDialog = true
    },

    confirmDelete (review) {
      if (!this.canDelete) return

      this.$q.dialog({
        title: 'Delete Performance Review',
        message: `Are you sure you want to delete the performance review for ${review.employee_name}?`,
        cancel: {
          flat: true,
          noCaps: true
        },
        ok: {
          unelevated: true,
          noCaps: true,
          label: 'Delete'
        },
        persistent: true
      }).onOk(async () => {
        try {
          await api.delete(
            `/performance/${review.id}/`,
            this.getAuthConfig()
          )

          this.$q.notify({
            type: 'positive',
            message: 'Performance review deleted successfully.',
            icon: 'delete'
          })

          await this.loadData()
        } catch (error) {
          console.error('Performance delete error:', error)

          this.$q.notify({
            type: 'negative',
            message:
              error?.response?.data?.detail ||
              'Unable to delete performance review.'
          })
        }
      })
    },

    clearFilters () {
      this.filters = {
        search: '',
        period: null,
        status: null,
        department: null
      }
    },

    resetForm () {
      this.formErrors = {}
      this.errorMessage = ''
    },

    formatScore (value) {
      const number = Number(value)

      if (Number.isNaN(number)) {
        return '0.0'
      }

      return number.toFixed(1)
    },

    scoreValue (value) {
      const number = Number(value)

      if (Number.isNaN(number)) {
        return 0
      }

      return Math.min(
        1,
        Math.max(0, number / 10)
      )
    },

    formatPeriod (value) {
      const labels = {
        MONTHLY: 'Monthly',
        QUARTERLY: 'Quarterly',
        HALF_YEARLY: 'Half-Yearly',
        YEARLY: 'Yearly'
      }

      return labels[value] || value || '—'
    },

    formatStatus (value) {
      const labels = {
        DRAFT: 'Draft',
        SUBMITTED: 'Submitted',
        ACKNOWLEDGED: 'Acknowledged'
      }

      return labels[value] || value || '—'
    },

    statusClass (value) {
      return {
        DRAFT: 'status-draft',
        SUBMITTED: 'status-submitted',
        ACKNOWLEDGED: 'status-acknowledged'
      }[value] || 'status-draft'
    },

    statusIcon (value) {
      return {
        DRAFT: 'edit_note',
        SUBMITTED: 'check_circle',
        ACKNOWLEDGED: 'verified'
      }[value] || 'description'
    },

    formatDate (value) {
      if (!value) return '—'

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleDateString(
        'en-US',
        {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        }
      )
    }
  },

}
</script>

<style scoped>
.performance-page {
  min-height: 100vh;
  background: #f6f8fc;
  padding: 28px;
}

.page-shell {
  max-width: 1500px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 26px;
}

.eyebrow,
.dialog-eyebrow {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: #64748b;
}

.page-header h1 {
  margin: 7px 0 5px;
  font-size: 30px;
  line-height: 1.2;
  font-weight: 800;
  color: #172033;
}

.page-header p {
  margin: 0;
  color: #718096;
  font-size: 14px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.primary-action {
  min-height: 42px;
  padding: 0 18px;
  border-radius: 10px;
  font-weight: 700;
  background: #2563eb;
  color: white;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 15px;
  min-height: 120px;
  padding: 20px;
  border: 1px solid #e6eaf1;
  border-radius: 16px;
  background: white;
  box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
}

.summary-icon {
  width: 48px;
  height: 48px;
  flex: 0 0 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 13px;
  font-size: 23px;
}

.summary-icon.blue {
  background: #eff6ff;
  color: #2563eb;
}

.summary-icon.green {
  background: #ecfdf5;
  color: #059669;
}

.summary-icon.orange {
  background: #fff7ed;
  color: #ea580c;
}

.summary-icon.purple {
  background: #f5f3ff;
  color: #7c3aed;
}

.summary-content {
  min-width: 0;
}

.summary-content span {
  display: block;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
}

.summary-content strong {
  display: block;
  margin: 2px 0;
  color: #172033;
  font-size: 25px;
  line-height: 1.1;
}

.summary-content small {
  color: #94a3b8;
  font-size: 11px;
}

.content-card {
  overflow: hidden;
  border-color: #e6eaf1;
  border-radius: 16px;
  background: white;
}

.filter-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px;
  border-bottom: 1px solid #edf0f5;
}

.search-field {
  flex: 1 1 330px;
  min-width: 260px;
}

.filter-field {
  width: 180px;
}

.clear-btn {
  color: #64748b;
}

.performance-table {
  border-radius: 0;
}

.performance-table :deep(th) {
  background: #fafbfc;
  color: #64748b;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.performance-table :deep(td) {
  height: 68px;
  color: #334155;
  font-size: 13px;
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.employee-avatar {
  background: #eef2ff;
  color: #4f46e5;
}

.employee-name {
  color: #172033;
  font-weight: 700;
}

.employee-id {
  margin-top: 2px;
  color: #94a3b8;
  font-size: 11px;
}

.rating-cell {
  display: flex;
  align-items: baseline;
  gap: 4px;
  color: #172033;
}

.rating-cell q-icon {
  color: #f59e0b;
}

.rating-cell strong {
  font-size: 15px;
}

.rating-cell span {
  color: #94a3b8;
  font-size: 11px;
}

.period-chip,
.status-chip {
  font-weight: 700;
  font-size: 11px;
}

.period-chip {
  background: #f1f5f9;
  color: #475569;
}

.status-draft {
  background: #fff7ed;
  color: #c2410c;
}

.status-submitted {
  background: #ecfdf5;
  color: #047857;
}

.status-acknowledged {
  background: #eff6ff;
  color: #1d4ed8;
}

.score-mini-grid {
  display: flex;
  gap: 5px;
}

.score-mini-grid span {
  min-width: 39px;
  padding: 4px 5px;
  border-radius: 6px;
  background: #f8fafc;
  color: #64748b;
  font-size: 10px;
  text-align: center;
}

.score-mini-grid b {
  margin-right: 2px;
  color: #334155;
}

.date-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  color: #64748b;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
}

.action-buttons .q-btn {
  color: #64748b;
}

.action-buttons .delete-action {
  color: #dc2626;
}

.empty-state {
  padding: 65px 20px;
  text-align: center;
  color: #94a3b8;
}

.empty-state > .q-icon {
  color: #cbd5e1;
}

.empty-title {
  margin-top: 12px;
  color: #334155;
  font-size: 17px;
  font-weight: 750;
}

.empty-text {
  margin-top: 5px;
  font-size: 13px;
}

.error-banner {
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.form-dialog,
.details-dialog {
  width: min(900px, 94vw);
  max-width: 900px;
  border-radius: 18px;
  overflow: hidden;
}

.details-dialog {
  width: min(800px, 94vw);
  max-width: 800px;
}

.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  padding: 22px 24px;
}

.dialog-title {
  margin-top: 5px;
  color: #172033;
  font-size: 21px;
  font-weight: 800;
}

.dialog-subtitle {
  margin-top: 4px;
  color: #718096;
  font-size: 12px;
}

.dialog-body {
  max-height: 72vh;
  overflow-y: auto;
  padding: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #334155;
  font-size: 14px;
  font-weight: 800;
}

.section-title .q-icon {
  color: #2563eb;
}

.section-hint {
  margin-left: auto;
  color: #94a3b8;
  font-size: 11px;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 14px;
}

.score-form-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 14px;
}

.score-input .q-linear-progress {
  margin: 5px 2px 0;
}

.feedback-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 14px;
}

.dialog-actions {
  padding: 14px 24px;
}

.details-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
  border-radius: 14px;
  background: #f8fafc;
}

.overall-score {
  text-align: center;
  min-width: 130px;
}

.score-number {
  color: #2563eb;
  font-size: 38px;
  line-height: 1;
  font-weight: 850;
}

.score-label {
  margin-top: 5px;
  color: #64748b;
  font-size: 11px;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.detail-date {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #64748b;
  font-size: 12px;
}

.detail-score-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin-top: 20px;
}

.detail-score {
  padding: 14px;
  border: 1px solid #e7ebf1;
  border-radius: 12px;
  background: white;
}

.detail-score span {
  display: block;
  color: #64748b;
  font-size: 11px;
}

.detail-score strong {
  display: block;
  margin: 4px 0 8px;
  color: #172033;
  font-size: 20px;
}

.details-feedback {
  display: grid;
  gap: 12px;
  margin-top: 20px;
}

.feedback-block {
  padding: 15px;
  border-radius: 12px;
  background: #f8fafc;
}

.feedback-title {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
}

.feedback-title .q-icon {
  color: #2563eb;
}

.feedback-block p {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
}

@media (max-width: 1100px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .score-form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .detail-score-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 850px) {
  .performance-page {
    padding: 18px;
  }

  .page-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .filter-toolbar {
    flex-wrap: wrap;
  }

  .search-field {
    flex-basis: 100%;
  }

  .filter-field {
    flex: 1 1 180px;
  }

  .form-grid,
  .feedback-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .performance-page {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 25px;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .summary-card {
    min-height: 100px;
  }

  .score-form-grid {
    grid-template-columns: 1fr;
  }

  .detail-score-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .details-summary {
    flex-direction: column;
    align-items: stretch;
  }

  .detail-meta {
    justify-content: flex-start;
  }

  .overall-score {
    text-align: left;
  }
}

body.body--dark .performance-page {
  background: #0f172a;
}

body.body--dark .summary-card,
body.body--dark .content-card,
body.body--dark .detail-score {
  background: #111c2e;
  border-color: #263449;
}

body.body--dark .page-header h1,
body.body--dark .summary-content strong,
body.body--dark .employee-name,
body.body--dark .rating-cell strong,
body.body--dark .dialog-title,
body.body--dark .detail-score strong {
  color: #f1f5f9;
}

body.body--dark .page-header p,
body.body--dark .summary-content span,
body.body--dark .summary-content small,
body.body--dark .employee-id,
body.body--dark .dialog-subtitle,
body.body--dark .dialog-eyebrow,
body.body--dark .eyebrow {
  color: #94a3b8;
}

body.body--dark .filter-toolbar,
body.body--dark .performance-table :deep(th) {
  border-color: #263449;
  background: #0f1929;
}

body.body--dark .performance-table :deep(td) {
  color: #cbd5e1;
}

body.body--dark .period-chip {
  background: #1e293b;
  color: #cbd5e1;
}

body.body--dark .score-mini-grid span,
body.body--dark .feedback-block,
body.body--dark .details-summary {
  background: #172337;
}

body.body--dark .feedback-title,
body.body--dark .section-title {
  color: #e2e8f0;
}

body.body--dark .feedback-block p,
body.body--dark .detail-date,
body.body--dark .score-label {
  color: #94a3b8;
}

</style>
