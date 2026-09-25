<template>
  <div class="account-page q-pa-md q-pa-lg-xl">

    <!-- Page Header -->
    <div class="page-header q-mb-lg">
      <div class="row items-center justify-between q-col-gutter-md">
        <div class="col">
          <div class="row items-center no-wrap">
            <q-avatar
              size="52px"
              color="blue-1"
              text-color="primary"
              class="q-mr-md"
            >
              <q-icon
                name="manage_accounts"
                size="28px"
              />
            </q-avatar>

            <div>
              <div class="text-h4 text-weight-bold text-grey-9">
                Account Settings
              </div>

              <div class="text-subtitle2 text-grey-6 q-mt-xs">
                Manage your profile information and account preferences
              </div>
            </div>
          </div>
        </div>

        <div class="col-auto">
          <q-chip
            color="green-1"
            text-color="green-9"
            icon="verified_user"
            class="account-chip"
          >
            {{ userRoleLabel }}
          </q-chip>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <q-card
      v-if="loading"
      class="som-card loading-card"
    >
      <q-card-section class="flex flex-center column q-pa-xl">
        <q-spinner
          color="primary"
          size="42px"
        />

        <div class="text-subtitle1 text-grey-7 q-mt-md">
          Loading account information...
        </div>
      </q-card-section>
    </q-card>

    <template v-else>

      <div class="row q-col-gutter-lg">

        <!-- Profile Sidebar -->
        <div class="col-12 col-md-4 col-lg-3">

          <q-card class="som-card profile-card">

            <q-card-section class="profile-section text-center">

              <div class="profile-label">
                My Profile
              </div>

              <div class="text-caption text-grey-6 q-mt-xs">
                Your SOMI account
              </div>

              <div class="avatar-wrapper q-mt-lg">

                <q-avatar
                  size="150px"
                  color="blue-1"
                  text-color="primary"
                  class="profile-avatar"
                >
                  <q-img
                    v-if="profileImage"
                    :src="profileImage"
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
                  :loading="uploadingPhoto"
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
                @change="onFileSelected"
              />

              <q-btn
                outline
                color="primary"
                icon="upload"
                label="Change Photo"
                no-caps
                class="q-mt-md full-width"
                :loading="uploadingPhoto"
                @click="openFileInput"
              />

              <div class="text-caption text-grey-5 q-mt-sm">
                JPG, PNG or WEBP · Maximum 5 MB
              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div class="profile-name">
                {{ displayName }}
              </div>

              <div class="profile-username">
                @{{ user.username || 'user' }}
              </div>

              <div class="profile-role q-mt-md">
                <q-icon
                  name="shield"
                  size="17px"
                />

                <span>
                  {{ userRoleLabel }}
                </span>
              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div class="side-detail">
                <q-icon
                  name="email"
                  color="grey-6"
                  size="19px"
                />

                <div>
                  <div class="text-caption text-grey-5">
                    Email
                  </div>

                  <div class="text-body2 text-grey-8 ellipsis">
                    {{ user.email || 'Not available' }}
                  </div>
                </div>
              </div>

              <div class="side-detail q-mt-md">
                <q-icon
                  name="phone"
                  color="grey-6"
                  size="19px"
                />

                <div>
                  <div class="text-caption text-grey-5">
                    Phone
                  </div>

                  <div class="text-body2 text-grey-8">
                    {{ user.phone || employee.phone || 'Not available' }}
                  </div>
                </div>
              </div>

            </q-card-section>

          </q-card>

        </div>

        <!-- Main Content -->
        <div class="col-12 col-md-8 col-lg-9">

          <!-- Account Information -->
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
                    Account Information
                  </div>

                  <div class="text-caption text-grey-6">
                    Information associated with your SOMI account
                  </div>
                </div>

              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div class="row q-col-gutter-md">

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="user.username"
                    outlined
                    label="Username"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="account_circle" />
                    </template>

                    <template #append>
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Username is managed by the account system.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="user.email"
                    outlined
                    type="email"
                    label="Email Address"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="email" />
                    </template>

                    <template #append>
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Email is managed by the account system.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="fullName"
                    outlined
                    label="Full Name"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="badge" />
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="user.phone || employee.phone"
                    outlined
                    label="Phone Number"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="phone" />
                    </template>

                    <template #append>
                      <q-icon
                        name="lock"
                        size="18px"
                        color="grey-5"
                      >
                        <q-tooltip>
                          Contact information is managed through the employee record.
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-input>

                </div>

              </div>

            </q-card-section>

          </q-card>

          <!-- Professional Information -->
          <q-card class="som-card q-mb-lg">

            <q-card-section>

              <div class="section-title">

                <div class="section-icon professional-icon">
                  <q-icon
                    name="business_center"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Professional Information
                  </div>

                  <div class="text-caption text-grey-6">
                    Your current role and employment information
                  </div>
                </div>

              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div
                v-if="employeeFound"
                class="row q-col-gutter-md"
              >

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="employee.job_title || 'Not assigned'"
                    outlined
                    label="Job Title"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="work_outline" />
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="departmentName"
                    outlined
                    label="Department"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="corporate_fare" />
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="formatDate(employee.joining_date)"
                    outlined
                    label="Joining Date"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="event" />
                    </template>
                  </q-input>

                </div>

                <div class="col-12 col-md-6">

                  <q-input
                    :model-value="employmentTypeLabel"
                    outlined
                    label="Employment Type"
                    readonly
                  >
                    <template #prepend>
                      <q-icon name="badge" />
                    </template>
                  </q-input>

                </div>

              </div>

              <q-banner
                v-else
                rounded
                class="info-banner"
              >
                <template #avatar>
                  <q-icon
                    name="info"
                    color="primary"
                  />
                </template>

                No employee profile is currently linked to this account.
              </q-banner>

            </q-card-section>

          </q-card>

          <!-- Account Status -->
          <q-card class="som-card q-mb-lg">

            <q-card-section>

              <div class="section-title">

                <div class="section-icon status-icon">
                  <q-icon
                    name="verified_user"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Account Status
                  </div>

                  <div class="text-caption text-grey-6">
                    Current status and access information
                  </div>
                </div>

              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div class="row q-col-gutter-md">

                <div class="col-12 col-sm-4">

                  <div class="status-box">

                    <q-icon
                      name="check_circle"
                      color="positive"
                      size="24px"
                    />

                    <div>
                      <div class="text-caption text-grey-5">
                        Account
                      </div>

                      <div class="text-subtitle2 text-weight-bold text-positive">
                        Active
                      </div>
                    </div>

                  </div>

                </div>

                <div class="col-12 col-sm-4">

                  <div class="status-box">

                    <q-icon
                      name="admin_panel_settings"
                      color="primary"
                      size="24px"
                    />

                    <div>
                      <div class="text-caption text-grey-5">
                        Access Role
                      </div>

                      <div class="text-subtitle2 text-weight-bold text-primary">
                        {{ userRoleLabel }}
                      </div>
                    </div>

                  </div>

                </div>

                <div class="col-12 col-sm-4">

                  <div class="status-box">

                    <q-icon
                      name="work_history"
                      color="deep-purple"
                      size="24px"
                    />

                    <div>
                      <div class="text-caption text-grey-5">
                        Employee Status
                      </div>

                      <div class="text-subtitle2 text-weight-bold text-deep-purple">
                        {{ employeeStatusLabel }}
                      </div>
                    </div>

                  </div>

                </div>

              </div>

            </q-card-section>

          </q-card>

          <!-- Security -->
          <q-card class="som-card q-mb-lg">

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
                    Security
                  </div>

                  <div class="text-caption text-grey-6">
                    Password and account security settings
                  </div>
                </div>

              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <q-banner
                rounded
                class="security-banner"
              >
                <template #avatar>
                  <q-icon
                    name="info"
                    color="primary"
                    size="24px"
                  />
                </template>

                <div class="text-weight-medium">
                  Password management is currently handled by the
                  SOMI authentication system.
                </div>

                <div class="text-caption q-mt-xs">
                  A dedicated change-password endpoint is not currently
                  available in the connected backend.
                </div>
              </q-banner>

            </q-card-section>

          </q-card>

          <!-- Account Meta -->
          <q-card class="som-card">

            <q-card-section>

              <div class="section-title">

                <div class="section-icon meta-icon">
                  <q-icon
                    name="info"
                    size="21px"
                  />
                </div>

                <div>
                  <div class="text-h6 text-weight-bold text-grey-9">
                    Account Details
                  </div>

                  <div class="text-caption text-grey-6">
                    System information
                  </div>
                </div>

              </div>

            </q-card-section>

            <q-separator />

            <q-card-section>

              <div class="row q-col-gutter-lg">

                <div class="col-12 col-sm-6">

                  <div class="meta-item">
                    <span>Account Created</span>
                    <strong>
                      {{ formatDateTime(user.created_at || user.date_joined) }}
                    </strong>
                  </div>

                </div>

                <div class="col-12 col-sm-6">

                  <div class="meta-item">
                    <span>Username</span>
                    <strong>
                      {{ user.username || 'Not available' }}
                    </strong>
                  </div>

                </div>

              </div>

            </q-card-section>

          </q-card>

        </div>

      </div>

    </template>

  </div>
</template>

<script>
import EmployeeApi from './employee/employeeClass'

const BACKEND_BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'AccountSettings',

  data () {
    return {
      loading: true,
      uploadingPhoto: false,

      user: {},
      employee: {},
      employeeFound: false
    }
  },

  computed: {
    displayName () {
      const name = `${this.user.first_name || ''} ${this.user.last_name || ''}`.trim()

      return name || this.user.username || 'SOMI User'
    },

    fullName () {
      return this.displayName
    },

    initials () {
      const first = this.user.first_name?.charAt(0) || ''
      const last = this.user.last_name?.charAt(0) || ''

      const result = `${first}${last}`.toUpperCase()

      return result || this.user.username?.charAt(0)?.toUpperCase() || 'U'
    },

    userRoleLabel () {
      const role = String(this.user.role || 'EMPLOYEE').toUpperCase()

      return role.charAt(0) + role.slice(1).toLowerCase()
    },

    profileImage () {
      const image =
        this.user.profile_picture ||
        this.employee.profile_picture ||
        ''

      return this.normalizeImageUrl(image)
    },

    departmentName () {
      return (
        this.employee.department_name ||
        this.employee.department?.name ||
        'Not assigned'
      )
    },

    employmentTypeLabel () {
      const value = this.employee.employment_type

      const labels = {
        FULL_TIME: 'Full Time',
        PART_TIME: 'Part Time',
        CONTRACT: 'Contract',
        INTERN: 'Intern'
      }

      return labels[value] || value || 'Not assigned'
    },

    employeeStatusLabel () {
      const value = this.employee.status

      const labels = {
        ACTIVE: 'Active',
        INACTIVE: 'Inactive',
        ON_LEAVE: 'On Leave'
      }

      return labels[value] || value || 'Not available'
    }
  },

  async mounted () {
    await this.loadAccount()
  },

  methods: {
    async loadAccount () {
      this.loading = true

      try {
        const currentUser = this.$store.getters.currentUser

        if (currentUser) {
          this.user = { ...currentUser }
        } else {
          await this.$store.dispatch('fetchCurrentUser')

          this.user = {
            ...(this.$store.getters.currentUser || {})
          }
        }

        await this.loadEmployeeProfile()
      } catch (error) {
        console.error(
          'Failed to load account:',
          error
        )

        this.$q.notify({
          type: 'negative',
          message: 'Failed to load account information.'
        })
      } finally {
        this.loading = false
      }
    },

    async loadEmployeeProfile () {
      try {
        const response =
          await EmployeeApi.getEmployees()

        const data = response.data

        const employees = Array.isArray(data)
          ? data
          : Array.isArray(data?.results)
            ? data.results
            : []

        const currentUserId = this.user.id

        const employee = employees.find((item) => {
          const employeeUserId =
            typeof item.user === 'object'
              ? item.user?.id
              : item.user

          return (
            String(employeeUserId) ===
            String(currentUserId)
          )
        })

        if (employee) {
          this.employee = employee
          this.employeeFound = true
        }
      } catch (error) {
        console.error(
          'Failed to load employee profile:',
          error
        )
      }
    },

    openFileInput () {
      this.$refs.fileInput?.click()
    },

    async onFileSelected (event) {
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
          message: 'Please select a JPG, PNG or WEBP image.'
        })

        event.target.value = ''
        return
      }

      const maxSize = 5 * 1024 * 1024

      if (file.size > maxSize) {
        this.$q.notify({
          type: 'warning',
          message: 'Image size must be less than 5 MB.'
        })

        event.target.value = ''
        return
      }

      if (!this.employeeFound || !this.employee.id) {
        this.$q.notify({
          type: 'warning',
          message: 'No employee profile is linked to this account.'
        })

        event.target.value = ''
        return
      }

      const formData = new FormData()

      formData.append(
        'profile_picture',
        file
      )

      this.uploadingPhoto = true

      try {
        const response =
          await EmployeeApi.updateEmployee(
            this.employee.id,
            formData
          )

        this.employee = response.data

        this.$q.notify({
          type: 'positive',
          message: 'Profile photo updated successfully.'
        })
      } catch (error) {
        console.error(
          'Profile photo update failed:',
          error
        )

        this.$q.notify({
          type: 'negative',
          message: this.getErrorMessage(
            error,
            'Failed to update profile photo.'
          )
        })
      } finally {
        this.uploadingPhoto = false

        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = ''
        }
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

    formatDate (value) {
      if (!value) {
        return 'Not available'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleDateString(
        'en-US',
        {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        }
      )
    },

    formatDateTime (value) {
      if (!value) {
        return 'Not available'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleDateString(
        'en-US',
        {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        }
      )
    },

    getErrorMessage (error, fallback) {
      const data = error?.response?.data

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

      Object.keys(data).forEach((key) => {
        const value = data[key]

        if (Array.isArray(value)) {
          messages.push(
            `${key}: ${value.join(', ')}`
          )
        } else if (
          typeof value === 'string'
        ) {
          messages.push(
            `${key}: ${value}`
          )
        }
      })

      return messages.length
        ? messages.join(' | ')
        : fallback
    }
  }
}
</script>

<style scoped>
.account-page {
  min-height: 100%;
  background: #f6f8fc;
}

.page-header {
  max-width: 1500px;
  margin-left: auto;
  margin-right: auto;
}

.account-chip {
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

.profile-name {
  font-size: 19px;
  font-weight: 700;
  color: #263238;
  text-align: center;
}

.profile-username {
  text-align: center;
  color: #78909c;
  font-size: 13px;
  margin-top: 3px;
}

.profile-role {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  color: #1976d2;
  font-size: 13px;
  font-weight: 600;
}

.side-detail {
  display: flex;
  align-items: flex-start;
  gap: 11px;
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

.professional-icon {
  color: #1565c0;
  background: #eaf3ff;
}

.security-icon {
  color: #546e7a;
  background: #eef2f4;
}

.status-icon {
  color: #2e7d32;
  background: #edf8f0;
}

.meta-icon {
  color: #6a1b9a;
  background: #f6edfa;
}

.status-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid #edf0f5;
  border-radius: 13px;
  background: #f9fafc;
  height: 100%;
}

.info-banner {
  background: #f2f7ff;
  border: 1px solid #dceaff;
  color: #455a64;
}

.security-banner {
  background: #f2f7ff;
  border: 1px solid #dceaff;
  color: #455a64;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 14px 16px;
  border-radius: 12px;
  background: #f8f9fb;
  border: 1px solid #edf0f4;
}

.meta-item span {
  color: #90a4ae;
  font-size: 12px;
}

.meta-item strong {
  color: #37474f;
  font-size: 14px;
}

.loading-card {
  min-height: 280px;
}

@media (max-width: 1023px) {
  .profile-card {
    position: static;
  }
}

@media (max-width: 599px) {
  .account-page {
    padding: 12px !important;
  }

  .page-header .text-h4 {
    font-size: 24px;
  }

  .account-chip {
    margin-top: 10px;
  }

  .section-title {
    align-items: flex-start;
  }

  .section-icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
  }

  .status-box {
    min-height: 72px;
  }
}
</style>
