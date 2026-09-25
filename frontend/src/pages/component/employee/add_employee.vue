<template>
  <div class="employee-page q-pa-md q-pa-lg-xl">
    <div class="page-header q-mb-lg">
      <div class="row items-center justify-between q-col-gutter-md">
        <div class="col">
          <div class="row items-center no-wrap">
            <q-btn
              flat
              round
              icon="arrow_back"
              color="grey-7"
              class="q-mr-sm"
              :disable="saving"
              @click="goBack"
            />

            <div>
              <div class="text-h4 text-weight-bold text-grey-9">
                {{ isEditMode ? 'Edit Employee' : 'Add Employee' }}
              </div>

              <div class="text-subtitle2 text-grey-6 q-mt-xs">
                {{
                  isEditMode
                    ? 'Update employee profile and employment information'
                    : 'Create a new employee account and profile'
                }}
              </div>
            </div>
          </div>
        </div>

        <div class="col-auto">
          <q-chip
            v-if="isEditMode"
            color="blue-1"
            text-color="blue-9"
            icon="edit"
            class="mode-chip"
          >
            Edit Mode
          </q-chip>

          <q-chip
            v-else
            color="green-1"
            text-color="green-9"
            icon="person_add"
            class="mode-chip"
          >
            New Employee
          </q-chip>
        </div>
      </div>
    </div>

    <q-form
      ref="employeeForm"
      @submit.prevent="saveEmployee"
    >
      <div class="row q-col-gutter-lg">

        <!-- Profile Sidebar -->
        <div class="col-12 col-md-4 col-lg-3">
          <q-card class="som-card profile-card">

            <q-card-section class="profile-section text-center">
              <div class="profile-label">
                Employee Profile
              </div>

              <div class="text-caption text-grey-6 q-mt-xs">
                {{ isEditMode ? 'Update profile photo' : 'Add employee photo' }}
              </div>

              <div class="avatar-wrapper q-mt-lg">
                <q-avatar
                  size="150px"
                  color="blue-1"
                  text-color="primary"
                  class="profile-avatar"
                >
                  <q-img
                    v-if="capturedImage"
                    :src="capturedImage"
                    fit="cover"
                    style="width: 150px; height: 150px;"
                  />

                  <span
                    v-else
                    class="text-h3 text-weight-medium"
                  >
                    {{ initials }}
                  </span>
                </q-avatar>

                <q-btn
                  round
                  unelevated
                  color="primary"
                  icon="photo_camera"
                  class="avatar-button"
                  size="sm"
                  :disable="saving"
                  @click="openFileInput"
                >
                  <q-tooltip>
                    Change profile photo
                  </q-tooltip>
                </q-btn>
              </div>

              <input
                ref="fileInput"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                style="display: none"
                @change="captureImage"
              />

              <q-btn
                outline
                color="primary"
                icon="upload"
                label="Upload Photo"
                no-caps
                class="q-mt-md full-width"
                :disable="saving"
                @click="openFileInput"
              />

              <q-btn
                v-if="selectedImageFile"
                flat
                dense
                color="negative"
                icon="delete_outline"
                label="Remove Selected Photo"
                no-caps
                class="q-mt-xs"
                :disable="saving"
                @click="removeSelectedImage"
              />

              <div class="text-caption text-grey-5 q-mt-sm">
                JPG, PNG or WEBP · Maximum 5 MB
              </div>

              <div
                v-if="selectedImageFile"
                class="photo-status q-mt-md"
              >
                <q-icon
                  name="check_circle"
                  color="positive"
                  size="17px"
                />

                <span>
                  New photo selected
                </span>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="employee-id-box">
                <div class="text-caption text-grey-6">
                  Employee ID
                </div>

                <div class="text-subtitle1 text-weight-bold text-grey-9 q-mt-xs">
                  {{ form.employee_id || 'Not assigned yet' }}
                </div>

                <div
                  v-if="!isEditMode"
                  class="text-caption text-grey-5 q-mt-xs"
                >
                  Enter the employee ID used by your organization.
                </div>

                <div
                  v-else
                  class="text-caption text-grey-5 q-mt-xs"
                >
                  Unique employee identifier.
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section class="text-left">
              <div class="side-info">
                <q-icon
                  name="security"
                  color="primary"
                  size="20px"
                />

                <div>
                  <div class="text-caption text-weight-bold text-grey-8">
                    Account Security
                  </div>

                  <div class="text-caption text-grey-6 q-mt-xs">
                    {{
                      isEditMode
                        ? 'Account credentials are managed separately.'
                        : 'A secure employee account will be created automatically.'
                    }}
                  </div>
                </div>
              </div>
            </q-card-section>

          </q-card>
        </div>

        <!-- Main Form -->
        <div class="col-12 col-md-8 col-lg-9">

          <!-- Personal Information -->
          <q-card class="som-card q-mb-lg">
            <q-card-section>
              <div class="section-title">
                <div class="section-icon">
                  <q-icon
                    name="person"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Personal Information
                  </div>

                  <div class="text-caption text-grey-6">
                    Basic identity and contact information
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="row q-col-gutter-md">

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.first_name"
                    outlined
                    label="First Name"
                    placeholder="Enter first name"
                    :rules="[requiredRule]"
                    lazy-rules
                    :readonly="isEditMode"
                  >
                    <template #prepend>
                      <q-icon name="person_outline" />
                    </template>

                    <template
                      v-if="isEditMode"
                      #append
                    >
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Name is managed through the user account.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.last_name"
                    outlined
                    label="Last Name"
                    placeholder="Enter last name"
                    :rules="[requiredRule]"
                    lazy-rules
                    :readonly="isEditMode"
                  >
                    <template #prepend>
                      <q-icon name="person_outline" />
                    </template>

                    <template
                      v-if="isEditMode"
                      #append
                    >
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Name is managed through the user account.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.username"
                    outlined
                    label="Username"
                    placeholder="Enter username"
                    :rules="[requiredRule]"
                    lazy-rules
                    :readonly="isEditMode"
                  >
                    <template #prepend>
                      <q-icon name="account_circle" />
                    </template>

                    <template
                      v-if="isEditMode"
                      #append
                    >
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Username cannot be changed from Employee API.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.email"
                    outlined
                    type="email"
                    label="Email Address"
                    placeholder="employee@example.com"
                    :rules="[requiredRule, emailRule]"
                    lazy-rules
                    :readonly="isEditMode"
                  >
                    <template #prepend>
                      <q-icon name="email" />
                    </template>

                    <template
                      v-if="isEditMode"
                      #append
                    >
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Email cannot be changed from Employee API.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.phone"
                    outlined
                    label="Phone Number"
                    placeholder="03001234567"
                    :readonly="isEditMode"
                  >
                    <template #prepend>
                      <q-icon name="phone" />
                    </template>

                    <template
                      v-if="isEditMode"
                      #append
                    >
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Phone is stored on the User account.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model="form.date_of_birth"
                    outlined
                    type="date"
                    label="Date of Birth"
                  >
                    <template #prepend>
                      <q-icon name="cake" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12">
                  <q-input
                    v-model.trim="form.address"
                    outlined
                    type="textarea"
                    autogrow
                    label="Address"
                    placeholder="Enter employee address"
                  >
                    <template #prepend>
                      <q-icon name="home" />
                    </template>
                  </q-input>
                </div>

              </div>
            </q-card-section>
          </q-card>

          <!-- Account Security -->
          <q-card
            v-if="!isEditMode"
            class="som-card q-mb-lg"
          >
            <q-card-section>
              <div class="section-title">
                <div class="section-icon security-icon">
                  <q-icon
                    name="lock"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Account Security
                  </div>

                  <div class="text-caption text-grey-6">
                    Set the initial password for the employee account
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <q-banner
                rounded
                class="security-banner q-mb-md"
              >
                <template #avatar>
                  <q-icon
                    name="info"
                    color="primary"
                  />
                </template>

                The employee account will be created with the
                <strong>Employee</strong> role automatically.
              </q-banner>

              <div class="row q-col-gutter-md">

                <div class="col-12 col-md-6">
                  <q-input
                    v-model="form.password"
                    outlined
                    :type="showPassword ? 'text' : 'password'"
                    label="Initial Password"
                    placeholder="Enter secure password"
                    :rules="[passwordRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="lock_outline" />
                    </template>

                    <template #append>
                      <q-btn
                        flat
                        round
                        dense
                        :icon="showPassword ? 'visibility_off' : 'visibility'"
                        color="grey-6"
                        @click="showPassword = !showPassword"
                      />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model="form.password_confirm"
                    outlined
                    :type="showConfirmPassword ? 'text' : 'password'"
                    label="Confirm Password"
                    placeholder="Re-enter password"
                    :rules="[confirmPasswordRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="lock_outline" />
                    </template>

                    <template #append>
                      <q-btn
                        flat
                        round
                        dense
                        :icon="showConfirmPassword ? 'visibility_off' : 'visibility'"
                        color="grey-6"
                        @click="showConfirmPassword = !showConfirmPassword"
                      />
                    </template>
                  </q-input>
                </div>

              </div>
            </q-card-section>
          </q-card>

          <!-- Employment Information -->
          <q-card class="som-card q-mb-lg">
            <q-card-section>
              <div class="section-title">
                <div class="section-icon">
                  <q-icon
                    name="business_center"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Employment Information
                  </div>

                  <div class="text-caption text-grey-6">
                    Department, position and employment details
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="row q-col-gutter-md">

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.employee_id"
                    outlined
                    label="Employee ID"
                    placeholder="e.g. EMP-002"
                    :rules="[requiredRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="badge" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-select
                    v-model="form.department"
                    outlined
                    emit-value
                    map-options
                    :options="departmentOptions"
                    option-value="id"
                    option-label="name"
                    label="Department"
                    placeholder="Select department"
                    :loading="departmentsLoading"
                    :rules="[requiredSelectRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="corporate_fare" />
                    </template>

                    <template #no-option>
                      <q-item>
                        <q-item-section class="text-grey-6">
                          No departments available
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.job_title"
                    outlined
                    label="Job Title"
                    placeholder="e.g. Frontend Developer"
                    :rules="[requiredRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="work_outline" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model="form.joining_date"
                    outlined
                    type="date"
                    label="Joining Date"
                    :rules="[requiredRule]"
                    lazy-rules
                  >
                    <template #prepend>
                      <q-icon name="event" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-select
                    v-model="form.employment_type"
                    outlined
                    emit-value
                    map-options
                    :options="employmentTypeOptions"
                    label="Employment Type"
                  >
                    <template #prepend>
                      <q-icon name="badge" />
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-md-6">
                  <q-select
                    v-model="form.status"
                    outlined
                    emit-value
                    map-options
                    :options="statusOptions"
                    label="Employment Status"
                  >
                    <template #prepend>
                      <q-icon name="toggle_on" />
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="form.salary"
                    outlined
                    type="number"
                    min="0"
                    label="Salary"
                    placeholder="Enter salary"
                  >
                    <template #prepend>
                      <q-icon name="payments" />
                    </template>
                  </q-input>
                </div>

              </div>
            </q-card-section>
          </q-card>

          <!-- Emergency Contact -->
          <q-card class="som-card q-mb-lg">
            <q-card-section>
              <div class="section-title">
                <div class="section-icon emergency-icon">
                  <q-icon
                    name="contact_emergency"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Emergency Contact
                  </div>

                  <div class="text-caption text-grey-6">
                    Contact information for emergency situations
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="row q-col-gutter-md">

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.emergency_contact_name"
                    outlined
                    label="Contact Name"
                    placeholder="Enter emergency contact name"
                  >
                    <template #prepend>
                      <q-icon name="person" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.trim="form.emergency_contact_phone"
                    outlined
                    label="Contact Phone"
                    placeholder="Enter emergency contact phone"
                  >
                    <template #prepend>
                      <q-icon name="phone" />
                    </template>
                  </q-input>
                </div>

              </div>
            </q-card-section>
          </q-card>

          <!-- Actions -->
          <q-card class="som-card action-card">
            <q-card-section>
              <div class="row items-center justify-between q-col-gutter-md">

                <div class="col-12 col-sm">
                  <div class="row items-center no-wrap">
                    <q-avatar
                      size="42px"
                      color="blue-1"
                      text-color="primary"
                      class="q-mr-sm"
                    >
                      <q-icon
                        :name="isEditMode ? 'save' : 'person_add'"
                        size="21px"
                      />
                    </q-avatar>

                    <div>
                      <div class="text-subtitle1 text-weight-bold text-grey-8">
                        {{
                          isEditMode
                            ? 'Save employee changes'
                            : 'Create employee profile'
                        }}
                      </div>

                      <div class="text-caption text-grey-6">
                        {{
                          isEditMode
                            ? 'Review the updated information before saving.'
                            : 'Review all required information before creating the employee.'
                        }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-12 col-sm-auto">
                  <div class="row q-gutter-sm">

                    <q-btn
                      outline
                      color="grey-7"
                      label="Cancel"
                      no-caps
                      :disable="saving"
                      @click="goBack"
                    />

                    <q-btn
                      unelevated
                      color="primary"
                      :label="isEditMode ? 'Update Employee' : 'Create Employee'"
                      :icon="isEditMode ? 'save' : 'person_add'"
                      no-caps
                      :loading="saving"
                      type="submit"
                    />

                  </div>
                </div>

              </div>
            </q-card-section>
          </q-card>

        </div>
      </div>
    </q-form>
  </div>
</template>

<script>
import axios from 'axios'
import EmployeeApi from './employeeClass'
import DepartmentApi from '../department/api'

const API_BASE_URL = 'http://127.0.0.1:8000/api'
const BACKEND_BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'AddEmployee',

  data () {
    return {
      saving: false,
      departmentsLoading: false,

      capturedImage: null,
      selectedImageFile: null,

      showPassword: false,
      showConfirmPassword: false,

      form: {
        employee_id: '',
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        department: null,
        job_title: '',
        phone: '',
        address: '',
        date_of_birth: '',
        joining_date: '',
        employment_type: 'FULL_TIME',
        status: 'ACTIVE',
        salary: null,
        emergency_contact_name: '',
        emergency_contact_phone: '',
        password: '',
        password_confirm: ''
      },

      departments: [],

      employmentTypeOptions: [
        {
          label: 'Full Time',
          value: 'FULL_TIME'
        },
        {
          label: 'Part Time',
          value: 'PART_TIME'
        },
        {
          label: 'Contract',
          value: 'CONTRACT'
        },
        {
          label: 'Intern',
          value: 'INTERN'
        }
      ],

      statusOptions: [
        {
          label: 'Active',
          value: 'ACTIVE'
        },
        {
          label: 'Inactive',
          value: 'INACTIVE'
        },
        {
          label: 'On Leave',
          value: 'ON_LEAVE'
        }
      ]
    }
  },

  computed: {
    isEditMode () {
      return !!this.$route.query.id
    },

    employeeId () {
      return this.$route.query.id || null
    },

    departmentOptions () {
      return this.departments
    },

    initials () {
      const first = this.form.first_name?.charAt(0) || ''
      const last = this.form.last_name?.charAt(0) || ''

      const result = `${first}${last}`.toUpperCase()

      return result || 'EM'
    },

    canManage () {
      return (
        this.$store.getters.isAdmin ||
        this.$store.getters.isManager
      )
    }
  },

  async mounted () {
    if (!this.canManage) {
      this.$q.notify({
        type: 'negative',
        message: 'You do not have permission to manage employees.'
      })

      this.goBack()
      return
    }

    await this.loadDepartments()

    if (this.isEditMode) {
      await this.loadEmployee()
    }
  },

  methods: {
    requiredRule (value) {
      return !!value || 'This field is required'
    },

    requiredSelectRule (value) {
      return (
        (
          value !== null &&
          value !== undefined &&
          value !== ''
        ) ||
        'Please select an option'
      )
    },

    emailRule (value) {
      if (!value) {
        return 'This field is required'
      }

      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

      return (
        pattern.test(value) ||
        'Please enter a valid email address'
      )
    },

    passwordRule (value) {
      if (!value) {
        return 'Password is required'
      }

      if (value.length < 8) {
        return 'Password must be at least 8 characters'
      }

      return true
    },

    confirmPasswordRule (value) {
      if (!value) {
        return 'Please confirm the password'
      }

      if (value !== this.form.password) {
        return 'Passwords do not match'
      }

      return true
    },

    async loadDepartments () {
      this.departmentsLoading = true

      try {
        const response = await DepartmentApi.getDepartment()

        const data = response.data

        this.departments = Array.isArray(data)
          ? data
          : Array.isArray(data?.results)
            ? data.results
            : []
      } catch (error) {
        console.error('Failed to load departments:', error)

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Failed to load departments.'
          )
        })
      } finally {
        this.departmentsLoading = false
      }
    },

    normalizeImageUrl (value) {
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

      if (value.startsWith('/')) {
        return `${BACKEND_BASE_URL}${value}`
      }

      return `${BACKEND_BASE_URL}/${value}`
    },

    async loadEmployee () {
      if (!this.employeeId) {
        return
      }

      this.saving = true

      try {
        const response = await EmployeeApi.getEmployee(
          this.employeeId
        )

        const employee = response.data

        this.form.employee_id =
          employee.employee_id || ''

        this.form.username =
          employee.username ||
          employee.user?.username ||
          ''

        this.form.email =
          employee.email ||
          employee.user?.email ||
          ''

        this.form.job_title =
          employee.job_title || ''

        this.form.phone =
          employee.phone ||
          employee.user?.phone ||
          ''

        this.form.address =
          employee.address || ''

        this.form.date_of_birth =
          employee.date_of_birth || ''

        this.form.joining_date =
          employee.joining_date || ''

        this.form.employment_type =
          employee.employment_type ||
          'FULL_TIME'

        this.form.status =
          employee.status ||
          'ACTIVE'

        this.form.salary =
          employee.salary ?? null

        this.form.emergency_contact_name =
          employee.emergency_contact_name || ''

        this.form.emergency_contact_phone =
          employee.emergency_contact_phone || ''

        this.form.department =
          typeof employee.department === 'object'
            ? employee.department?.id || null
            : employee.department || null

        const userFirstName =
          employee.user?.first_name || ''

        const userLastName =
          employee.user?.last_name || ''

        const directFirstName =
          employee.first_name || ''

        const directLastName =
          employee.last_name || ''

        this.form.first_name =
          userFirstName || directFirstName

        this.form.last_name =
          userLastName || directLastName

        if (
          !this.form.first_name &&
          !this.form.last_name
        ) {
          const fullName =
            employee.full_name || ''

          const nameParts = fullName
            .trim()
            .split(/\s+/)
            .filter(Boolean)

          this.form.first_name =
            nameParts.shift() || ''

          this.form.last_name =
            nameParts.join(' ') || ''
        }

        if (employee.profile_picture) {
          this.capturedImage =
            this.normalizeImageUrl(
              employee.profile_picture
            )
        } else if (employee.user?.profile_picture) {
          this.capturedImage =
            this.normalizeImageUrl(
              employee.user.profile_picture
            )
        }
      } catch (error) {
        console.error(
          'Failed to load employee:',
          error
        )

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Failed to load employee.'
          )
        })

        this.goBack()
      } finally {
        this.saving = false
      }
    },

    openFileInput () {
      this.$refs.fileInput?.click()
    },

    captureImage (event) {
      const file = event.target.files?.[0]

      if (!file) {
        return
      }

      const allowedTypes = [
        'image/jpeg',
        'image/png',
        'image/webp'
      ]

      if (!allowedTypes.includes(file.type)) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please select a JPG, PNG or WEBP image.'
        })

        event.target.value = ''
        return
      }

      const maxSize = 5 * 1024 * 1024

      if (file.size > maxSize) {
        this.$q.notify({
          type: 'warning',
          message:
            'Image size must be less than 5 MB.'
        })

        event.target.value = ''
        return
      }

      this.selectedImageFile = file

      const reader = new FileReader()

      reader.onload = () => {
        this.capturedImage = reader.result
      }

      reader.readAsDataURL(file)
    },

    removeSelectedImage () {
      this.selectedImageFile = null

      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }

      if (this.isEditMode) {
        this.$q.notify({
          type: 'info',
          message:
            'The existing profile photo will remain unchanged unless a new photo is uploaded.'
        })

        return
      }

      this.capturedImage = null
    },

    appendFormDataValue (
      formData,
      key,
      value
    ) {
      if (
        value === undefined ||
        value === null ||
        value === ''
      ) {
        return
      }

      formData.append(
        key,
        value
      )
    },

    buildEmployeeFormData (userId = null) {
      const formData = new FormData()

      this.appendFormDataValue(
        formData,
        'employee_id',
        this.form.employee_id
      )

      if (userId) {
        formData.append(
          'user',
          userId
        )
      }

      this.appendFormDataValue(
        formData,
        'department',
        this.form.department
      )

      this.appendFormDataValue(
        formData,
        'job_title',
        this.form.job_title
      )

      this.appendFormDataValue(
        formData,
        'phone',
        this.form.phone
      )

      this.appendFormDataValue(
        formData,
        'address',
        this.form.address
      )

      this.appendFormDataValue(
        formData,
        'date_of_birth',
        this.form.date_of_birth
      )

      this.appendFormDataValue(
        formData,
        'joining_date',
        this.form.joining_date
      )

      this.appendFormDataValue(
        formData,
        'employment_type',
        this.form.employment_type
      )

      this.appendFormDataValue(
        formData,
        'status',
        this.form.status
      )

      if (
        this.form.salary !== null &&
        this.form.salary !== undefined &&
        this.form.salary !== ''
      ) {
        formData.append(
          'salary',
          this.form.salary
        )
      }

      this.appendFormDataValue(
        formData,
        'emergency_contact_name',
        this.form.emergency_contact_name
      )

      this.appendFormDataValue(
        formData,
        'emergency_contact_phone',
        this.form.emergency_contact_phone
      )

      if (this.selectedImageFile) {
        formData.append(
          'profile_picture',
          this.selectedImageFile
        )
      }

      return formData
    },

    async createUserAccount () {
      const payload = {
        username: this.form.username,
        email: this.form.email,
        password: this.form.password,
        password_confirm:
          this.form.password_confirm,
        first_name: this.form.first_name,
        last_name: this.form.last_name,
        phone: this.form.phone
      }

      const response = await axios.post(
        `${API_BASE_URL}/auth/register/`,
        payload
      )

      return response.data
    },

    async createEmployeeRecord (userId) {
      const formData =
        this.buildEmployeeFormData(userId)

      return EmployeeApi.createEmployee(
        formData
      )
    },

    async createEmployee () {
      const userResponse =
        await this.createUserAccount()

      const userId =
        userResponse?.id ||
        userResponse?.user?.id

      if (!userId) {
        throw new Error(
          'Employee account was created but the user ID was not returned by the server.'
        )
      }

      await this.createEmployeeRecord(
        userId
      )
    },

    async updateEmployee () {
      const formData =
        this.buildEmployeeFormData()

      return EmployeeApi.updateEmployee(
        this.employeeId,
        formData
      )
    },

    async saveEmployee () {
      if (this.saving) {
        return
      }

      if (!this.canManage) {
        this.$q.notify({
          type: 'negative',
          message:
            'You do not have permission to manage employees.'
        })

        return
      }

      const valid =
        await this.$refs.employeeForm.validate()

      if (!valid) {
        this.$q.notify({
          type: 'warning',
          message:
            'Please complete all required fields.'
        })

        return
      }

      this.saving = true

      try {
        if (this.isEditMode) {
          await this.updateEmployee()

          this.$q.notify({
            type: 'positive',
            message:
              'Employee updated successfully.'
          })
        } else {
          await this.createEmployee()

          this.$q.notify({
            type: 'positive',
            message:
              'Employee account and profile created successfully.'
          })
        }

        await this.$router.push(
          '/Empl-list'
        )
      } catch (error) {
        console.error(
          'Employee save failed:',
          error
        )

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            this.isEditMode
              ? 'Failed to update employee.'
              : 'Failed to create employee.'
          ),
          timeout: 7000
        })
      } finally {
        this.saving = false
      }
    },

    getErrorMessage (error, fallback) {
      if (
        error?.message &&
        !error?.response
      ) {
        return error.message
      }

      const data =
        error?.response?.data

      if (!data) {
        return fallback
      }

      if (typeof data === 'string') {
        return data
      }

      if (data.detail) {
        return data.detail
      }

      if (data.message) {
        return data.message
      }

      const messages = []

      Object.keys(data).forEach(
        (key) => {
          const value = data[key]

          if (Array.isArray(value)) {
            messages.push(
              `${key}: ${value.join(', ')}`
            )
          } else if (
            typeof value === 'object' &&
            value !== null
          ) {
            messages.push(
              `${key}: ${JSON.stringify(value)}`
            )
          } else if (
            typeof value === 'string'
          ) {
            messages.push(
              `${key}: ${value}`
            )
          }
        }
      )

      return messages.length
        ? messages.join(' | ')
        : fallback
    },

    goBack () {
      this.$router.push(
        '/Empl-list'
      )
    }
  }
}
</script>

<style scoped>
.employee-page {
  min-height: 100%;
  background: #f6f8fc;
}

.page-header {
  max-width: 1500px;
  margin-left: auto;
  margin-right: auto;
}

.mode-chip {
  font-weight: 600;
  padding: 7px 12px;
}

.som-card {
  border: 1px solid #e6eaf0;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 5px 24px rgba(25, 42, 70, 0.055);
  overflow: hidden;
}

.profile-card {
  position: sticky;
  top: 20px;
}

.profile-section {
  padding-top: 28px;
  padding-bottom: 26px;
}

.profile-label {
  font-size: 17px;
  font-weight: 700;
  color: #263238;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  border: 5px solid #eef4ff;
  box-shadow: 0 10px 30px rgba(25, 118, 210, 0.14);
  overflow: hidden;
}

.avatar-button {
  position: absolute;
  right: 1px;
  bottom: 5px;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.employee-id-box {
  padding: 14px;
  border-radius: 12px;
  background: #f7f9fc;
  border: 1px solid #edf0f5;
}

.side-info {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 4px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 13px;
}

.section-icon {
  width: 42px;
  height: 42px;
  min-width: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #1976d2;
  background: #edf4ff;
}

.security-icon {
  color: #546e7a;
  background: #eef2f4;
}

.emergency-icon {
  color: #c62828;
  background: #fff0f0;
}

.security-banner {
  background: #f2f7ff;
  border: 1px solid #dceaff;
  color: #455a64;
}

.photo-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #edf8f0;
  color: #2e7d32;
  font-size: 12px;
  font-weight: 600;
}

.action-card {
  margin-bottom: 30px;
}

.q-field--outlined .q-field__control {
  border-radius: 11px;
}

.q-field--outlined.q-field--focused .q-field__control {
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.08);
}

@media (max-width: 1023px) {
  .profile-card {
    position: static;
  }
}

@media (max-width: 599px) {
  .employee-page {
    padding: 12px !important;
  }

  .page-header .text-h4 {
    font-size: 24px;
  }

  .mode-chip {
    margin-top: 12px;
  }

  .section-title {
    align-items: flex-start;
  }

  .section-icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
  }

  .action-card .q-btn {
    flex: 1;
  }
}
</style>
