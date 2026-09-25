<template>
  <q-page class="tasks-page">
    <div class="page-container">

      <!-- ==================== PAGE HEADER ==================== -->
      <div class="page-header">
        <div>
          <div class="eyebrow">
            WORKSPACE
          </div>

          <h1 class="page-title">
            Tasks
          </h1>

          <p class="page-subtitle">
            Manage work, track progress and monitor productivity.
          </p>
        </div>

        <div class="header-actions">
          <q-btn
            flat
            round
            icon="refresh"
            :loading="loading"
            class="header-icon-btn"
            @click="loadTasks"
          >
            <q-tooltip>
              Refresh tasks
            </q-tooltip>
          </q-btn>

          <q-btn
            v-if="canManage"
            unelevated
            no-caps
            icon="add"
            label="Create Task"
            class="create-btn"
            @click="openCreateDialog"
          />
        </div>
      </div>

      <!-- ==================== SUMMARY ==================== -->
      <div class="summary-grid">

        <div class="summary-card">
          <div class="summary-icon summary-icon--blue">
            <q-icon name="task_alt" />
          </div>

          <div>
            <div class="summary-label">
              Total Tasks
            </div>

            <div class="summary-value">
              {{ summary.total }}
            </div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon summary-icon--orange">
            <q-icon name="pending_actions" />
          </div>

          <div>
            <div class="summary-label">
              In Progress
            </div>

            <div class="summary-value">
              {{ summary.inProgress }}
            </div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon summary-icon--green">
            <q-icon name="check_circle" />
          </div>

          <div>
            <div class="summary-label">
              Completed
            </div>

            <div class="summary-value">
              {{ summary.completed }}
            </div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon summary-icon--red">
            <q-icon name="priority_high" />
          </div>

          <div>
            <div class="summary-label">
              High Priority
            </div>

            <div class="summary-value">
              {{ summary.highPriority }}
            </div>
          </div>
        </div>

      </div>

      <!-- ==================== ERROR ==================== -->
      <q-banner
        v-if="errorMessage"
        rounded
        class="error-banner"
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
            label="Retry"
            color="negative"
            @click="loadTasks"
          />
        </template>
      </q-banner>

      <!-- ==================== FILTER CARD ==================== -->
      <q-card
        flat
        bordered
        class="filter-card"
      >
        <div class="filter-row">

          <q-input
            v-model="search"
            outlined
            dense
            clearable
            class="task-search"
            placeholder="Search tasks, employees or IDs..."
          >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <q-select
            v-model="statusFilter"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="statusOptions"
            label="Status"
            class="filter-select"
          />

          <q-select
            v-model="priorityFilter"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="priorityOptions"
            label="Priority"
            class="filter-select"
          />

          <q-select
            v-model="departmentFilter"
            outlined
            dense
            clearable
            emit-value
            map-options
            :options="departmentOptions"
            label="Department"
            class="filter-select"
          />

          <q-btn
            v-if="hasActiveFilters"
            flat
            no-caps
            icon="filter_alt_off"
            label="Clear"
            class="clear-filter-btn"
            @click="clearFilters"
          />

        </div>
      </q-card>

      <!-- ==================== TASK TABLE ==================== -->
      <q-card
        flat
        bordered
        class="tasks-card"
      >

        <div class="table-header">
          <div>
            <div class="table-title">
              Task List
            </div>

            <div class="table-caption">
              {{ filteredTasks.length }} task{{ filteredTasks.length === 1 ? '' : 's' }} shown
            </div>
          </div>
        </div>

        <q-separator />

        <q-table
          flat
          :rows="filteredTasks"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          class="tasks-table"
          no-data-label="No tasks found"
          loading-label="Loading tasks..."
          :rows-per-page-options="[10, 20, 50]"
        >

          <!-- Task -->
          <template #body-cell-title="props">
            <q-td :props="props">
              <div class="task-title-cell">
                <div class="task-title">
                  {{ props.row.title }}
                </div>

                <div
                  v-if="props.row.description"
                  class="task-description"
                >
                  {{ props.row.description }}
                </div>
              </div>
            </q-td>
          </template>

          <!-- Employee -->
          <template #body-cell-employee="props">
            <q-td :props="props">
              <div class="employee-cell">
                <q-avatar
                  size="34px"
                  class="employee-avatar"
                >
                  {{ getInitials(props.row.employee_name) }}
                </q-avatar>

                <div>
                  <div class="employee-name">
                    {{ props.row.employee_name }}
                  </div>

                  <div class="employee-id">
                    {{ props.row.employee_id }}
                  </div>
                </div>
              </div>
            </q-td>
          </template>

          <!-- Priority -->
          <template #body-cell-priority="props">
            <q-td :props="props">
              <q-badge
                rounded
                :class="priorityClass(props.row.priority)"
              >
                {{ formatStatus(props.row.priority) }}
              </q-badge>
            </q-td>
          </template>

          <!-- Status -->
          <template #body-cell-status="props">
            <q-td :props="props">
              <q-badge
                rounded
                :class="statusClass(props.row.status)"
              >
                {{ formatStatus(props.row.status) }}
              </q-badge>
            </q-td>
          </template>

          <!-- Due date -->
          <template #body-cell-due_date="props">
            <q-td :props="props">
              <div
                v-if="props.row.due_date"
                :class="dueDateClass(props.row)"
              >
                <q-icon
                  name="event"
                  size="15px"
                />

                {{ formatDate(props.row.due_date) }}
              </div>

              <span
                v-else
                class="muted-text"
              >
                No due date
              </span>
            </q-td>
          </template>

          <!-- Hours -->
          <template #body-cell-hours="props">
            <q-td :props="props">
              <div class="hours-cell">
                <span>
                  {{ props.row.actual_hours ?? 0 }}
                </span>

                <span class="hours-separator">
                  /
                </span>

                <span class="hours-estimated">
                  {{ props.row.estimated_hours ?? 0 }}h
                </span>
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
                  class="table-action"
                  @click="openDetailsDialog(props.row)"
                >
                  <q-tooltip>
                    View task
                  </q-tooltip>
                </q-btn>

                <q-btn
                  v-if="canManage"
                  flat
                  round
                  dense
                  icon="edit"
                  class="table-action"
                  @click="openEditDialog(props.row)"
                >
                  <q-tooltip>
                    Edit task
                  </q-tooltip>
                </q-btn>

                <q-btn
                  v-if="canDelete"
                  flat
                  round
                  dense
                  icon="delete_outline"
                  class="table-action table-action--danger"
                  @click="confirmDelete(props.row)"
                >
                  <q-tooltip>
                    Delete task
                  </q-tooltip>
                </q-btn>

              </div>
            </q-td>
          </template>

          <!-- Empty -->
          <template #no-data>
            <div class="empty-state">
              <div class="empty-icon">
                <q-icon name="task_alt" />
              </div>

              <div class="empty-title">
                No tasks found
              </div>

              <div class="empty-text">
                Try changing your search or filters.
              </div>

              <q-btn
                v-if="canManage"
                unelevated
                no-caps
                icon="add"
                label="Create Task"
                class="empty-action"
                @click="openCreateDialog"
              />
            </div>
          </template>

        </q-table>
      </q-card>

    </div>

    <!-- ==================== CREATE / EDIT DIALOG ==================== -->
    <q-dialog
      v-model="taskDialog"
      persistent
      transition-show="scale"
      transition-hide="scale"
    >
      <q-card class="task-dialog">

        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">
              {{ editingTask ? 'Edit Task' : 'Create Task' }}
            </div>

            <div class="dialog-caption">
              {{ editingTask
                ? 'Update task details and progress.'
                : 'Assign and schedule a new task.' }}
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            @click="closeTaskDialog"
          />
        </q-card-section>

        <q-separator />

        <q-card-section class="dialog-body">

          <q-input
            v-model="taskForm.title"
            outlined
            label="Task Title *"
            maxlength="200"
            counter
            :error="!!formErrors.title"
            :error-message="formErrors.title"
            class="dialog-field"
          />

          <q-input
            v-model="taskForm.description"
            outlined
            type="textarea"
            autogrow
            label="Description"
            class="dialog-field"
          />

          <div class="form-grid">

            <q-select
              v-if="canManage"
              v-model="taskForm.assigned_to"
              outlined
              emit-value
              map-options
              :options="employeeOptions"
              label="Assign Employee *"
              :error="!!formErrors.assigned_to"
              :error-message="formErrors.assigned_to"
            />

            <q-select
              v-model="taskForm.priority"
              outlined
              emit-value
              map-options
              :options="priorityOptions"
              label="Priority"
            />

            <q-select
              v-model="taskForm.status"
              outlined
              emit-value
              map-options
              :options="editableStatusOptions"
              label="Status"
            />

            <q-input
              v-model="taskForm.start_date"
              outlined
              type="date"
              label="Start Date"
            />

            <q-input
              v-model="taskForm.due_date"
              outlined
              type="date"
              label="Due Date"
              :error="!!formErrors.due_date"
              :error-message="formErrors.due_date"
            />

            <q-input
              v-model.number="taskForm.estimated_hours"
              outlined
              type="number"
              min="0"
              step="0.5"
              label="Estimated Hours"
            />

            <q-input
              v-model.number="taskForm.actual_hours"
              outlined
              type="number"
              min="0"
              step="0.5"
              label="Actual Hours"
            />

          </div>

        </q-card-section>

        <q-separator />

        <q-card-actions
          align="right"
          class="dialog-actions"
        >
          <q-btn
            flat
            no-caps
            label="Cancel"
            @click="closeTaskDialog"
          />

          <q-btn
            unelevated
            no-caps
            :label="editingTask ? 'Save Changes' : 'Create Task'"
            :loading="saving"
            class="dialog-save-btn"
            @click="saveTask"
          />
        </q-card-actions>

      </q-card>
    </q-dialog>

    <!-- ==================== DETAILS DIALOG ==================== -->
    <q-dialog
      v-model="detailsDialog"
    >
      <q-card
        v-if="selectedTask"
        class="details-dialog"
      >

        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">
              Task Details
            </div>

            <div class="dialog-caption">
              Task #{{ selectedTask.id }}
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            @click="detailsDialog = false"
          />
        </q-card-section>

        <q-separator />

        <q-card-section>

          <div class="details-title">
            {{ selectedTask.title }}
          </div>

          <div
            v-if="selectedTask.description"
            class="details-description"
          >
            {{ selectedTask.description }}
          </div>

          <div class="details-badges">
            <q-badge
              rounded
              :class="priorityClass(selectedTask.priority)"
            >
              {{ formatStatus(selectedTask.priority) }}
            </q-badge>

            <q-badge
              rounded
              :class="statusClass(selectedTask.status)"
            >
              {{ formatStatus(selectedTask.status) }}
            </q-badge>
          </div>

          <div class="details-grid">

            <div class="detail-item">
              <div class="detail-label">
                Assigned To
              </div>

              <div class="detail-value">
                {{ selectedTask.employee_name }}
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Employee ID
              </div>

              <div class="detail-value">
                {{ selectedTask.employee_id }}
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Department
              </div>

              <div class="detail-value">
                {{ selectedTask.department_name || '—' }}
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Start Date
              </div>

              <div class="detail-value">
                {{ formatDate(selectedTask.start_date) }}
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Due Date
              </div>

              <div class="detail-value">
                {{ formatDate(selectedTask.due_date) }}
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Hours
              </div>

              <div class="detail-value">
                {{ selectedTask.actual_hours ?? 0 }}
                /
                {{ selectedTask.estimated_hours ?? 0 }}h
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-label">
                Completed At
              </div>

              <div class="detail-value">
                {{ formatDateTime(selectedTask.completed_at) }}
              </div>
            </div>

          </div>

        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn
            flat
            no-caps
            label="Close"
            @click="detailsDialog = false"
          />

          <q-btn
            v-if="canManage"
            unelevated
            no-caps
            icon="edit"
            label="Edit Task"
            class="dialog-save-btn"
            @click="openEditFromDetails"
          />
        </q-card-actions>

      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

export default {
  name: 'TasksPage',

  data () {
    return {
      loading: false,
      saving: false,

      errorMessage: '',

      tasks: [],
      employees: [],
      departments: [],

      search: '',
      statusFilter: null,
      priorityFilter: null,
      departmentFilter: null,

      taskDialog: false,
      detailsDialog: false,

      editingTask: null,
      selectedTask: null,

      taskForm: this.emptyTaskForm(),

      formErrors: {},

      pagination: {
        page: 1,
        rowsPerPage: 10
      },

      statusOptions: [
        {
          label: 'To Do',
          value: 'TODO'
        },
        {
          label: 'In Progress',
          value: 'IN_PROGRESS'
        },
        {
          label: 'Review',
          value: 'REVIEW'
        },
        {
          label: 'Completed',
          value: 'COMPLETED'
        },
        {
          label: 'Cancelled',
          value: 'CANCELLED'
        }
      ],

      editableStatusOptions: [
        {
          label: 'To Do',
          value: 'TODO'
        },
        {
          label: 'In Progress',
          value: 'IN_PROGRESS'
        },
        {
          label: 'Review',
          value: 'REVIEW'
        },
        {
          label: 'Completed',
          value: 'COMPLETED'
        },
        {
          label: 'Cancelled',
          value: 'CANCELLED'
        }
      ],

      priorityOptions: [
        {
          label: 'Low',
          value: 'LOW'
        },
        {
          label: 'Medium',
          value: 'MEDIUM'
        },
        {
          label: 'High',
          value: 'HIGH'
        },
        {
          label: 'Urgent',
          value: 'URGENT'
        }
      ],

      columns: [
        {
          name: 'title',
          label: 'TASK',
          align: 'left',
          field: 'title',
          sortable: true,
          style: 'min-width: 260px'
        },
        {
          name: 'employee',
          label: 'ASSIGNED TO',
          align: 'left',
          field: 'employee_name',
          sortable: true,
          style: 'min-width: 190px'
        },
        {
          name: 'department',
          label: 'DEPARTMENT',
          align: 'left',
          field: 'department_name',
          sortable: true
        },
        {
          name: 'priority',
          label: 'PRIORITY',
          align: 'left',
          field: 'priority',
          sortable: true
        },
        {
          name: 'status',
          label: 'STATUS',
          align: 'left',
          field: 'status',
          sortable: true
        },
        {
          name: 'due_date',
          label: 'DUE DATE',
          align: 'left',
          field: 'due_date',
          sortable: true
        },
        {
          name: 'hours',
          label: 'HOURS',
          align: 'left',
          field: row => row.actual_hours,
          sortable: true
        },
        {
          name: 'actions',
          label: '',
          align: 'right',
          field: 'actions',
          sortable: false
        }
      ]
    }
  },

  computed: {
    currentUser () {
      return this.$store.getters.currentUser
    },

    role () {
      return String(
        this.$store.getters.userRole || ''
      ).toUpperCase()
    },

    canManage () {
      return (
        this.role === 'ADMIN' ||
        this.role === 'MANAGER'
      )
    },

    canDelete () {
      return this.role === 'ADMIN'
    },

    summary () {
      return {
        total: this.tasks.length,

        inProgress: this.tasks.filter(
          task => task.status === 'IN_PROGRESS'
        ).length,

        completed: this.tasks.filter(
          task => task.status === 'COMPLETED'
        ).length,

        highPriority: this.tasks.filter(
          task =>
            task.priority === 'HIGH' ||
            task.priority === 'URGENT'
        ).length
      }
    },

    departmentOptions () {
      return this.departments.map(department => ({
        label: department.name,
        value: department.id
      }))
    },

    employeeOptions () {
      return this.employees
        .filter(employee => employee.status !== 'INACTIVE')
        .map(employee => ({
          label: `${this.employeeDisplayName(employee)} (${employee.employee_id})`,
          value: employee.id
        }))
    },

    hasActiveFilters () {
      return Boolean(
        this.search ||
        this.statusFilter ||
        this.priorityFilter ||
        this.departmentFilter
      )
    },

    filteredTasks () {
      let result = [...this.tasks]

      const search = this.search
        .trim()
        .toLowerCase()

      if (search) {
        result = result.filter(task => {
          return [
            task.title,
            task.description,
            task.employee_name,
            task.employee_id,
            task.department_name
          ]
            .filter(Boolean)
            .some(value =>
              String(value)
                .toLowerCase()
                .includes(search)
            )
        })
      }

      if (this.statusFilter) {
        result = result.filter(
          task => task.status === this.statusFilter
        )
      }

      if (this.priorityFilter) {
        result = result.filter(
          task => task.priority === this.priorityFilter
        )
      }

      if (this.departmentFilter) {
        result = result.filter(
          task => {
            const department = this.departments.find(
              item => item.id === this.departmentFilter
            )

            return (
              department &&
              task.department_name === department.name
            )
          }
        )
      }

      return result
    }
  },

  mounted () {
    this.loadInitialData()
  },

  methods: {
    emptyTaskForm () {
      return {
        title: '',
        description: '',
        assigned_to: null,
        priority: 'MEDIUM',
        status: 'TODO',
        start_date: '',
        due_date: '',
        estimated_hours: null,
        actual_hours: 0
      }
    },

    getAuthConfig () {
      const token =
        localStorage.getItem('access_token') ||
        localStorage.getItem('access')

      return {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    },

    async loadInitialData () {
      await Promise.all([
        this.loadTasks(),
        this.loadEmployees(),
        this.loadDepartments()
      ])
    },

    async loadTasks () {
      this.loading = true
      this.errorMessage = ''

      try {
        const response = await axios.get(
          `${API_BASE_URL}/tasks/`,
          this.getAuthConfig()
        )

        this.tasks = this.normalizeResponse(
          response.data
        )
      } catch (error) {
        console.error(
          'Failed to load tasks:',
          error
        )

        this.errorMessage =
          this.getErrorMessage(
            error,
            'Unable to load tasks.'
          )
      } finally {
        this.loading = false
      }
    },

    async loadEmployees () {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/employees/`,
          this.getAuthConfig()
        )

        this.employees = this.normalizeResponse(
          response.data
        )
      } catch (error) {
        console.error(
          'Failed to load employees:',
          error
        )
      }
    },

    async loadDepartments () {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/departments/`,
          this.getAuthConfig()
        )

        this.departments = this.normalizeResponse(
          response.data
        )
      } catch (error) {
        console.error(
          'Failed to load departments:',
          error
        )
      }
    },

    normalizeResponse (data) {
      if (Array.isArray(data)) {
        return data
      }

      if (Array.isArray(data?.results)) {
        return data.results
      }

      return []
    },

    employeeDisplayName (employee) {
      const fullName = employee.full_name ||
        `${employee.first_name || ''} ${employee.last_name || ''}`.trim()

      return fullName ||
        employee.username ||
        employee.employee_id ||
        'Employee'
    },

    openCreateDialog () {
      this.editingTask = null
      this.formErrors = {}
      this.taskForm = this.emptyTaskForm()
      this.taskDialog = true
    },

    openEditDialog (task) {
      this.editingTask = task
      this.formErrors = {}

      this.taskForm = {
        title: task.title || '',
        description: task.description || '',
        assigned_to: task.assigned_to || null,
        priority: task.priority || 'MEDIUM',
        status: task.status || 'TODO',
        start_date: task.start_date || '',
        due_date: task.due_date || '',
        estimated_hours: task.estimated_hours !== null
          ? Number(task.estimated_hours)
          : null,
        actual_hours: task.actual_hours !== null
          ? Number(task.actual_hours)
          : 0
      }

      this.taskDialog = true
    },

    openDetailsDialog (task) {
      this.selectedTask = task
      this.detailsDialog = true
    },

    openEditFromDetails () {
      const task = this.selectedTask

      this.detailsDialog = false

      if (task) {
        this.openEditDialog(task)
      }
    },

    closeTaskDialog () {
      if (this.saving) {
        return
      }

      this.taskDialog = false
      this.editingTask = null
      this.formErrors = {}
    },

    validateForm () {
      const errors = {}

      if (!this.taskForm.title.trim()) {
        errors.title = 'Task title is required.'
      }

      if (
        this.canManage &&
        !this.taskForm.assigned_to
      ) {
        errors.assigned_to =
          'Please select an employee.'
      }

      if (
        this.taskForm.start_date &&
        this.taskForm.due_date &&
        this.taskForm.due_date <
          this.taskForm.start_date
      ) {
        errors.due_date =
          'Due date cannot be earlier than start date.'
      }

      if (
        this.taskForm.estimated_hours !== null &&
        Number(this.taskForm.estimated_hours) < 0
      ) {
        errors.estimated_hours =
          'Estimated hours cannot be negative.'
      }

      if (
        this.taskForm.actual_hours !== null &&
        Number(this.taskForm.actual_hours) < 0
      ) {
        errors.actual_hours =
          'Actual hours cannot be negative.'
      }

      this.formErrors = errors

      return Object.keys(errors).length === 0
    },

    async saveTask () {
      if (!this.validateForm()) {
        return
      }

      this.saving = true

      try {
        const payload = {
          title: this.taskForm.title.trim(),
          description:
            this.taskForm.description?.trim() || '',
          priority: this.taskForm.priority,
          status: this.taskForm.status,
          start_date:
            this.taskForm.start_date || null,
          due_date:
            this.taskForm.due_date || null,
          estimated_hours:
            this.taskForm.estimated_hours === null ||
            this.taskForm.estimated_hours === ''
              ? null
              : Number(this.taskForm.estimated_hours),
          actual_hours:
            this.taskForm.actual_hours === null ||
            this.taskForm.actual_hours === ''
              ? 0
              : Number(this.taskForm.actual_hours)
        }

        if (this.canManage) {
          payload.assigned_to =
            this.taskForm.assigned_to
        }

        let response

        if (this.editingTask) {
          response = await axios.patch(
            `${API_BASE_URL}/tasks/${this.editingTask.id}/`,
            payload,
            this.getAuthConfig()
          )

          this.$q.notify({
            type: 'positive',
            message: 'Task updated successfully.',
            position: 'top-right'
          })
        } else {
          response = await axios.post(
            `${API_BASE_URL}/tasks/`,
            payload,
            this.getAuthConfig()
          )

          this.$q.notify({
            type: 'positive',
            message: 'Task created successfully.',
            position: 'top-right'
          })
        }

        const savedTask = response.data

        if (this.editingTask) {
          const index = this.tasks.findIndex(
            task => task.id === savedTask.id
          )

          if (index !== -1) {
            this.tasks.splice(index, 1, savedTask)
          }
        } else {
          this.tasks.unshift(savedTask)
        }

        this.taskDialog = false
        this.editingTask = null
      } catch (error) {
        console.error(
          'Failed to save task:',
          error
        )

        if (error.response?.data) {
          const data = error.response.data

          if (typeof data === 'object') {
            this.formErrors = {
              ...this.formErrors,
              ...this.flattenFormErrors(data)
            }
          }
        }

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Unable to save task.'
          ),
          position: 'top-right'
        })
      } finally {
        this.saving = false
      }
    },

    confirmDelete (task) {
      this.$q
        .dialog({
          title: 'Delete Task?',
          message:
            `Are you sure you want to delete "${task.title}"?`,
          cancel: {
            label: 'Cancel',
            flat: true
          },
          ok: {
            label: 'Delete',
            color: 'negative',
            unelevated: true
          },
          persistent: true
        })
        .onOk(() => {
          this.deleteTask(task)
        })
    },

    async deleteTask (task) {
      try {
        await axios.delete(
          `${API_BASE_URL}/tasks/${task.id}/`,
          this.getAuthConfig()
        )

        this.tasks = this.tasks.filter(
          item => item.id !== task.id
        )

        this.$q.notify({
          type: 'positive',
          message: 'Task deleted successfully.',
          position: 'top-right'
        })
      } catch (error) {
        console.error(
          'Failed to delete task:',
          error
        )

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Unable to delete task.'
          ),
          position: 'top-right'
        })
      }
    },

    clearFilters () {
      this.search = ''
      this.statusFilter = null
      this.priorityFilter = null
      this.departmentFilter = null
    },

    formatStatus (value) {
      if (!value) {
        return '—'
      }

      return String(value)
        .toLowerCase()
        .replace(/_/g, ' ')
        .replace(/\b\w/g, letter =>
          letter.toUpperCase()
        )
    },

    formatDate (value) {
      if (!value) {
        return '—'
      }

      const date = new Date(`${value}T00:00:00`)

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
    },

    formatDateTime (value) {
      if (!value) {
        return 'Not completed'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleString(
        'en-US',
        {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          hour: 'numeric',
          minute: '2-digit'
        }
      )
    },

    dueDateClass (task) {
      if (
        task.status === 'COMPLETED' ||
        !task.due_date
      ) {
        return 'due-date'
      }

      const today = new Date()
      today.setHours(0, 0, 0, 0)

      const due = new Date(
        `${task.due_date}T00:00:00`
      )

      if (due < today) {
        return 'due-date due-date--overdue'
      }

      return 'due-date'
    },

    statusClass (status) {
      return `status-badge status-badge--${String(status || '').toLowerCase()}`
    },

    priorityClass (priority) {
      return `priority-badge priority-badge--${String(priority || '').toLowerCase()}`
    },

    getInitials (name) {
      if (!name) {
        return 'U'
      }

      const parts = String(name)
        .trim()
        .split(/\s+/)

      if (parts.length === 1) {
        return parts[0]
          .charAt(0)
          .toUpperCase()
      }

      return (
        parts[0].charAt(0) +
        parts[parts.length - 1].charAt(0)
      ).toUpperCase()
    },

    flattenFormErrors (data) {
      const result = {}

      Object.keys(data).forEach(key => {
        const value = data[key]

        if (Array.isArray(value)) {
          result[key] = value[0]
        } else if (
          typeof value === 'string'
        ) {
          result[key] = value
        }
      })

      return result
    },

    getErrorMessage (error, fallback) {
      const data = error?.response?.data

      if (typeof data?.detail === 'string') {
        return data.detail
      }

      if (
        data &&
        typeof data === 'object'
      ) {
        const firstKey = Object.keys(data)[0]

        if (firstKey) {
          const value = data[firstKey]

          if (Array.isArray(value)) {
            return value[0]
          }

          if (typeof value === 'string') {
            return value
          }
        }
      }

      return fallback
    }
  }
}
</script>

<style scoped>
.tasks-page {
  min-height: 100vh;
  background: #f5f7fb;
}

.page-container {
  max-width: 1500px;
  margin: 0 auto;
  padding: 28px 30px 42px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}

.eyebrow {
  margin-bottom: 6px;
  color: #6b7a90;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.2px;
}

.page-title {
  margin: 0;
  color: #172033;
  font-size: 28px;
  font-weight: 800;
  line-height: 1.15;
}

.page-subtitle {
  margin: 7px 0 0;
  color: #7c889b;
  font-size: 13px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon-btn {
  color: #637186;
}

.create-btn {
  min-height: 42px;
  padding: 0 17px;
  border-radius: 10px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 13px;
  min-height: 96px;
  padding: 17px;
  border: 1px solid #e7ecf3;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
}

.summary-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 12px;
  font-size: 21px;
}

.summary-icon--blue {
  background: #edf3ff;
  color: #2563eb;
}

.summary-icon--orange {
  background: #fff6e7;
  color: #d97706;
}

.summary-icon--green {
  background: #eafaf1;
  color: #16a34a;
}

.summary-icon--red {
  background: #fff0f0;
  color: #dc2626;
}

.summary-label {
  color: #7c889b;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.summary-value {
  margin-top: 5px;
  color: #172033;
  font-size: 23px;
  font-weight: 800;
}

.error-banner {
  margin-bottom: 16px;
  border: 1px solid #fecaca;
  background: #fff7f7;
  color: #991b1b;
}

.filter-card {
  margin-bottom: 16px;
  padding: 13px;
  border-color: #e7ecf3;
  border-radius: 14px;
  background: #ffffff;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-search {
  flex: 1;
  min-width: 260px;
}

.filter-select {
  width: 170px;
}

.clear-filter-btn {
  color: #64748b;
}

.tasks-card {
  overflow: hidden;
  border-color: #e7ecf3;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.035);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 76px;
  padding: 16px 20px;
}

.table-title {
  color: #172033;
  font-size: 15px;
  font-weight: 800;
}

.table-caption {
  margin-top: 3px;
  color: #8a96a7;
  font-size: 10px;
}

.tasks-table :deep(thead tr) {
  background: #fafbfd;
}

.tasks-table :deep(th) {
  height: 48px;
  color: #8290a3;
  font-size: 9.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.tasks-table :deep(td) {
  height: 66px;
  color: #445268;
  font-size: 12px;
  border-color: #edf1f5;
}

.task-title {
  max-width: 320px;
  overflow: hidden;
  color: #1e293b;
  font-size: 12.5px;
  font-weight: 750;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-description {
  max-width: 320px;
  margin-top: 4px;
  overflow: hidden;
  color: #8a96a7;
  font-size: 10px;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 9px;
}

.employee-avatar {
  background: #edf3ff;
  color: #315dcc;
  font-size: 11px;
  font-weight: 800;
}

.employee-name {
  color: #334155;
  font-size: 11.5px;
  font-weight: 700;
}

.employee-id {
  margin-top: 2px;
  color: #94a3b8;
  font-size: 9px;
}

.status-badge,
.priority-badge {
  padding: 5px 8px;
  border-radius: 6px;
  font-size: 9px;
  font-weight: 750;
  letter-spacing: 0.15px;
}

.status-badge--todo {
  background: #f1f5f9;
  color: #64748b;
}

.status-badge--in_progress {
  background: #fff7e8;
  color: #b45309;
}

.status-badge--review {
  background: #f1edff;
  color: #6d3fd4;
}

.status-badge--completed {
  background: #eafaf1;
  color: #15803d;
}

.status-badge--cancelled {
  background: #fff0f0;
  color: #dc2626;
}

.priority-badge--low {
  background: #f1f5f9;
  color: #64748b;
}

.priority-badge--medium {
  background: #edf3ff;
  color: #315dcc;
}

.priority-badge--high {
  background: #fff4e5;
  color: #c2410c;
}

.priority-badge--urgent {
  background: #fff0f0;
  color: #dc2626;
}

.due-date {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #526276;
  font-size: 11px;
  font-weight: 600;
}

.due-date--overdue {
  color: #dc2626;
}

.muted-text {
  color: #a0aaba;
  font-size: 10px;
}

.hours-cell {
  color: #334155;
  font-size: 11px;
  font-weight: 700;
}

.hours-separator {
  margin: 0 3px;
  color: #a0aaba;
}

.hours-estimated {
  color: #94a3b8;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
}

.table-action {
  color: #718096;
}

.table-action:hover {
  background: #edf3ff;
  color: #2563eb;
}

.table-action--danger:hover {
  background: #fff0f0;
  color: #dc2626;
}

.empty-state {
  width: 100%;
  padding: 55px 20px;
  text-align: center;
}

.empty-icon {
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  border-radius: 15px;
  background: #edf3ff;
  color: #2563eb;
  font-size: 25px;
}

.empty-title {
  color: #334155;
  font-size: 14px;
  font-weight: 750;
}

.empty-text {
  margin-top: 5px;
  color: #8a96a7;
  font-size: 11px;
}

.empty-action {
  margin-top: 17px;
  border-radius: 9px;
  background: #2563eb;
  color: #ffffff;
}

.task-dialog,
.details-dialog {
  width: 720px;
  max-width: 95vw;
  border-radius: 16px;
}

.details-dialog {
  width: 650px;
}

.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 18px 20px;
}

.dialog-title {
  color: #172033;
  font-size: 16px;
  font-weight: 800;
}

.dialog-caption {
  margin-top: 4px;
  color: #8a96a7;
  font-size: 10px;
}

.dialog-body {
  max-height: 70vh;
  overflow-y: auto;
  padding: 20px;
}

.dialog-field {
  margin-bottom: 14px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 13px;
}

.dialog-actions {
  padding: 14px 20px;
}

.dialog-save-btn {
  border-radius: 8px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 700;
}

.details-title {
  color: #172033;
  font-size: 20px;
  font-weight: 800;
}

.details-description {
  margin-top: 8px;
  color: #69778b;
  font-size: 12px;
  line-height: 1.55;
}

.details-badges {
  display: flex;
  gap: 7px;
  margin-top: 14px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 13px;
  margin-top: 22px;
}

.detail-item {
  padding: 12px;
  border: 1px solid #edf1f5;
  border-radius: 10px;
  background: #fafbfd;
}

.detail-label {
  color: #8a96a7;
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  margin-top: 5px;
  color: #334155;
  font-size: 11.5px;
  font-weight: 700;
}

/* ==================== DARK MODE ==================== */

:global(.body--dark) .tasks-page {
  background: #0f172a;
}

:global(.body--dark) .page-title,
:global(.body--dark) .summary-value,
:global(.body--dark) .table-title,
:global(.body--dark) .task-title,
:global(.body--dark) .dialog-title,
:global(.body--dark) .details-title {
  color: #f8fafc;
}

:global(.body--dark) .page-subtitle,
:global(.body--dark) .summary-label,
:global(.body--dark) .table-caption,
:global(.body--dark) .task-description,
:global(.body--dark) .dialog-caption {
  color: #8fa0b5;
}

:global(.body--dark) .summary-card,
:global(.body--dark) .filter-card,
:global(.body--dark) .tasks-card {
  background: #111827;
  border-color: #1f2937;
}

:global(.body--dark) .tasks-table :deep(thead tr) {
  background: #172033;
}

:global(.body--dark) .tasks-table :deep(td) {
  color: #c1cad6;
  border-color: #1f2937;
}

:global(.body--dark) .employee-name,
:global(.body--dark) .hours-cell,
:global(.body--dark) .due-date,
:global(.body--dark) .detail-value {
  color: #d5dce6;
}

:global(.body--dark) .employee-id,
:global(.body--dark) .hours-estimated {
  color: #8493a7;
}

:global(.body--dark) .task-dialog,
:global(.body--dark) .details-dialog {
  background: #111827;
  color: #e5e7eb;
}

:global(.body--dark) .detail-item {
  background: #172033;
  border-color: #263348;
}

:global(.body--dark) .details-description {
  color: #a7b3c3;
}

:global(.body--dark) .header-icon-btn,
:global(.body--dark) .clear-filter-btn {
  color: #aeb9c8;
}

/* ==================== RESPONSIVE ==================== */

@media (max-width: 1100px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .filter-row {
    flex-wrap: wrap;
  }

  .task-search {
    flex-basis: 100%;
  }
}

@media (max-width: 700px) {
  .page-container {
    padding: 20px 14px 30px;
  }

  .page-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .create-btn {
    flex: 1;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .filter-select {
    flex: 1;
    min-width: 145px;
  }

  .form-grid,
  .details-grid {
    grid-template-columns: 1fr;
  }

  .tasks-card {
    overflow-x: auto;
  }

  .tasks-table {
    min-width: 1050px;
  }
}
</style>
