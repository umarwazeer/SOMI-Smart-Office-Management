<template>
  <div class="department-page q-pa-md">
    <!-- Page Header -->
    <div class="row items-center justify-between q-col-gutter-md q-mb-lg">
      <div class="col-12 col-md">
        <div class="text-h4 text-weight-bold">Departments</div>
        <div class="text-subtitle2 text-grey-6 q-mt-xs">
          Manage and monitor your organization's departments
        </div>
      </div>

      <div
        v-if="canManage"
        class="col-12 col-md-auto"
      >
        <q-btn
          unelevated
          color="primary"
          icon="add"
          label="Add Department"
          class="q-px-lg"
          no-caps
          @click="openCreateDialog"
        />
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-4">
        <q-card flat bordered class="summary-card">
          <q-card-section class="row items-center no-wrap">
            <div class="summary-icon primary-icon">
              <q-icon name="business" size="26px" />
            </div>

            <div class="q-ml-md">
              <div class="text-caption text-grey-6">
                Total Departments
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
                Active Departments
              </div>
              <div class="text-h5 text-weight-bold">
                {{ activeDepartments }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-4">
        <q-card flat bordered class="summary-card">
          <q-card-section class="row items-center no-wrap">
            <div class="summary-icon warning-icon">
              <q-icon name="groups" size="26px" />
            </div>

            <div class="q-ml-md">
              <div class="text-caption text-grey-6">
                With Assigned Manager
              </div>
              <div class="text-h5 text-weight-bold">
                {{ departmentsWithManager }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Department Table -->
    <q-card flat bordered class="department-table-card">
      <q-card-section class="q-pb-sm">
        <div class="row items-center justify-between q-col-gutter-md">
          <div class="col-12 col-md">
            <div class="text-h6 text-weight-bold">
              Department Directory
            </div>
            <div class="text-caption text-grey-6">
              {{ rows.length }} department{{ rows.length === 1 ? '' : 's' }}
              available
            </div>
          </div>

          <div class="col-12 col-md-4">
            <q-input
              v-model="filter"
              outlined
              dense
              clearable
              placeholder="Search departments..."
              class="search-input"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-section
        v-if="canDelete && selectedRows.length > 0"
        class="selected-toolbar"
      >
        <div class="row items-center justify-between">
          <div class="text-body2">
            <q-icon name="check_circle" class="q-mr-xs" />
            {{ selectedRows.length }} department{{
              selectedRows.length === 1 ? '' : 's'
            }}
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
        :rows="rows"
        :filter="filter"
        :columns="columns"
        row-key="id"
        :selection="canDelete ? 'multiple' : 'none'"
        v-model:selected="selectedRows"
        :loading="loading"
        :rows-per-page-options="[10, 20, 50]"
        no-data-label="No departments found"
        no-results-label="No matching departments found"
      >
        <template v-slot:loading>
          <q-inner-loading showing color="primary" />
        </template>

        <template v-slot:no-data>
          <div class="full-width column flex-center q-pa-xl text-grey-6">
            <q-icon name="business" size="48px" class="q-mb-md" />
            <div class="text-subtitle1 text-weight-medium">
              No departments found
            </div>
            <div class="text-caption q-mt-xs">
              {{
                filter
                  ? 'Try changing your search.'
                  : 'Departments will appear here once they are added.'
              }}
            </div>
          </div>
        </template>

        <template v-slot:body-cell-no="props">
          <q-td :props="props">
            <span class="text-grey-6">
              {{ props.rowIndex + 1 }}
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <div class="department-avatar">
                {{ getDepartmentInitials(props.row.name) }}
              </div>

              <div class="q-ml-sm">
                <div class="text-weight-medium">
                  {{ props.row.name || '—' }}
                </div>

                <div
                  v-if="props.row.description"
                  class="text-caption text-grey-6 department-description"
                >
                  {{ props.row.description }}
                </div>
              </div>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-code="props">
          <q-td :props="props">
            <q-chip
              dense
              square
              outline
              color="primary"
              text-color="primary"
              icon="tag"
            >
              {{ props.row.code || '—' }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-manager_name="props">
          <q-td :props="props">
            <div
              v-if="props.row.manager_name"
              class="row items-center no-wrap"
            >
              <q-icon
                name="person"
                size="18px"
                color="grey-6"
                class="q-mr-xs"
              />
              <span>{{ props.row.manager_name }}</span>
            </div>

            <span v-else class="text-grey-5">
              Not assigned
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-is_active="props">
          <q-td :props="props">
            <q-badge
              rounded
              :color="props.row.is_active ? 'positive' : 'grey-6'"
              :label="props.row.is_active ? 'Active' : 'Inactive'"
              class="status-badge"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-Action="props">
          <q-td :props="props">
            <div
              v-if="canManage || canDelete"
              class="row justify-end q-gutter-xs"
            >
              <q-btn
                v-if="canManage"
                flat
                round
                dense
                color="primary"
                icon="edit"
                @click="openEditDialog(props.row)"
              >
                <q-tooltip>
                  Edit Department
                </q-tooltip>
              </q-btn>

              <q-btn
                v-if="canDelete"
                flat
                round
                dense
                color="negative"
                icon="delete"
                @click="del(props.row.id)"
              >
                <q-tooltip>
                  Delete Department
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

    <!-- Add / Edit Department Dialog -->
    <q-dialog
      v-model="showDepartmentDialog"
      persistent
    >
      <add-dep
        :newDep="newDep"
        :isEditing="isEditing"
        :loading="saving"
        @addDep="addDep"
        @cancel="closeDepartmentDialog"
      />
    </q-dialog>
  </div>
</template>

<script>
import addDep from './addDep.vue'
import DepartmentApi from './api'

export default {
  name: 'list_dep',

  components: {
    addDep
  },

  data () {
    return {
      newDep: {
        id: null,
        name: '',
        code: '',
        description: ''
      },

      filter: '',
      isEditing: false,
      selectedRows: [],

      rows: [],

      loading: false,
      saving: false,
      showDepartmentDialog: false,

      columns: [
        {
          name: 'no',
          required: true,
          label: '#',
          align: 'left',
          field: 'no',
          sortable: false
        },
        {
          name: 'name',
          align: 'left',
          label: 'Department',
          field: 'name',
          sortable: true
        },
        {
          name: 'code',
          align: 'left',
          label: 'Code',
          field: 'code',
          sortable: true
        },
        {
          name: 'manager_name',
          align: 'left',
          label: 'Manager',
          field: 'manager_name',
          sortable: true
        },
        {
          name: 'is_active',
          align: 'center',
          label: 'Status',
          field: 'is_active',
          sortable: true
        },
        {
          name: 'Action',
          align: 'right',
          label: 'Actions',
          field: 'Action',
          sortable: false
        }
      ]
    }
  },

  computed: {
    canManage () {
      return this.$store.getters.isAdmin || this.$store.getters.isManager
    },

    canDelete () {
      return this.$store.getters.isAdmin
    },

    activeDepartments () {
      return this.rows.filter(row => row.is_active !== false).length
    },

    departmentsWithManager () {
      return this.rows.filter(row => !!row.manager_name).length
    }
  },

  mounted () {
    this.getDepartment()
  },

  methods: {
    openCreateDialog () {
      this.resetForm()
      this.isEditing = false
      this.showDepartmentDialog = true
    },

    openEditDialog (department) {
      this.newDep = {
        id: department.id,
        name: department.name || '',
        code: department.code || '',
        description: department.description || ''
      }

      this.isEditing = true
      this.showDepartmentDialog = true
    },

    closeDepartmentDialog () {
      if (this.saving) {
        return
      }

      this.showDepartmentDialog = false
      this.resetForm()
    },

    async addDep () {
      if (this.isEditing) {
        await this.updateDepartment()
      } else {
        await this.createDepartment()
      }
    },

    async getDepartment () {
      this.loading = true

      try {
        const response = await DepartmentApi.getDepartment()

        this.rows = Array.isArray(response.data)
          ? response.data
          : []

        this.selectedRows = []
      } catch (error) {
        console.error('Error loading departments:', error)

        this.$q.notify({
          type: 'negative',
          position: 'top',
          message: 'Failed to load departments'
        })
      } finally {
        this.loading = false
      }
    },

    async createDepartment () {
      this.saving = true

      try {
        const payload = {
          name: this.newDep.name.trim(),
          code: this.newDep.code.trim(),
          description: this.newDep.description.trim()
        }

        const response = await DepartmentApi.createDepartment(payload)

        if (response.status === 201) {
          this.$q.notify({
            type: 'positive',
            position: 'top',
            message: 'Department created successfully'
          })

          this.showDepartmentDialog = false
          this.resetForm()

          await this.getDepartment()
        }
      } catch (error) {
        console.error('Error creating department:', error)

        const message =
          error.response?.data?.detail ||
          this.getValidationMessage(error) ||
          'Something went wrong while creating the department'

        this.$q.notify({
          type: 'negative',
          position: 'top',
          message
        })
      } finally {
        this.saving = false
      }
    },

    async updateDepartment () {
      this.saving = true

      try {
        const payload = {
          name: this.newDep.name.trim(),
          code: this.newDep.code.trim(),
          description: this.newDep.description.trim()
        }

        const response = await DepartmentApi.updateDepartment(
          this.newDep.id,
          payload
        )

        if (response.status === 200) {
          this.$q.notify({
            type: 'positive',
            position: 'top',
            message: 'Department updated successfully'
          })

          this.showDepartmentDialog = false
          this.resetForm()

          await this.getDepartment()
        }
      } catch (error) {
        console.error('Error updating department:', error)

        const message =
          error.response?.data?.detail ||
          this.getValidationMessage(error) ||
          'Something went wrong while updating the department'

        this.$q.notify({
          type: 'negative',
          position: 'top',
          message
        })
      } finally {
        this.saving = false
      }
    },

    del (id) {
      this.$q
        .dialog({
          title: 'Delete Department',
          message: 'Are you sure you want to delete this department?',
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
            await DepartmentApi.deleteDepartment(id)

            this.$q.notify({
              type: 'positive',
              position: 'top',
              message: 'Department deleted successfully'
            })

            await this.getDepartment()
          } catch (error) {
            console.error('Error deleting department:', error)

            const message =
              error.response?.data?.detail ||
              'Something went wrong while deleting the department'

            this.$q.notify({
              type: 'negative',
              position: 'top',
              message
            })
          }
        })
    },

    multiDelete () {
      if (!this.selectedRows.length || !this.canDelete) {
        return
      }

      this.$q
        .dialog({
          title: 'Delete Selected Departments',
          message: `Are you sure you want to delete ${this.selectedRows.length} selected departments?`,
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
          try {
            this.loading = true

            for (const department of this.selectedRows) {
              await DepartmentApi.deleteDepartment(department.id)
            }

            this.$q.notify({
              type: 'positive',
              position: 'top',
              message: 'Selected departments deleted successfully'
            })

            this.selectedRows = []

            await this.getDepartment()
          } catch (error) {
            console.error(
              'Error deleting selected departments:',
              error
            )

            this.$q.notify({
              type: 'negative',
              position: 'top',
              message: 'Failed to delete selected departments'
            })
          } finally {
            this.loading = false
          }
        })
    },

    resetForm () {
      this.newDep = {
        id: null,
        name: '',
        code: '',
        description: ''
      }

      this.isEditing = false
    },

    getDepartmentInitials (name) {
      if (!name) {
        return 'D'
      }

      const words = name
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (words.length === 1) {
        return words[0].substring(0, 2).toUpperCase()
      }

      return `${words[0][0]}${words[1][0]}`.toUpperCase()
    },

    getValidationMessage (error) {
      const data = error.response?.data

      if (!data || typeof data !== 'object') {
        return ''
      }

      const messages = []

      Object.keys(data).forEach(key => {
        const value = data[key]

        if (Array.isArray(value)) {
          messages.push(`${key}: ${value.join(', ')}`)
        } else if (typeof value === 'string') {
          messages.push(`${key}: ${value}`)
        }
      })

      return messages.join(' | ')
    }
  }
}
</script>

<style scoped>
.department-page {
  max-width: 1600px;
  margin: 0 auto;
}

.summary-card {
  border-radius: 14px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
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

.department-table-card {
  border-radius: 14px;
  overflow: hidden;
}

.search-input {
  max-width: 100%;
}

.selected-toolbar {
  background: rgba(25, 118, 210, 0.05);
}

.department-avatar {
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: var(--q-primary);
  font-size: 12px;
  font-weight: 700;
}

.department-description {
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-badge {
  padding: 5px 10px;
}

@media (max-width: 600px) {
  .department-page {
    padding: 8px !important;
  }

  .text-h4 {
    font-size: 1.75rem;
  }

  .department-table-card {
    border-radius: 10px;
  }

  .department-description {
    max-width: 150px;
  }
}
</style>
