  <template>
    <div class="employee-page q-pa-md">
      <!-- Page Header -->
      <div class="row items-center justify-between q-col-gutter-md q-mb-lg">
        <div class="col-12 col-md">
          <div class="row items-center no-wrap">
            <div class="page-icon q-mr-md">
              <q-icon name="groups" size="28px" />
            </div>

            <div>
              <div class="text-h4 text-weight-bold">
                Employees
              </div>

              <div class="text-subtitle2 text-grey-6 q-mt-xs">
                Manage and view your organization's employee directory
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="canCreate"
          class="col-12 col-md-auto"
        >
          <q-btn
            unelevated
            color="primary"
            icon="person_add"
            label="Add Employee"
            no-caps
            class="add-employee-btn q-px-lg"
            to="/add_employee"
          />
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="row q-col-gutter-md q-mb-lg">
        <div class="col-12 col-sm-6 col-md-4">
          <q-card flat bordered class="summary-card">
            <q-card-section class="row items-center no-wrap">
              <div class="summary-icon primary-icon">
                <q-icon name="groups" size="26px" />
              </div>

              <div class="q-ml-md">
                <div class="text-caption text-grey-6">
                  Total Employees
                </div>

                <div class="text-h5 text-weight-bold">
                  {{ rows.length }}
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-sm-6 col-md-4">
          <q-card flat bordered class="summary-card">
            <q-card-section class="row items-center no-wrap">
              <div class="summary-icon positive-icon">
                <q-icon name="check_circle" size="26px" />
              </div>

              <div class="q-ml-md">
                <div class="text-caption text-grey-6">
                  Active Employees
                </div>

                <div class="text-h5 text-weight-bold">
                  {{ activeEmployees }}
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-sm-6 col-md-4">
          <q-card flat bordered class="summary-card">
            <q-card-section class="row items-center no-wrap">
              <div class="summary-icon warning-icon">
                <q-icon name="business" size="26px" />
              </div>

              <div class="q-ml-md">
                <div class="text-caption text-grey-6">
                  Departments
                </div>

                <div class="text-h5 text-weight-bold">
                  {{ departmentCount }}
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Employee Directory -->
      <q-card flat bordered class="employee-table-card">
        <q-card-section class="q-pb-md">
          <div class="row items-center justify-between q-col-gutter-md">
            <div class="col-12 col-lg">
              <div class="text-h6 text-weight-bold">
                Employee Directory
              </div>

              <div class="text-caption text-grey-6 q-mt-xs">
                Showing {{ filteredEmployeeCount }} of {{ rows.length }} employees
              </div>
            </div>
            </div>

            <!-- Search -->
            <div class="col-12 col-sm-6 col-lg-4">
              <q-input
                v-model="filter"
                outlined
                dense
                rounded
                clearable
                placeholder="Search by name, ID, email..."
                class="search-input"
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>

            <!-- Actions -->
<!-- Actions -->
<template v-slot:body-cell-actions="props">
  <q-td :props="props">
    <div class="row justify-end q-gutter-xs">

      <!-- View Details -->
      <q-btn
        flat
        round
        dense
        color="grey-7"
        icon="visibility"
        @click="viewEmployee(props.row.id)"
      >
        <q-tooltip>
          View Employee Details
        </q-tooltip>
      </q-btn>

      <!-- Edit -->
      <q-btn
        v-if="canEdit"
        flat
        round
        dense
        color="primary"
        icon="edit"
        @click="editEmployee(props.row.id)"
      >
        <q-tooltip>
          Edit Employee
        </q-tooltip>
      </q-btn>

      <!-- Delete -->
      <q-btn
        v-if="canDelete"
        flat
        round
        dense
        color="negative"
        icon="delete"
        @click="deleteEmployee(props.row)"
      >
        <q-tooltip>
          Delete Employee
        </q-tooltip>
      </q-btn>

    </div>
  </q-td>
</template>


          <!-- Filters -->
          <div class="row q-col-gutter-sm q-mt-md">
            <div class="col-12 col-sm-6 col-md-3">
              <q-select
                v-model="departmentFilter"
                outlined
                dense
                clearable
                emit-value
                map-options
                :options="departmentOptions"
                label="Department"
                option-label="label"
                option-value="value"
              >
                <template v-slot:prepend>
                  <q-icon name="business" />
                </template>
              </q-select>
            </div>

            <div class="col-12 col-sm-6 col-md-3">
              <q-select
                v-model="statusFilter"
                outlined
                dense
                clearable
                emit-value
                map-options
                :options="statusOptions"
                label="Status"
              >
                <template v-slot:prepend>
                  <q-icon name="verified_user" />
                </template>
              </q-select>
            </div>

            <div class="col-12 col-md-auto flex items-center">
              <q-btn
                v-if="hasActiveFilters"
                flat
                dense
                color="primary"
                icon="filter_alt_off"
                label="Clear Filters"
                no-caps
                @click="clearFilters"
              />
            </div>
          </div>
        </q-card-section>

        <q-separator />

        <!-- Selected Toolbar -->
        <q-card-section
          v-if="canDelete && selectedRows.length > 0"
          class="selected-toolbar"
        >
          <div class="row items-center justify-between">
            <div class="text-body2">
              <q-icon
                name="check_circle"
                color="primary"
                class="q-mr-xs"
              />

              {{ selectedRows.length }}
              employee{{ selectedRows.length === 1 ? '' : 's' }}
              selected
            </div>

            <q-btn
              flat
              color="negative"
              icon="delete"
              label="Delete Selected"
              no-caps
              @click="multiDelete"
            />
          </div>
        </q-card-section>

        <q-table
          flat
          :rows="filteredRows"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :selection="canDelete ? 'multiple' : 'none'"
          v-model:selected="selectedRows"
          :rows-per-page-options="[10, 20, 50]"
          no-data-label="No employees found"
          no-results-label="No matching employees found"
          class="employee-table"
        >
          <!-- Loading -->
          <template v-slot:loading>
            <q-inner-loading showing color="primary">
              <q-spinner-dots
                size="40px"
                color="primary"
              />
            </q-inner-loading>
          </template>

          <!-- Empty State -->
          <template v-slot:no-data>
            <div class="full-width column flex-center q-pa-xl text-grey-6">
              <div class="empty-icon q-mb-md">
                <q-icon
                  name="groups"
                  size="42px"
                />
              </div>

              <div class="text-subtitle1 text-weight-medium">
                No employees found
              </div>

              <div class="text-caption q-mt-xs text-center">
                {{
                  hasActiveFilters
                    ? 'Try changing or clearing your filters.'
                    : 'Employees will appear here once they are added.'
                }}
              </div>

              <q-btn
                v-if="hasActiveFilters"
                flat
                color="primary"
                label="Clear Filters"
                no-caps
                class="q-mt-sm"
                @click="clearFilters"
              />
            </div>
          </template>

          <!-- Employee ID -->
          <template v-slot:body-cell-employee_id="props">
            <q-td :props="props">
              <q-chip
                dense
                square
                outline
                color="primary"
                icon="badge"
              >
                {{ props.row.employee_id || '—' }}
              </q-chip>
            </q-td>
          </template>

          <!-- Employee Name + Picture -->
          <template v-slot:body-cell-full_name="props">
            <q-td :props="props">
              <div class="row items-center no-wrap employee-cell">
                <q-avatar
                  size="44px"
                  class="employee-avatar"
                >
                  <img
                    v-if="getProfilePicture(props.row)"
                    :src="getProfilePicture(props.row)"
                    alt="Employee"
                    @error="handleImageError"
                  />

                  <span v-else>
                    {{ getInitials(getEmployeeName(props.row)) }}
                  </span>
                </q-avatar>

                <div class="q-ml-sm employee-info">
                  <div class="text-weight-medium employee-name">
                    {{ getEmployeeName(props.row) }}
                  </div>

                  <div class="text-caption text-grey-6">
                    @{{ getUsername(props.row) || '—' }}
                  </div>
                </div>
              </div>
            </q-td>
          </template>

          <!-- Department -->
          <template v-slot:body-cell-department_name="props">
            <q-td :props="props">
              <div
                v-if="getDepartmentName(props.row)"
                class="row items-center no-wrap"
              >
                <q-icon
                  name="business"
                  size="18px"
                  color="grey-6"
                  class="q-mr-xs"
                />

                <span>
                  {{ getDepartmentName(props.row) }}
                </span>
              </div>

              <span
                v-else
                class="text-grey-5"
              >
                Not assigned
              </span>
            </q-td>
          </template>

          <!-- Job Title -->
          <template v-slot:body-cell-job_title="props">
            <q-td :props="props">
              <span>
                {{ props.row.job_title || '—' }}
              </span>
            </q-td>
          </template>

          <!-- Contact -->
          <template v-slot:body-cell-contact="props">
            <q-td :props="props">
              <div>
                <div
                  v-if="getEmail(props.row)"
                  class="text-body2 contact-line"
                >
                  <q-icon
                    name="email"
                    size="16px"
                    color="grey-6"
                    class="q-mr-xs"
                  />

                  {{ getEmail(props.row) }}
                </div>

                <div
                  v-if="props.row.phone"
                  class="text-caption text-grey-6 q-mt-xs contact-line"
                >
                  <q-icon
                    name="phone"
                    size="15px"
                    class="q-mr-xs"
                  />

                  {{ props.row.phone }}
                </div>

                <span
                  v-if="!getEmail(props.row) && !props.row.phone"
                  class="text-grey-5"
                >
                  —
                </span>
              </div>
            </q-td>
          </template>

          <!-- Joining Date -->
          <template v-slot:body-cell-joining_date="props">
            <q-td :props="props">
              {{ formatDate(props.row.joining_date) }}
            </q-td>
          </template>

          <!-- Employment Type -->
          <template v-slot:body-cell-employment_type="props">
            <q-td :props="props">
              <q-chip
                v-if="props.row.employment_type"
                dense
                color="grey-2"
                text-color="grey-8"
                icon="work_outline"
              >
                {{ formatEmploymentType(props.row.employment_type) }}
              </q-chip>

              <span
                v-else
                class="text-grey-5"
              >
                —
              </span>
            </q-td>
          </template>

          <!-- Status -->
          <template v-slot:body-cell-status="props">
            <q-td :props="props">
              <q-badge
                rounded
                :color="getStatusColor(props.row.status)"
                :label="formatStatus(props.row.status)"
                class="status-badge"
              />
            </q-td>
          </template>

          <!-- Salary -->
          <template v-slot:body-cell-salary="props">
            <q-td :props="props">
              <span
                v-if="
                  props.row.salary !== null &&
                  props.row.salary !== undefined &&
                  props.row.salary !== ''
                "
                class="text-weight-medium"
              >
                {{ formatSalary(props.row.salary) }}
              </span>

              <span
                v-else
                class="text-grey-5"
              >
                —
              </span>
            </q-td>
          </template>

          <!-- Actions -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div
                v-if="canEdit || canDelete"
                class="row justify-end q-gutter-xs"
              >
                <q-btn
                  v-if="canEdit"
                  flat
                  round
                  dense
                  color="primary"
                  icon="edit"
                  @click="editEmployee(props.row.id)"
                >
                  <q-tooltip>
                    Edit Employee
                  </q-tooltip>
                </q-btn>

                <q-btn
                  v-if="canDelete"
                  flat
                  round
                  dense
                  color="negative"
                  icon="delete"
                  @click="deleteEmployee(props.row)"
                >
                  <q-tooltip>
                    Delete Employee
                  </q-tooltip>
                </q-btn>
              </div>

              <span
                v-else
                class="text-caption text-grey-5"
              >
                View only
              </span>
            </q-td>
          </template>
        </q-table>
      </q-card>
    </div>
  </template>

  <script>
  import EmployeeApi from './employee/employeeClass'

  export default {
    name: 'empl-list',

    data () {
      return {
        rows: [],
        selectedRows: [],
        filter: '',
        departmentFilter: null,
        statusFilter: null,
        loading: false,

        columns: [
          {
            name: 'employee_id',
            label: 'Employee ID',
            field: 'employee_id',
            align: 'left',
            sortable: true
          },
          {
            name: 'full_name',
            label: 'Employee',
            field: 'full_name',
            align: 'left',
            sortable: true
          },
          {
            name: 'department_name',
            label: 'Department',
            field: 'department_name',
            align: 'left',
            sortable: true
          },
          {
            name: 'job_title',
            label: 'Job Title',
            field: 'job_title',
            align: 'left',
            sortable: true
          },
          {
            name: 'contact',
            label: 'Contact',
            field: row => this.getEmail(row) || row.phone || '',
            align: 'left',
            sortable: false
          },
          {
            name: 'joining_date',
            label: 'Joining Date',
            field: 'joining_date',
            align: 'left',
            sortable: true
          },
          {
            name: 'employment_type',
            label: 'Employment',
            field: 'employment_type',
            align: 'left',
            sortable: true
          },
          {
            name: 'status',
            label: 'Status',
            field: 'status',
            align: 'center',
            sortable: true
          },
          {
            name: 'salary',
            label: 'Salary',
            field: 'salary',
            align: 'right',
            sortable: true
          },
          {
            name: 'actions',
            label: 'Actions',
            field: 'actions',
            align: 'right',
            sortable: false
          }
        ]
      }
    },

    computed: {
      canCreate () {
        return (
          this.$store.getters.isAdmin ||
          this.$store.getters.isManager
        )
      },

      canEdit () {
        return (
          this.$store.getters.isAdmin ||
          this.$store.getters.isManager
        )
      },

      canDelete () {
        return this.$store.getters.isAdmin
      },

      activeEmployees () {
        return this.rows.filter(row => {
          const status = String(row.status || '').toUpperCase()

          return (
            status === 'ACTIVE' ||
            status === 'EMPLOYED' ||
            status === ''
          )
        }).length
      },

      departmentCount () {
        const departments = this.rows
          .map(row => this.getDepartmentName(row))
          .filter(Boolean)

        return new Set(departments).size
      },

      departmentOptions () {
        const departments = this.rows
          .map(row => this.getDepartmentName(row))
          .filter(Boolean)

        const uniqueDepartments = [...new Set(departments)]

        return uniqueDepartments
          .sort((a, b) => a.localeCompare(b))
          .map(department => ({
            label: department,
            value: department
          }))
      },

      statusOptions () {
        const statuses = this.rows
          .map(row => String(row.status || '').toUpperCase())
          .filter(Boolean)

        const uniqueStatuses = [...new Set(statuses)]

        return uniqueStatuses
          .sort()
          .map(status => ({
            label: this.formatStatus(status),
            value: status
          }))
      },

      hasActiveFilters () {
        return Boolean(
          this.filter ||
          this.departmentFilter ||
          this.statusFilter
        )
      },

      filteredRows () {
        const search = String(this.filter || '')
          .trim()
          .toLowerCase()

        return this.rows.filter(row => {
          const department = this.getDepartmentName(row)
          const status = String(row.status || '').toUpperCase()

          const searchableText = [
            row.employee_id,
            this.getEmployeeName(row),
            this.getUsername(row),
            this.getEmail(row),
            department,
            row.job_title,
            row.phone,
            row.employment_type
          ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()

          const matchesSearch =
            !search ||
            searchableText.includes(search)

          const matchesDepartment =
            !this.departmentFilter ||
            department === this.departmentFilter

          const matchesStatus =
            !this.statusFilter ||
            status === this.statusFilter

          return (
            matchesSearch &&
            matchesDepartment &&
            matchesStatus
          )
        })
      },

      filteredEmployeeCount () {
        return this.filteredRows.length
      }
    },

    mounted () {
      this.getEmployees()
    },

    methods: {
      async getEmployees () {
        this.loading = true

        try {
          const response = await EmployeeApi.getEmployees()

          if (Array.isArray(response.data)) {
            this.rows = response.data
          } else if (Array.isArray(response.data?.results)) {
            this.rows = response.data.results
          } else {
            this.rows = []
          }

          this.selectedRows = []
        } catch (error) {
          console.error('Error loading employees:', error)

          const message =
            error.response?.data?.detail ||
            error.response?.data?.message ||
            'Failed to load employees'

          this.$q.notify({
            type: 'negative',
            position: 'top',
            message
          })
        } finally {
          this.loading = false
        }
      },

      getEmployeeName (employee) {
        if (!employee) {
          return ''
        }

        if (employee.full_name) {
          return employee.full_name
        }

        if (employee.user?.first_name || employee.user?.last_name) {
          return [
            employee.user?.first_name,
            employee.user?.last_name
          ]
            .filter(Boolean)
            .join(' ')
        }

        return employee.first_name ||
          employee.user?.username ||
          employee.username ||
          ''
      },

      getUsername (employee) {
        return (
          employee?.username ||
          employee?.user?.username ||
          ''
        )
      },

      getEmail (employee) {
        return (
          employee?.email ||
          employee?.user?.email ||
          ''
        )
      },

      getDepartmentName (employee) {
        if (!employee) {
          return ''
        }

        if (employee.department_name) {
          return employee.department_name
        }

        if (typeof employee.department === 'object') {
          return employee.department?.name || ''
        }

        return ''
      },

      getProfilePicture (employee) {
        if (!employee) {
          return ''
        }

        const picture =
          employee.profile_picture ||
          employee.user?.profile_picture ||
          ''

        if (!picture) {
          return ''
        }

        if (typeof picture !== 'string') {
          return ''
        }

        const value = picture.trim()

        if (!value) {
          return ''
        }

        if (
          value.startsWith('http://') ||
          value.startsWith('https://') ||
          value.startsWith('data:')
        ) {
          return value
        }

        const backendUrl = 'http://127.0.0.1:8000'

        if (value.startsWith('/')) {
          return `${backendUrl}${value}`
        }

        return `${backendUrl}/${value}`
      },

      handleImageError (event) {
        if (event?.target) {
          event.target.style.display = 'none'
        }
      },


      viewEmployee (id) {
  if (!id) {
    return
  }

  this.$router.push(`/EmployeeDetails/${id}`)
},


      editEmployee (id) {
        this.$router.push({
          path: '/add_employee',
          query: {
            id
          }
        })
      },

      deleteEmployee (employee) {
        this.$q
          .dialog({
            title: 'Delete Employee',
            message: `Are you sure you want to delete ${this.getEmployeeName(employee) || 'this employee'}?`,
            cancel: {
              label: 'Cancel',
              flat: true
            },
            persistent: true,
            ok: {
              label: 'Delete',
              color: 'negative'
            }
          })
          .onOk(async () => {
            try {
              await EmployeeApi.deleteEmployee(employee.id)

              this.$q.notify({
                type: 'positive',
                position: 'top',
                message: 'Employee deleted successfully'
              })

              await this.getEmployees()
            } catch (error) {
              console.error('Error deleting employee:', error)

              const message =
                error.response?.data?.detail ||
                error.response?.data?.message ||
                'Something went wrong while deleting the employee'

              this.$q.notify({
                type: 'negative',
                position: 'top',
                message
              })
            }
          })
      },

      multiDelete () {
        if (!this.canDelete || !this.selectedRows.length) {
          return
        }

        this.$q
          .dialog({
            title: 'Delete Selected Employees',
            message: `Are you sure you want to delete ${this.selectedRows.length} selected employees?`,
            cancel: {
              label: 'Cancel',
              flat: true
            },
            persistent: true,
            ok: {
              label: 'Delete All',
              color: 'negative'
            }
          })
          .onOk(async () => {
            this.loading = true

            try {
              for (const employee of this.selectedRows) {
                await EmployeeApi.deleteEmployee(employee.id)
              }

              this.$q.notify({
                type: 'positive',
                position: 'top',
                message: 'Selected employees deleted successfully'
              })

              this.selectedRows = []

              await this.getEmployees()
            } catch (error) {
              console.error(
                'Error deleting selected employees:',
                error
              )

              this.$q.notify({
                type: 'negative',
                position: 'top',
                message: 'Failed to delete selected employees'
              })
            } finally {
              this.loading = false
            }
          })
      },

      clearFilters () {
        this.filter = ''
        this.departmentFilter = null
        this.statusFilter = null
      },

      getInitials (name) {
        if (!name) {
          return 'E'
        }

        const words = String(name)
          .trim()
          .split(/\s+/)
          .filter(Boolean)

        if (words.length === 1) {
          return words[0]
            .substring(0, 2)
            .toUpperCase()
        }

        return `${words[0][0]}${words[1][0]}`.toUpperCase()
      },

      formatDate (value) {
        if (!value) {
          return '—'
        }

        const date = new Date(value)

        if (Number.isNaN(date.getTime())) {
          return value
        }

        return date.toLocaleDateString()
      },

      formatEmploymentType (value) {
        if (!value) {
          return '—'
        }

        return String(value)
          .replace(/_/g, ' ')
          .replace(/\b\w/g, char => char.toUpperCase())
      },

      formatStatus (value) {
        if (!value) {
          return 'Active'
        }

        return String(value)
          .replace(/_/g, ' ')
          .replace(/\b\w/g, char => char.toUpperCase())
      },

      getStatusColor (value) {
        const status = String(value || '').toUpperCase()

        if (
          status === 'ACTIVE' ||
          status === 'EMPLOYED'
        ) {
          return 'positive'
        }

        if (
          status === 'INACTIVE' ||
          status === 'TERMINATED' ||
          status === 'RESIGNED'
        ) {
          return 'negative'
        }

        if (
          status === 'ON_LEAVE' ||
          status === 'SUSPENDED'
        ) {
          return 'warning'
        }

        return 'grey-6'
      },

      formatSalary (value) {
        const number = Number(value)

        if (Number.isNaN(number)) {
          return value
        }

        return new Intl.NumberFormat().format(number)
      },

      printTable () {
        window.print()
      }
    }
  }
  </script>

  <style scoped>
  .employee-page {
    max-width: 1600px;
    margin: 0 auto;
  }

  .page-icon {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--q-primary);
    background: rgba(25, 118, 210, 0.1);
  }

  .add-employee-btn {
    min-height: 42px;
    border-radius: 10px;
  }

  .summary-card {
    border-radius: 14px;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .summary-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  }

  .summary-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .primary-icon {
    color: var(--q-primary);
    background: rgba(25, 118, 210, 0.1);
  }

  .positive-icon {
    color: var(--q-positive);
    background: rgba(33, 186, 69, 0.1);
  }

  .warning-icon {
    color: var(--q-warning);
    background: rgba(242, 192, 54, 0.12);
  }

  .employee-table-card {
    border-radius: 14px;
    overflow: hidden;
  }

  .search-input {
    max-width: 100%;
  }

  .selected-toolbar {
    background: rgba(25, 118, 210, 0.05);
  }

  .employee-cell {
    min-width: 190px;
  }

  .employee-avatar {
    flex-shrink: 0;
    background: rgba(25, 118, 210, 0.1);
    color: var(--q-primary);
    font-size: 12px;
    font-weight: 700;
    overflow: hidden;
  }

  .employee-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .employee-info {
    min-width: 0;
  }

  .employee-name {
    max-width: 180px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .contact-line {
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .status-badge {
    padding: 5px 10px;
  }

  .empty-icon {
    width: 76px;
    height: 76px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--q-primary);
    background: rgba(25, 118, 210, 0.08);
  }

  .employee-table {
    min-height: 250px;
  }

  @media (max-width: 700px) {
    .employee-page {
      padding: 8px !important;
    }

    .text-h4 {
      font-size: 1.75rem;
    }

    .page-icon {
      width: 44px;
      height: 44px;
    }

    .employee-table-card {
      border-radius: 10px;
    }

    .employee-cell {
      min-width: 160px;
    }

    .employee-name {
      max-width: 130px;
    }
  }

  @media print {
    .employee-page {
      max-width: none;
      padding: 0 !important;
    }

    .add-employee-btn,
    .search-input,
    .selected-toolbar {
      display: none !important;
    }
  }
  </style>
  s
