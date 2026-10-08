<template>
  <q-layout view="hHh Lpr lFf" class="somi-layout">

    <!-- ==================== HEADER ==================== -->
    <q-header class="somi-header">
      <q-toolbar class="somi-toolbar">

        <q-btn
          flat
          round
          dense
          icon="menu"
          class="header-action"
          aria-label="Toggle navigation"
          @click="toggleLeftDrawer"
        >
          <q-tooltip>
            Toggle navigation
          </q-tooltip>
        </q-btn>

        <!-- Desktop title -->
        <div class="desktop-header-title">
          <div class="header-title-main">
            Smart Office Management
          </div>

          <div class="header-title-caption">
            Intelligence & Workforce Platform
          </div>
        </div>

        <!-- Mobile brand -->
        <div class="mobile-brand">
          <div class="brand-mark brand-mark--small">
            <q-icon
              name="hub"
              size="20px"
            />
          </div>

          <div class="mobile-brand-text">
            <div class="mobile-brand-name">
              SOMI
            </div>

            <div class="mobile-brand-caption">
              Smart Office
            </div>
          </div>
        </div>

        <q-space />

        <!-- Notifications -->
         <NotificationBell v-if="isAuthenticated" />

        <!-- Current user -->
        <div
          v-if="isAuthenticated"
          class="header-user"
        >
          <q-avatar
            size="36px"
            class="header-user-avatar"
          >
            <img
              v-if="profilePicture"
              :src="profilePicture"
              alt="Profile"
            >

            <span v-else>
              {{ initials }}
            </span>
          </q-avatar>

          <div class="header-user-info">
            <div class="header-user-name">
              {{ shortName }}
            </div>

            <div class="header-user-role">
              {{ formattedRole }}
            </div>
          </div>
        </div>

        <!-- Dark mode -->
        <q-btn
          flat
          round
          dense
          class="header-action"
          :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'"
          aria-label="Toggle dark mode"
          @click="toggleDarkmode"
        >
          <q-tooltip>
            {{ $q.dark.isActive ? 'Light mode' : 'Dark mode' }}
          </q-tooltip>
        </q-btn>

        <!-- Logout -->
        <q-btn
          v-if="isAuthenticated"
          flat
          round
          dense
          icon="logout"
          class="header-action header-logout"
          aria-label="Sign out"
          @click="Logout"
        >
          <q-tooltip>
            Sign out
          </q-tooltip>
        </q-btn>

      </q-toolbar>
    </q-header>

    <!-- ==================== SIDEBAR ==================== -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="270"
      bordered
      class="somi-drawer"
    >
      <div class="drawer-container">

        <!-- Brand -->
        <div class="drawer-brand">

          <div class="brand-mark">
            <q-icon
              name="hub"
              size="25px"
            />
          </div>

          <div class="brand-content">
            <div class="brand-name">
              SOMI
            </div>

            <div class="brand-subtitle">
              Smart Office Management & Intelligence
            </div>
          </div>

        </div>

        <!-- Profile -->
        <div class="drawer-profile">

          <q-avatar
            size="48px"
            class="profile-avatar"
          >
            <img
              v-if="profilePicture"
              :src="profilePicture"
              alt="Profile"
            >

            <span v-else>
              {{ initials }}
            </span>
          </q-avatar>

          <div class="profile-info">

            <div class="profile-name">
              {{ shortName }}
            </div>

            <div class="profile-email">
              {{ email || 'SOMI User' }}
            </div>

            <q-badge class="profile-role">
              {{ formattedRole }}
            </q-badge>

          </div>

        </div>

        <!-- Navigation -->
        <div class="navigation-wrapper">

          <!-- Workspace -->
          <div class="navigation-label">
            WORKSPACE
          </div>

          <q-list class="navigation-list">

            <!-- Dashboard -->
            <q-item
              clickable
              v-ripple
              to="/emp-dashboard"
              exact
              class="navigation-item"
              active-class="navigation-item--active"
            >
              <q-item-section avatar>
                <q-icon name="space_dashboard" />
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  Dashboard
                </q-item-label>

                <q-item-label caption>
                  Overview & insights
                </q-item-label>
              </q-item-section>
            </q-item>

            <!-- Employees -->
            <q-item
              clickable
              v-ripple
              to="/Empl-list"
              class="navigation-item"
              active-class="navigation-item--active"
            >
              <q-item-section avatar>
                <q-icon name="groups" />
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  Employees
                </q-item-label>

                <q-item-label caption>
                  Workforce directory
                </q-item-label>
              </q-item-section>
            </q-item>

            <!-- Departments -->
            <q-item
              clickable
              v-ripple
              to="/list_dep"
              class="navigation-item"
              active-class="navigation-item--active"
            >
              <q-item-section avatar>
                <q-icon name="account_tree" />
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  Departments
                </q-item-label>

                <q-item-label caption>
                  Teams & structure
                </q-item-label>
              </q-item-section>
            </q-item>


            <!-- Tasks -->
<q-item
  clickable
  v-ripple
  to="/tasks"
  class="navigation-item"
  active-class="navigation-item--active"
>
  <q-item-section avatar>
    <q-icon name="task_alt" />
  </q-item-section>

  <q-item-section>
    <q-item-label>
      Tasks
    </q-item-label>

    <q-item-label caption>
      Work & productivity
    </q-item-label>
  </q-item-section>
</q-item>


<!-- Performance -->
<q-item
  clickable
  v-ripple
  to="/performance"
  class="navigation-item"
  active-class="navigation-item--active"
>
  <q-item-section avatar>
    <q-icon name="trending_up" />
  </q-item-section>

  <q-item-section>
    <q-item-label>
      Performance
    </q-item-label>

    <q-item-label caption>
      Reviews & growth
    </q-item-label>
  </q-item-section>
</q-item>

<!-- Office Intelligence -->
<q-item
  clickable
  v-ripple
  to="/intelligence"
  class="navigation-item intelligence-navigation-item"
  active-class="navigation-item--active"
>
  <q-item-section avatar>
    <q-icon name="auto_awesome" />
  </q-item-section>

  <q-item-section>
    <q-item-label>
      Office Intelligence
    </q-item-label>

    <q-item-label caption>
      Smart office insights
    </q-item-label>
  </q-item-section>
</q-item>


<!-- AI Assistant -->
<q-item
  clickable
  v-ripple
  to="/ai-assistant"
  active-class="nav-item-active"
>
  <q-item-section avatar>
    <q-icon name="smart_toy" />
  </q-item-section>

  <q-item-section>
    <q-item-label>AI Assistant</q-item-label>
    <q-item-label caption>Ask SOMI AI</q-item-label>
  </q-item-section>
</q-item>

            <!-- Management section -->
            <template v-if="canManage">

              <div class="navigation-sub-label">
                MANAGEMENT
              </div>

              <!-- Add Employee -->
              <q-item
                clickable
                v-ripple
                to="/add_employee"
                class="navigation-item"
                active-class="navigation-item--active"
              >
                <q-item-section avatar>
                  <q-icon name="person_add" />
                </q-item-section>

                <q-item-section>
                  <q-item-label>
                    Add Employee
                  </q-item-label>

                  <q-item-label caption>
                    Create employee record
                  </q-item-label>
                </q-item-section>
              </q-item>

              <!-- Add Department -->
              <q-item
                clickable
                v-ripple
                to="/addDep"
                class="navigation-item"
                active-class="navigation-item--active"
              >
                <q-item-section avatar>
                  <q-icon name="add_business" />
                </q-item-section>

                <q-item-section>
                  <q-item-label>
                    Add Department
                  </q-item-label>

                  <q-item-label caption>
                    Create department
                  </q-item-label>
                </q-item-section>
              </q-item>

            </template>

           <!-- Attendance -->
<q-expansion-item
  icon="event_available"
  label="Attendance"
  caption="Work attendance"
  class="navigation-expansion"
  header-class="navigation-expansion-header"
>
  <q-item
    clickable
    v-ripple
    to="/attan_report"
    class="navigation-subitem"
    active-class="navigation-subitem--active"
  >
    <q-item-section avatar>
      <q-icon name="event_available" />
    </q-item-section>

    <q-item-section>
      Attendance
    </q-item-section>
  </q-item>
</q-expansion-item>

            <!-- Leave -->
           <!-- Leave -->
<q-expansion-item
  icon="event_busy"
  label="Leave"
  caption="Leave management"
  class="navigation-expansion"
  header-class="navigation-expansion-header"
>
  <!-- Request Leave -->
  <q-item
    clickable
    v-ripple
    to="/leavePage"
    class="navigation-subitem"
    active-class="navigation-subitem--active"
  >
    <q-item-section avatar>
      <q-icon name="add_circle_outline" />
    </q-item-section>

    <q-item-section>
      Request Leave
    </q-item-section>
  </q-item>

  <!-- Approve Leaves -->
  <q-item
    v-if="canManage"
    clickable
    v-ripple
    to="/Approver_leaves"
    class="navigation-subitem"
    active-class="navigation-subitem--active"
  >
    <q-item-section avatar>
      <q-icon name="task_alt" />
    </q-item-section>

    <q-item-section>
      Approve Leaves
    </q-item-section>
  </q-item>

  <!-- Leave Reports -->
 <q-item
  clickable
  v-ripple
  to="/LeaveReport"
  class="navigation-subitem"
  active-class="navigation-subitem--active"
>
  <q-item-section avatar>
    <q-icon name="assessment" />
  </q-item-section>

  <q-item-section>
    Leave Reports
  </q-item-section>
</q-item>
</q-expansion-item>

            <!-- Payroll -->
            <q-expansion-item
              icon="payments"
              label="Payroll"
              caption="Salary & payroll"
              class="navigation-expansion"
              header-class="navigation-expansion-header"
            >
              <q-item
                clickable
                v-ripple
                to="/payroll_report"
                class="navigation-subitem"
                active-class="navigation-subitem--active"
              >
                <q-item-section avatar>
                  <q-icon name="description" />
                </q-item-section>

                <q-item-section>
                  Payroll Reports
                </q-item-section>
              </q-item>

              <q-item
                v-if="canManage"
                clickable
                v-ripple
                to="/new_payroll"
                class="navigation-subitem"
                active-class="navigation-subitem--active"
              >
                <q-item-section avatar>
                  <q-icon name="post_add" />
                </q-item-section>

                <q-item-section>
                  Create Payroll
                </q-item-section>
              </q-item>
            </q-expansion-item>

          </q-list>

          <!-- Account -->
          <div class="navigation-label navigation-label--secondary">
            ACCOUNT
          </div>

          <q-list class="navigation-list">

            <!-- User management -->
            <q-item
              v-if="canManage"
              clickable
              v-ripple
              to="/users"
              class="navigation-item"
              active-class="navigation-item--active"
            >
              <q-item-section avatar>
                <q-icon name="manage_accounts" />
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  User Management
                </q-item-label>

                <q-item-label caption>
                  Access & user records
                </q-item-label>
              </q-item-section>
            </q-item>

            <!-- Settings -->
            <q-item
              clickable
              v-ripple
              to="/AccountSettings"
              class="navigation-item"
              active-class="navigation-item--active"
            >
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  Settings
                </q-item-label>

                <q-item-label caption>
                  Account preferences
                </q-item-label>
              </q-item-section>
            </q-item>

          </q-list>

        </div>

        <!-- Footer -->
        <div class="drawer-footer">

          <div class="footer-status">
            <span class="status-dot"></span>

            <span>
              SOMI Workspace
            </span>
          </div>

          <div class="footer-version">
            Smart Office Management & Intelligence
          </div>

        </div>

      </div>
    </q-drawer>

    <!-- ==================== PAGE CONTENT ==================== -->
    <q-page-container class="somi-page-container">
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue'
import AuthenticationService from '../pages/authentication/AuthenticationService'
import NotificationBell from '../components/notifications/NotificationBell'

export default {
  name: 'EMSLayout',

  components: {
  NotificationBell
},

  setup () {
    const leftDrawerOpen = ref(true)

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    return {
      leftDrawerOpen,
      toggleLeftDrawer
    }
  },

  computed: {
    currentUser () {
      return this.$store.getters.currentUser
    },

    fullName () {
      return this.$store.getters.fullName || 'User'
    },

    shortName () {
      const name = this.fullName || 'User'
      const parts = name.trim().split(/\s+/)

      if (parts.length <= 2) {
        return name
      }

      return `${parts[0]} ${parts[parts.length - 1]}`
    },

    initials () {
      const name = this.fullName || 'User'

      const parts = name
        .trim()
        .split(/\s+/)
        .filter(Boolean)

      if (!parts.length) {
        return 'U'
      }

      if (parts.length === 1) {
        return parts[0].charAt(0).toUpperCase()
      }

      return (
        parts[0].charAt(0) +
        parts[parts.length - 1].charAt(0)
      ).toUpperCase()
    },

    email () {
      return this.$store.getters.email || ''
    },

    role () {
      return String(
        this.$store.getters.userRole || ''
      ).toUpperCase()
    },

    formattedRole () {
      const role = this.role || 'USER'

      return role
        .toLowerCase()
        .replace(/\b\w/g, letter => letter.toUpperCase())
    },

    profilePicture () {
      const picture = this.currentUser?.profile_picture

      if (!picture) {
        return null
      }

      if (
        picture.startsWith('http://') ||
        picture.startsWith('https://')
      ) {
        return picture
      }

      return `http://127.0.0.1:8000${picture}`
    },

    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },

    isAdmin () {
      return this.role === 'ADMIN'
    },

    isManager () {
      return this.role === 'MANAGER'
    },

    isEmployee () {
      return this.role === 'EMPLOYEE'
    },

    canManage () {
      return (
        this.role === 'ADMIN' ||
        this.role === 'MANAGER'
      )
    }
  },

  mounted () {
    this.loadCurrentUser()
  },

  methods: {
    toggleDarkmode () {
      this.$q.dark.toggle()
    },

    async loadCurrentUser () {
      if (!AuthenticationService.isAuthenticated()) {
        return
      }

      try {
        await this.$store.dispatch(
          'fetchCurrentUser'
        )
      } catch (error) {
        console.error(
          'Failed to fetch current user:',
          error
        )

        if (error.response?.status === 401) {
          AuthenticationService.clearTokens()
          this.$store.commit('CLEAR_USER')
          this.$router.push('/LoginPage')
        }
      }
    },

    Logout () {
      this.$q
        .dialog({
          title: 'Sign out of SOMI?',
          message:
            'Your current session will be securely closed.',

          cancel: {
            label: 'Cancel',
            flat: true
          },

          ok: {
            label: 'Sign out',
            unelevated: true
          },

          persistent: true
        })
        .onOk(async () => {
          try {
            await this.$store.dispatch('logout')
          } finally {
            this.$router.push('/LoginPage')
          }
        })
    }
  }
}
</script>

<style scoped>
.somi-layout {
  min-height: 100vh;
  background: #f5f7fb;
}

.somi-page-container {
  min-height: 100vh;
  background: #f5f7fb;
}

.somi-header {
  background: rgba(255, 255, 255, 0.98);
  color: #172033;
  border-bottom: 1px solid #e8edf4;
  box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
  backdrop-filter: blur(14px);
}

.somi-toolbar {
  min-height: 66px;
  padding: 0 18px;
}

.header-action {
  color: #526071;
  margin-left: 3px;
  transition:
    background 0.18s ease,
    color 0.18s ease,
    transform 0.18s ease;
}

.header-action:hover {
  background: #f1f5f9;
  color: #2563eb;
}

.header-action:active {
  transform: scale(0.94);
}

.header-logout:hover {
  background: #fff1f2;
  color: #dc2626;
}

.desktop-header-title {
  padding-left: 14px;
}

.header-title-main {
  color: #172033;
  font-size: 16px;
  font-weight: 750;
  line-height: 1.2;
}

.header-title-caption {
  margin-top: 3px;
  color: #8a94a6;
  font-size: 10.5px;
  font-weight: 500;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-right: 6px;
}

.header-user-avatar {
  background: #eef2ff;
  color: #4f46e5;
  border: 1px solid #dfe5f2;
  font-size: 13px;
  font-weight: 800;
}

.header-user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-user-info {
  min-width: 85px;
}

.header-user-name {
  max-width: 125px;
  overflow: hidden;
  color: #1e293b;
  font-size: 12px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-user-role {
  margin-top: 2px;
  color: #8b97a8;
  font-size: 10px;
  font-weight: 600;
}

.mobile-brand {
  display: none;
  align-items: center;
  gap: 8px;
  margin-left: 10px;
}

.mobile-brand-text {
  line-height: 1;
}

.mobile-brand-name {
  color: #172033;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.mobile-brand-caption {
  margin-top: 3px;
  color: #94a3b8;
  font-size: 9px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 12px;
  background: linear-gradient(
    135deg,
    #2563eb,
    #4f46e5
  );
  color: #ffffff;
  box-shadow:
    0 7px 18px rgba(37, 99, 235, 0.22);
}

.brand-mark--small {
  width: 34px;
  height: 34px;
  border-radius: 10px;
}

.somi-drawer {
  background: #ffffff;
  color: #1e293b;
  border-right: 1px solid #e5e9f0;
}

.drawer-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.drawer-brand {
  min-height: 82px;
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 17px 18px;
  border-bottom: 1px solid #edf0f5;
}

.brand-content {
  min-width: 0;
}

.brand-name {
  color: #172033;
  font-size: 21px;
  font-weight: 800;
  letter-spacing: 0.8px;
  line-height: 1;
}

.brand-subtitle {
  max-width: 180px;
  margin-top: 5px;
  color: #8995a7;
  font-size: 9px;
  font-weight: 600;
  line-height: 1.35;
}

.drawer-profile {
  display: flex;
  align-items: center;
  gap: 11px;
  margin: 12px 12px 7px;
  padding: 10px 11px;
  min-height: 76px;
  border: 1px solid #e8edf4;
  border-radius: 13px;
  background: #f8fafc;
  transition:
    border-color 0.18s ease,
    background 0.18s ease;
}

.drawer-profile:hover {
  border-color: #dce5f4;
  background: #f6f9fd;
}

.profile-avatar {
  flex-shrink: 0;
  background: #eef2ff;
  color: #4f46e5;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 7px rgba(15, 23, 42, 0.08);
  font-size: 14px;
  font-weight: 800;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  min-width: 0;
  flex: 1;
}

.profile-name {
  overflow: hidden;
  color: #1e293b;
  font-size: 13px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-email {
  max-width: 160px;
  margin-top: 3px;
  overflow: hidden;
  color: #7d899b;
  font-size: 10px;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-role {
  margin-top: 5px;
  padding: 2px 7px;
  border-radius: 5px;
  background: #e8efff;
  color: #3158bd;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.navigation-wrapper {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 7px 9px 10px;
  scrollbar-width: thin;
  scrollbar-color: #d2d8e2 transparent;
}

.navigation-wrapper::-webkit-scrollbar {
  width: 4px;
}

.navigation-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.navigation-wrapper::-webkit-scrollbar-thumb {
  background: #d2d8e2;
  border-radius: 10px;
}

.navigation-label {
  padding: 11px 11px 6px;
  color: #8c98a9;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 1px;
}

.navigation-label--secondary {
  margin-top: 7px;
}

.navigation-sub-label {
  padding: 13px 11px 5px;
  color: #a0aaba;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.9px;
}

.navigation-list {
  padding: 0;
}

.navigation-item {
  min-height: 49px;
  margin: 3px 0;
  border-radius: 10px;
  color: #526276;
  transition:
    background 0.18s ease,
    color 0.18s ease,
    transform 0.18s ease;
}

.navigation-item:hover {
  background: #f4f7fb;
  color: #334155;
}

.navigation-item--active {
  background: #edf3ff !important;
  color: #225dcc !important;
  font-weight: 700;
  box-shadow:
    inset 3px 0 0 #2563eb;
}

.navigation-item--active .q-icon {
  color: #2563eb;
}

.navigation-item .q-item__section--avatar {
  min-width: 42px;
  color: #718096;
}

.navigation-item .q-icon {
  font-size: 20px;
  transition: color 0.18s ease;
}

.navigation-item .q-item__label {
  font-size: 12.5px;
  font-weight: 650;
}

.navigation-item .q-item__label--caption {
  margin-top: 2px;
  color: #8a96a7;
  font-size: 9.5px;
  font-weight: 500;
}

.navigation-item--active .q-item__label--caption {
  color: #6684d4;
}

.navigation-expansion {
  margin: 3px 0;
  border-radius: 10px;
  color: #526276;
  overflow: hidden;
}

.navigation-expansion-header {
  min-height: 49px;
  padding: 0 11px;
  border-radius: 10px;
  transition:
    background 0.18s ease,
    color 0.18s ease;
}

.navigation-expansion-header:hover {
  background: #f4f7fb;
}

.navigation-expansion :deep(.q-item__section--avatar) {
  min-width: 42px;
  color: #718096;
}

.navigation-expansion :deep(.q-icon) {
  font-size: 20px;
}

.navigation-expansion :deep(.q-item__label) {
  font-size: 12.5px;
  font-weight: 650;
}

.navigation-expansion :deep(.q-item__label--caption) {
  margin-top: 2px;
  color: #8a96a7;
  font-size: 9.5px;
  font-weight: 500;
}

.navigation-expansion :deep(.q-expansion-item__toggle-icon) {
  color: #94a3b8;
  font-size: 18px;
}

.navigation-subitem {
  min-height: 41px;
  margin: 2px 0 2px 18px;
  border-radius: 8px;
  color: #637186;
  transition:
    background 0.18s ease,
    color 0.18s ease;
}

.navigation-subitem:hover {
  background: #f7f9fc;
  color: #334155;
}

.navigation-subitem--active {
  background: #edf3ff !important;
  color: #2563eb !important;
}

.navigation-subitem .q-item__section--avatar {
  min-width: 35px;
  color: inherit;
}

.navigation-subitem .q-icon {
  font-size: 17px;
}

.navigation-subitem .q-item__label {
  font-size: 11.5px;
  font-weight: 600;
}

.drawer-footer {
  margin: 7px 12px 12px;
  padding: 10px 11px;
  border: 1px solid #e8edf4;
  border-radius: 11px;
  background: #fafbfc;
}

.footer-status {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #526071;
  font-size: 10px;
  font-weight: 700;
}

.status-dot {
  width: 7px;
  height: 7px;
  display: inline-block;
  flex-shrink: 0;
  border-radius: 50%;
  background: #22c55e;
  box-shadow:
    0 0 0 3px rgba(34, 197, 94, 0.12);
}

.footer-version {
  margin-top: 5px;
  color: #8d98a8;
  font-size: 8px;
  line-height: 1.4;
}

/* ==================== DARK MODE ==================== */

:global(.body--dark) .somi-layout,
:global(.body--dark) .somi-page-container {
  background: #0f172a;
}

:global(.body--dark) .somi-header {
  background: rgba(17, 24, 39, 0.98);
  color: #f8fafc;
  border-color: #1f2937;
}

:global(.body--dark) .header-action {
  color: #aeb9c8;
}

:global(.body--dark) .header-action:hover {
  background: #172033;
  color: #7da2ff;
}

:global(.body--dark) .header-logout:hover {
  background: #321c23;
  color: #f87171;
}

:global(.body--dark) .header-title-main,
:global(.body--dark) .mobile-brand-name {
  color: #f8fafc;
}

:global(.body--dark) .header-title-caption,
:global(.body--dark) .mobile-brand-caption {
  color: #94a3b8;
}

:global(.body--dark) .header-user-name {
  color: #e5e7eb;
}

:global(.body--dark) .header-user-role {
  color: #8fa0b5;
}

:global(.body--dark) .header-user-avatar {
  background: #1d2b4d;
  border-color: #334155;
}

:global(.body--dark) .somi-drawer {
  background: #111827;
  color: #e5e7eb;
  border-color: #1f2937;
}

:global(.body--dark) .drawer-brand,
:global(.body--dark) .drawer-profile,
:global(.body--dark) .drawer-footer {
  border-color: #1f2937;
}

:global(.body--dark) .drawer-profile,
:global(.body--dark) .drawer-footer {
  background: #172033;
}

:global(.body--dark) .drawer-profile:hover {
  background: #1a2538;
  border-color: #293850;
}

:global(.body--dark) .brand-name,
:global(.body--dark) .profile-name {
  color: #f8fafc;
}

:global(.body--dark) .brand-subtitle,
:global(.body--dark) .profile-email,
:global(.body--dark) .footer-version {
  color: #8fa0b5;
}

:global(.body--dark) .profile-avatar {
  background: #1d2b4d;
  border-color: #334155;
}

:global(.body--dark) .profile-role {
  background: #1d2b4d;
  color: #8fb0ff;
}

:global(.body--dark) .navigation-label,
:global(.body--dark) .navigation-sub-label {
  color: #8fa0b5;
}

:global(.body--dark) .navigation-item,
:global(.body--dark) .navigation-expansion {
  color: #b2bdcc;
}

:global(.body--dark) .navigation-item:hover,
:global(.body--dark) .navigation-expansion-header:hover,
:global(.body--dark) .navigation-subitem:hover {
  background: #172033;
}

:global(.body--dark) .navigation-item--active,
:global(.body--dark) .navigation-subitem--active {
  background: #1d2b4d !important;
  color: #7da2ff !important;
}

:global(.body--dark) .navigation-item--active .q-icon {
  color: #7da2ff;
}

:global(.body--dark) .navigation-item .q-item__label--caption,
:global(.body--dark) .navigation-expansion :deep(.q-item__label--caption) {
  color: #8797ad;
}

:global(.body--dark) .navigation-expansion :deep(.q-expansion-item__toggle-icon) {
  color: #718096;
}

:global(.body--dark) .footer-status {
  color: #b8c3d1;
}

:global(.body--dark) .navigation-wrapper {
  scrollbar-color: #334155 transparent;
}

:global(.body--dark) .navigation-wrapper::-webkit-scrollbar-thumb {
  background: #334155;
}

/* ==================== RESPONSIVE ==================== */

@media (max-width: 900px) {
  .somi-toolbar {
    min-height: 62px;
    padding: 0 10px;
  }

  .desktop-header-title {
    display: none;
  }

  .mobile-brand {
    display: flex;
  }
}

@media (max-width: 599px) {
  .header-user {
    display: none;
  }

  .mobile-brand {
    margin-left: 7px;
  }

  .mobile-brand-caption {
    display: none;
  }

  .mobile-brand-name {
    font-size: 14px;
  }

  .somi-toolbar {
    padding: 0 7px;
  }

  .header-action {
    margin-left: 0;
  }
}
</style>


