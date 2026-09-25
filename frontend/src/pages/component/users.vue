<template>
  <div class="users-page q-pa-lg">
    <!-- Page Header -->
    <div class="page-header row items-center justify-between q-mb-lg">
      <div>
        <div class="eyebrow">SYSTEM ADMINISTRATION</div>

        <div class="page-title">
          Users
        </div>

        <div class="page-subtitle">
          Manage system accounts, roles and access.
        </div>
      </div>

      <div class="header-actions row items-center q-gutter-sm">
        <q-btn
          flat
          round
          dense
          icon="refresh"
          :loading="loading"
          @click="loadUsers"
        >
          <q-tooltip>
            Refresh users
          </q-tooltip>
        </q-btn>

        <q-btn
          v-if="canCreate"
          unelevated
          no-caps
          color="primary"
          icon="person_add"
          label="Add User"
          class="add-user-btn"
          @click="openCreateDialog"
        />
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-grid q-mb-lg">
      <q-card class="summary-card">
        <div class="summary-icon summary-icon--users">
          <q-icon name="people" size="21px" />
        </div>
        <div class="summary-content">
          <div class="summary-label">Total Users</div>
          <div class="summary-value">{{ users.length }}</div>
          <div class="summary-caption">System accounts</div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--active">
          <q-icon name="verified_user" size="21px" />
        </div>
        <div class="summary-content">
          <div class="summary-label">Active Users</div>
          <div class="summary-value">{{ activeUsers }}</div>
          <div class="summary-caption">Currently active</div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--admin">
          <q-icon name="admin_panel_settings" size="21px" />
        </div>
        <div class="summary-content">
          <div class="summary-label">Administrators</div>
          <div class="summary-value">{{ adminCount }}</div>
          <div class="summary-caption">Admin accounts</div>
        </div>
      </q-card>

      <q-card class="summary-card">
        <div class="summary-icon summary-icon--manager">
          <q-icon name="manage_accounts" size="21px" />
        </div>
        <div class="summary-content">
          <div class="summary-label">Managers</div>
          <div class="summary-value">{{ managerCount }}</div>
          <div class="summary-caption">Manager accounts</div>
        </div>
      </q-card>
    </div>

    <!-- Toolbar -->
    <div class="toolbar q-mb-lg">
      <div class="search-wrapper">
        <q-input
          v-model="search"
          outlined
          dense
          clearable
          debounce="350"
          placeholder="Search users..."
          class="search-input"
          @update:model-value="applyFilters"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>

      <q-select
        v-model="roleFilter"
        outlined
        dense
        clearable
        emit-value
        map-options
        :options="roleOptions"
        label="Role"
        class="filter-select"
        @update:model-value="loadUsers"
      />

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
        @update:model-value="loadUsers"
      />

      <q-btn
        v-if="search || roleFilter || statusFilter"
        flat
        dense
        no-caps
        icon="filter_alt_off"
        label="Clear"
        @click="clearFilters"
      />
    </div>

    <!-- Error -->
    <q-banner
      v-if="error"
      rounded
      class="error-banner q-mb-lg"
    >
      <template #avatar>
        <q-icon name="error_outline" />
      </template>

      {{ error }}

      <template #action>
        <q-btn
          flat
          no-caps
          label="Retry"
          @click="loadUsers"
        />
      </template>
    </q-banner>

    <!-- Loading -->
    <div
      v-if="loading"
      class="state-container"
    >
      <q-spinner-dots
        color="primary"
        size="42px"
      />

      <div class="state-title">
        Loading users...
      </div>

      <div class="state-text">
        Please wait while user accounts are loaded.
      </div>
    </div>

    <!-- Empty -->
    <div
      v-else-if="filteredUsers.length === 0"
      class="state-container"
    >
      <div class="empty-icon">
        <q-icon
          name="people_outline"
          size="42px"
        />
      </div>

      <div class="state-title">
        No users found
      </div>

      <div class="state-text">
        {{
          search || roleFilter || statusFilter
            ? "Try changing your search or filters."
            : "There are no user accounts yet."
        }}
      </div>

      <q-btn
        v-if="canCreate && !search && !roleFilter && !statusFilter"
        unelevated
        no-caps
        color="primary"
        icon="person_add"
        label="Add First User"
        class="q-mt-md"
        @click="openCreateDialog"
      />
    </div>

    <!-- User Cards -->
    <div
      v-else
      class="users-grid"
    >
      <q-card
        v-for="user in filteredUsers"
        :key="user.id"
        class="user-card"
        :class="{
          'user-card--selected': selectedUsers.includes(user.id)
        }"
      >
        <!-- Card Top -->
        <div class="card-top">
          <q-checkbox
            v-model="selectedUsers"
            :val="user.id"
            dense
          />

          <div class="card-actions">
            <q-chip
              dense
              class="status-chip"
              :class="
                isUserActive(user)
                  ? 'status-active'
                  : 'status-inactive'
              "
            >
              <span
                class="status-dot"
                :class="{
                  active: isUserActive(user)
                }"
              />

              {{
                isUserActive(user)
                  ? "Active"
                  : "Not Active"
              }}
            </q-chip>

            <q-btn
              flat
              round
              dense
              icon="more_horiz"
              class="more-btn"
            >
              <q-menu
                anchor="bottom right"
                self="top right"
                class="user-menu"
              >
                <q-list
                  dense
                  style="min-width: 170px"
                >
                  <q-item
                    clickable
                    v-close-popup
                    @click="openViewDialog(user)"
                  >
                    <q-item-section avatar>
                      <q-icon name="visibility" />
                    </q-item-section>

                    <q-item-section>
                      View Account
                    </q-item-section>
                  </q-item>

                  <q-item
                    v-if="canEdit"
                    clickable
                    v-close-popup
                    @click="openEditDialog(user)"
                  >
                    <q-item-section avatar>
                      <q-icon name="edit" />
                    </q-item-section>

                    <q-item-section>
                      Edit User
                    </q-item-section>
                  </q-item>

                  <q-item
                    v-if="canEdit"
                    clickable
                    v-close-popup
                    @click="toggleAccountStatus(user)"
                  >
                    <q-item-section avatar>
                      <q-icon
                        :name="
                          isUserActive(user)
                            ? 'person_off'
                            : 'person'
                        "
                      />
                    </q-item-section>

                    <q-item-section>
                      {{
                        isUserActive(user)
                          ? "Disable Account"
                          : "Activate Account"
                      }}
                    </q-item-section>
                  </q-item>

                  <q-separator
                    v-if="canDelete(user)"
                    class="q-my-xs"
                  />

                  <q-item
                    v-if="canDelete(user)"
                    clickable
                    v-close-popup
                    class="delete-menu-item"
                    @click="confirmDelete(user)"
                  >
                    <q-item-section avatar>
                      <q-icon name="delete_outline" />
                    </q-item-section>

                    <q-item-section>
                      Delete User
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>
        </div>

        <!-- Avatar -->
        <div class="avatar-section">
          <q-avatar
            size="78px"
            class="user-avatar"
          >
            <img
              v-if="profileImage(user)"
              :src="profileImage(user)"
              alt="User profile"
            />

            <span v-else>
              {{ getInitials(user) }}
            </span>
          </q-avatar>
        </div>

        <!-- User Identity -->
        <div class="user-identity">
          <div class="user-name">
            {{ getFullName(user) }}
          </div>

          <div class="user-username">
            @{{ user.username }}
          </div>

          <div
            class="user-role"
            :class="`role-${String(
              user.role || ''
            ).toLowerCase()}`"
          >
            <q-icon
              :name="roleIcon(user.role)"
              size="14px"
            />

            {{ formatRole(user.role) }}
          </div>
        </div>

        <!-- Information Panel -->
        <div class="info-panel">
          <div class="info-row">
            <span class="info-label">
              Account
            </span>

            <span class="info-value">
              {{
                isUserActive(user)
                  ? "Active"
                  : "Disabled"
              }}
            </span>
          </div>

          <div class="info-row">
            <span class="info-label">
              Joined
            </span>

            <span class="info-value">
              {{ formatDate(user.date_joined) }}
            </span>
          </div>
        </div>

        <!-- Contact -->
        <div class="contact-section">
          <div class="contact-row">
            <q-icon
              name="email"
              size="15px"
            />

            <span>
              {{ user.email || "No email" }}
            </span>
          </div>

          <div class="contact-row">
            <q-icon
              name="phone"
              size="15px"
            />

            <span>
              {{ user.phone || "No phone" }}
            </span>
          </div>
        </div>
      </q-card>
    </div>

    <!-- Selected Toolbar -->
    <transition name="slide-up">
      <div
        v-if="selectedUsers.length"
        class="selection-bar"
      >
        <div>
          <strong>
            {{ selectedUsers.length }}
          </strong>

          user{{ selectedUsers.length > 1 ? "s" : "" }}
          selected
        </div>

        <div class="row q-gutter-sm">
          <q-btn
            flat
            dense
            no-caps
            label="Clear Selection"
            @click="selectedUsers = []"
          />
        </div>
      </div>
    </transition>

    <!-- Create / Edit Dialog -->
    <q-dialog
      v-model="showFormDialog"
      persistent
    >
      <q-card class="user-dialog">
        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">
              {{
                editingUser
                  ? "Edit User"
                  : "Add User"
              }}
            </div>

            <div class="dialog-subtitle">
              {{
                editingUser
                  ? "Update account details and access."
                  : "Create a new SOMI system account."
              }}
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            :disable="saving"
            @click="closeFormDialog"
          />
        </q-card-section>

        <q-separator />

        <q-form @submit.prevent="saveUser">
          <q-card-section class="dialog-body">
            <!-- Preview -->
            <div class="account-preview">
              <q-avatar
                size="58px"
                class="preview-avatar"
              >
                <span>
                  {{ getInitials(form) }}
                </span>
              </q-avatar>

              <div>
                <div class="preview-name">
                  {{
                    form.first_name ||
                    form.last_name
                      ? `${form.first_name} ${form.last_name}`.trim()
                      : "New User"
                  }}
                </div>

                <div class="preview-role">
                  {{ formatRole(form.role) }}
                </div>
              </div>
            </div>

            <div class="form-section-title">
              Personal Information
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.first_name"
                  outlined
                  label="First Name"
                  maxlength="50"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.last_name"
                  outlined
                  label="Last Name"
                  maxlength="50"
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.email"
                  outlined
                  type="email"
                  label="Email"
                  :rules="[
                    val =>
                      !!val ||
                      'Email is required',
                    val =>
                      /.+@.+\..+/.test(val) ||
                      'Enter a valid email'
                  ]"
                >
                  <template #prepend>
                    <q-icon name="email" />
                  </template>
                </q-input>
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.phone"
                  outlined
                  label="Phone"
                  maxlength="20"
                >
                  <template #prepend>
                    <q-icon name="phone" />
                  </template>
                </q-input>
              </div>
            </div>

            <div class="form-section-title q-mt-lg">
              Account Access
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.username"
                  outlined
                  label="Username"
                  :rules="[
                    val =>
                      !!val ||
                      'Username is required'
                  ]"
                >
                  <template #prepend>
                    <q-icon name="person" />
                  </template>
                </q-input>
              </div>

              <div class="col-12 col-md-6">
                <q-select
                  v-model="form.role"
                  outlined
                  emit-value
                  map-options
                  :options="formRoleOptions"
                  label="System Role"
                  :disable="!isAdmin"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.password"
                  outlined
                  :type="
                    showPassword
                      ? 'text'
                      : 'password'
                  "
                  :label="
                    editingUser
                      ? 'New Password (optional)'
                      : 'Password'
                  "
                  :rules="
                    editingUser
                      ? []
                      : [
                          val =>
                            !!val ||
                            'Password is required',
                          val =>
                            val.length >= 8 ||
                            'Minimum 8 characters'
                        ]
                  "
                >
                  <template #prepend>
                    <q-icon name="lock" />
                  </template>

                  <template #append>
                    <q-icon
                      :name="
                        showPassword
                          ? 'visibility_off'
                          : 'visibility'
                      "
                      class="cursor-pointer"
                      @click="
                        showPassword =
                          !showPassword
                      "
                    />
                  </template>
                </q-input>
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model="
                    form.password_confirm
                  "
                  outlined
                  type="password"
                  :label="
                    editingUser
                      ? 'Confirm New Password'
                      : 'Confirm Password'
                  "
                />
              </div>

              <div class="col-12">
                <q-toggle
                  v-model="
                    form.is_active_account
                  "
                  color="primary"
                  label="Account is active"
                  :disable="
                    editingUser &&
                    form.id === currentUserId
                  "
                />

                <div class="field-help">
                  Disabled accounts cannot sign in
                  to SOMI.
                </div>
              </div>
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
              :disable="saving"
              @click="closeFormDialog"
            />

            <q-btn
              unelevated
              no-caps
              color="primary"
              :label="
                editingUser
                  ? 'Save Changes'
                  : 'Create User'
              "
              :loading="saving"
              type="submit"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <!-- View Dialog -->
    <q-dialog v-model="showViewDialog">
      <q-card class="view-dialog">
        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">
              User Account
            </div>

            <div class="dialog-subtitle">
              Account details and access status.
            </div>
          </div>

          <q-btn
            flat
            round
            dense
            icon="close"
            @click="
              showViewDialog = false
            "
          />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="viewingUser">
          <div class="profile-header">
            <q-avatar
              size="78px"
              class="profile-avatar"
            >
              <img
                v-if="profileImage(viewingUser)"
                :src="
                  profileImage(viewingUser)
                "
                alt="Profile"
              />

              <span v-else>
                {{ getInitials(viewingUser) }}
              </span>
            </q-avatar>

            <div>
              <div class="profile-name">
                {{ getFullName(viewingUser) }}
              </div>

              <div class="profile-username">
                @{{ viewingUser.username }}
              </div>

              <div
                class="profile-role"
                :class="
                  `role-${String(
                    viewingUser.role || ''
                  ).toLowerCase()}`
                "
              >
                <q-icon
                  :name="
                    roleIcon(
                      viewingUser.role
                    )
                  "
                  size="15px"
                />

                {{ formatRole(viewingUser.role) }}
              </div>
            </div>
          </div>

          <div class="view-details">
            <div class="view-detail">
              <span>Email</span>
              <strong>
                {{ viewingUser.email || "—" }}
              </strong>
            </div>

            <div class="view-detail">
              <span>Phone</span>
              <strong>
                {{ viewingUser.phone || "—" }}
              </strong>
            </div>

            <div class="view-detail">
              <span>Status</span>
              <strong>
                {{
                  isUserActive(viewingUser)
                    ? "Active"
                    : "Not Active"
                }}
              </strong>
            </div>

            <div class="view-detail">
              <span>Joined</span>
              <strong>
                {{
                  formatDate(
                    viewingUser.date_joined
                  )
                }}
              </strong>
            </div>
          </div>
        </q-card-section>

        <q-card-actions
          align="right"
          class="dialog-actions"
        >
          <q-btn
            flat
            no-caps
            label="Close"
            @click="
              showViewDialog = false
            "
          />

          <q-btn
            v-if="canEdit && viewingUser"
            unelevated
            no-caps
            color="primary"
            icon="edit"
            label="Edit"
            @click="
              openEditDialog(viewingUser)
            "
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import api from "src/services/api";

export default {
  name: "UsersPage",

  data() {
    return {
      users: [],
      filteredUsers: [],
      selectedUsers: [],

      loading: false,
      saving: false,

      error: null,

      search: "",
      roleFilter: null,
      statusFilter: null,

      showFormDialog: false,
      showViewDialog: false,

      editingUser: null,
      viewingUser: null,

      showPassword: false,

      form: this.emptyForm(),

      roleOptions: [
        {
          label: "Admin",
          value: "ADMIN",
        },
        {
          label: "Manager",
          value: "MANAGER",
        },
        {
          label: "Employee",
          value: "EMPLOYEE",
        },
      ],

      statusOptions: [
        {
          label: "Active",
          value: "ACTIVE",
        },
        {
          label: "Inactive",
          value: "INACTIVE",
        },
        {
          label: "Disabled",
          value: "DISABLED",
        },
      ],
    };
  },

  computed: {
    currentUser() {
      return this.$store.state.user || {};
    },

    currentUserId() {
      return this.currentUser?.id || null;
    },

    isAdmin() {
      return (
        this.$store.getters.isAdmin === true ||
        this.currentUser?.role === "ADMIN"
      );
    },

    isManager() {
      return (
        this.$store.getters.isManager === true ||
        this.currentUser?.role === "MANAGER"
      );
    },

    canCreate() {
      return this.isAdmin || this.isManager;
    },

    canEdit() {
      return this.isAdmin || this.isManager;
    },

    activeUsers() {
      return this.users.filter(
        user => this.isUserActive(user)
      ).length;
    },

    adminCount() {
      return this.users.filter(
        user => user.role === "ADMIN"
      ).length;
    },

    managerCount() {
      return this.users.filter(
        user => user.role === "MANAGER"
      ).length;
    },

    formRoleOptions() {
      if (this.isAdmin) {
        return this.roleOptions;
      }

      return this.roleOptions.filter(
        option =>
          option.value === "EMPLOYEE"
      );
    },
  },

  mounted() {
    this.loadUsers();
  },

  methods: {
    emptyForm() {
      return {
        id: null,
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        phone: "",
        role: "EMPLOYEE",
        password: "",
        password_confirm: "",
        is_active_account: true,
        is_active: true,
        profile_picture: null,
      };
    },

    async loadUsers() {
      this.loading = true;
      this.error = null;

      try {
        const params = {};

        if (this.search.trim()) {
          params.search = this.search.trim();
        }

        if (this.roleFilter) {
          params.role = this.roleFilter;
        }

        if (this.statusFilter) {
          params.status = this.statusFilter;
        }

        const response = await api.get(
          "/auth/users/",
          { params }
        );

        const data = response.data;

        this.users = Array.isArray(data)
          ? data
          : data.results || [];

        this.applyFilters();
      } catch (error) {
        console.error(
          "Failed to load users:",
          error
        );

        this.users = [];
        this.filteredUsers = [];

        this.error =
          error.response?.data?.detail ||
          "Unable to load user accounts.";
      } finally {
        this.loading = false;
      }
    },

    applyFilters() {
      const term = this.search
        .trim()
        .toLowerCase();

      this.filteredUsers =
        this.users.filter(user => {
          if (!term) {
            return true;
          }

          const values = [
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            this.getFullName(user),
          ];

          return values.some(value =>
            String(value || "")
              .toLowerCase()
              .includes(term)
          );
        });
    },

    clearFilters() {
      this.search = "";
      this.roleFilter = null;
      this.statusFilter = null;
      this.loadUsers();
    },

    openCreateDialog() {
      this.editingUser = null;
      this.form = this.emptyForm();
      this.showPassword = false;
      this.showFormDialog = true;
    },

    openEditDialog(user) {
      this.editingUser = user;

      this.form = {
        id: user.id,
        username: user.username || "",
        email: user.email || "",
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        phone: user.phone || "",
        role: user.role || "EMPLOYEE",
        password: "",
        password_confirm: "",
        is_active_account:
          user.is_active_account !== false,
        is_active:
          user.is_active !== false,
        profile_picture:
          user.profile_picture || null,
      };

      this.showPassword = false;
      this.showViewDialog = false;
      this.showFormDialog = true;
    },

    closeFormDialog() {
      if (this.saving) {
        return;
      }

      this.showFormDialog = false;
      this.editingUser = null;
      this.form = this.emptyForm();
      this.showPassword = false;
    },

    openViewDialog(user) {
      this.viewingUser = user;
      this.showViewDialog = true;
    },

    async saveUser() {
      if (!this.form.username.trim()) {
        this.notify(
          "Username is required.",
          "negative"
        );
        return;
      }

      if (!this.form.email.trim()) {
        this.notify(
          "Email is required.",
          "negative"
        );
        return;
      }

      if (
        !this.editingUser &&
        !this.form.password
      ) {
        this.notify(
          "Password is required.",
          "negative"
        );
        return;
      }

      if (
        this.form.password &&
        this.form.password.length < 8
      ) {
        this.notify(
          "Password must be at least 8 characters.",
          "negative"
        );
        return;
      }

      if (
        this.form.password ||
        this.form.password_confirm
      ) {
        if (
          this.form.password !==
          this.form.password_confirm
        ) {
          this.notify(
            "Passwords do not match.",
            "negative"
          );
          return;
        }
      }

      this.saving = true;

      try {
        const payload = {
          username:
            this.form.username.trim(),

          email:
            this.form.email.trim(),

          first_name:
            this.form.first_name.trim(),

          last_name:
            this.form.last_name.trim(),

          phone:
            this.form.phone?.trim() || "",

          role: this.form.role,

          is_active_account:
            this.form.is_active_account,
        };

        if (this.form.password) {
          payload.password =
            this.form.password;

          payload.password_confirm =
            this.form.password_confirm;
        }

        if (this.editingUser) {
          await api.patch(
            `/auth/users/${this.editingUser.id}/`,
            payload
          );

          this.notify(
            "User updated successfully.",
            "positive"
          );
        } else {
          await api.post(
            "/auth/users/",
            payload
          );

          this.notify(
            "User created successfully.",
            "positive"
          );
        }

        this.closeFormDialog();
        await this.loadUsers();
      } catch (error) {
        console.error(
          "Failed to save user:",
          error
        );

        this.notify(
          this.extractApiError(error) ||
            "Unable to save user.",
          "negative"
        );
      } finally {
        this.saving = false;
      }
    },

    async toggleAccountStatus(user) {
      if (
        user.id === this.currentUserId &&
        isUserActiveSafe(user)
      ) {
        this.notify(
          "You cannot disable your own account.",
          "negative"
        );
        return;
      }

      const nextStatus =
        !this.isUserActive(user);

      this.$q
        .dialog({
          title: nextStatus
            ? "Activate Account"
            : "Disable Account",
          message: nextStatus
            ? `Activate ${this.getFullName(
                user
              )}'s account?`
            : `Disable ${this.getFullName(
                user
              )}'s account?`,
          cancel: true,
          persistent: true,
        })
        .onOk(async () => {
          try {
            await api.patch(
              `/auth/users/${user.id}/`,
              {
                is_active_account:
                  nextStatus,
              }
            );

            this.notify(
              nextStatus
                ? "Account activated successfully."
                : "Account disabled successfully.",
              "positive"
            );

            await this.loadUsers();
          } catch (error) {
            this.notify(
              this.extractApiError(error) ||
                "Unable to update account status.",
              "negative"
            );
          }
        });
    },

    canDelete(user) {
      return (
        this.isAdmin &&
        user.id !== this.currentUserId
      );
    },

    confirmDelete(user) {
      this.$q
        .dialog({
          title: "Delete User",
          message: `Are you sure you want to permanently delete ${this.getFullName(
            user
          )}?`,
          cancel: true,
          persistent: true,
          ok: {
            color: "negative",
            label: "Delete",
            unelevated: true,
          },
        })
        .onOk(() => {
          this.deleteUser(user);
        });
    },

    async deleteUser(user) {
      try {
        await api.delete(
          `/auth/users/${user.id}/`
        );

        this.selectedUsers =
          this.selectedUsers.filter(
            id => id !== user.id
          );

        this.notify(
          "User deleted successfully.",
          "positive"
        );

        await this.loadUsers();
      } catch (error) {
        this.notify(
          this.extractApiError(error) ||
            "Unable to delete user.",
          "negative"
        );
      }
    },

    getFullName(user) {
      const name = [
        user?.first_name,
        user?.last_name,
      ]
        .filter(Boolean)
        .join(" ")
        .trim();

      return name || user?.username || "Unknown User";
    },

    getInitials(user) {
      const name = this.getFullName(user);

      if (!name) {
        return "U";
      }

      const parts = name
        .split(" ")
        .filter(Boolean);

      if (parts.length === 1) {
        return parts[0]
          .substring(0, 2)
          .toUpperCase();
      }

      return (
        parts[0][0] +
        parts[parts.length - 1][0]
      ).toUpperCase();
    },

    profileImage(user) {
      if (!user?.profile_picture) {
        return null;
      }

      if (
        user.profile_picture.startsWith(
          "http"
        )
      ) {
        return user.profile_picture;
      }

      return `http://127.0.0.1:8000${user.profile_picture}`;
    },

    isUserActive(user) {
      return (
        user?.is_active === true &&
        user?.is_active_account === true
      );
    },

    formatRole(role) {
      const labels = {
        ADMIN: "Administrator",
        MANAGER: "Manager",
        EMPLOYEE: "Employee",
      };

      return (
        labels[role] ||
        role ||
        "User"
      );
    },

    roleIcon(role) {
      const icons = {
        ADMIN:
          "admin_panel_settings",
        MANAGER:
          "manage_accounts",
        EMPLOYEE: "person",
      };

      return icons[role] || "person";
    },

    formatDate(value) {
      if (!value) {
        return "—";
      }

      const date = new Date(value);

      if (
        Number.isNaN(date.getTime())
      ) {
        return "—";
      }

      return new Intl.DateTimeFormat(
        "en-GB",
        {
          day: "2-digit",
          month: "short",
          year: "numeric",
        }
      ).format(date);
    },

    extractApiError(error) {
      const data =
        error.response?.data;

      if (!data) {
        return null;
      }

      if (
        typeof data.detail === "string"
      ) {
        return data.detail;
      }

      const messages = [];

      Object.keys(data).forEach(
        key => {
          const value = data[key];

          if (Array.isArray(value)) {
            messages.push(
              `${key}: ${value.join(
                ", "
              )}`
            );
          } else if (
            typeof value === "string"
          ) {
            messages.push(
              `${key}: ${value}`
            );
          }
        }
      );

      return messages.length
        ? messages.join(" | ")
        : null;
    },

    notify(
      message,
      type = "positive"
    ) {
      this.$q.notify({
        type,
        message,
        position: "top-right",
        timeout: 3000,
      });
    },
  },
};

function isUserActiveSafe(user) {
  return (
    user?.is_active === true &&
    user?.is_active_account === true
  );
}
</script>

<style scoped>
.users-page {
  min-height: 100%;
}

/* Header */

.page-header {
  gap: 18px;
}

.eyebrow {
  color: #64748b;
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 1.3px;
  margin-bottom: 4px;
}

.page-title {
  color: #172033;
  font-size: 26px;
  font-weight: 750;
  line-height: 1.2;
}

.page-subtitle {
  color: #7a8699;
  font-size: 13px;
  margin-top: 5px;
}

.add-user-btn {
  min-height: 38px;
  border-radius: 8px;
}

/* Summary Cards */

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.summary-card {
  align-items: center;
  background: #ffffff;
  border: 1px solid #e6ebf1;
  border-radius: 10px;
  box-shadow: 0 3px 12px rgba(15, 23, 42, 0.045);
  display: flex;
  gap: 13px;
  min-height: 88px;
  padding: 14px 16px;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.summary-card:hover {
  border-color: #d3dce7;
  box-shadow: 0 7px 20px rgba(15, 23, 42, 0.075);
  transform: translateY(-1px);
}

.summary-icon {
  align-items: center;
  border-radius: 9px;
  display: flex;
  flex-shrink: 0;
  height: 43px;
  justify-content: center;
  width: 43px;
}

.summary-icon--users { background: #eef4ff; color: #2563eb; }
.summary-icon--active { background: #ecfdf5; color: #059669; }
.summary-icon--admin { background: #f3efff; color: #7c3aed; }
.summary-icon--manager { background: #fff7ed; color: #ea580c; }

.summary-content { min-width: 0; }

.summary-label {
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.2;
}

.summary-value {
  color: #172033;
  font-size: 23px;
  font-weight: 750;
  line-height: 1.15;
  margin-top: 3px;
}

.summary-caption {
  color: #9aa5b5;
  font-size: 9px;
  margin-top: 3px;
}

/* Toolbar */

.toolbar {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.search-wrapper {
  flex: 1 1 300px;
  min-width: 220px;
}

.search-input {
  width: 100%;
}

.filter-select {
  min-width: 145px;
}

/* Grid */

.users-grid {
  display: grid;
  grid-template-columns: repeat(
    4,
    minmax(0, 1fr)
  );
  gap: 16px;
}

/* User Card */

.user-card {
  background: #ffffff;
  border: 1px solid #e4e9ef;
  border-radius: 9px;
  box-shadow: 0 3px 12px
    rgba(15, 23, 42, 0.045);
  min-width: 0;
  overflow: hidden;
  padding: 11px;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease;
}

.user-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 8px 22px
    rgba(15, 23, 42, 0.09);
  transform: translateY(-2px);
}

.user-card--selected {
  border-color: #60a5fa;
  box-shadow: 0 0 0 2px
    rgba(37, 99, 235, 0.08);
}

.card-top {
  align-items: center;
  display: flex;
  justify-content: space-between;
  min-height: 28px;
}

.card-actions {
  align-items: center;
  display: flex;
  gap: 3px;
}

.status-chip {
  border-radius: 5px;
  font-size: 10px;
  font-weight: 650;
  min-height: 22px;
  padding: 0 7px;
}

.status-active {
  background: #ecfdf5;
  color: #059669;
}

.status-inactive {
  background: #fff7ed;
  color: #c2410c;
}

.status-dot {
  background: #fb923c;
  border-radius: 50%;
  display: inline-block;
  height: 5px;
  margin-right: 5px;
  width: 5px;
}

.status-dot.active {
  background: #10b981;
}

.more-btn {
  color: #64748b;
}

.user-menu {
  border: 1px solid #e7ebf0;
  border-radius: 9px;
  box-shadow: 0 10px 30px
    rgba(15, 23, 42, 0.12);
}

.delete-menu-item {
  color: #dc2626;
}

/* Avatar */

.avatar-section {
  align-items: center;
  display: flex;
  justify-content: center;
  margin-top: 4px;
}

.user-avatar {
  background: #eef2f7;
  border: 1px solid #edf1f5;
  color: #64748b;
  font-size: 19px;
  font-weight: 700;
  overflow: hidden;
}

.user-avatar img {
  height: 100%;
  object-fit: cover;
  width: 100%;
}

/* Identity */

.user-identity {
  margin-top: 9px;
  text-align: center;
}

.user-name {
  color: #111827;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.25;
}

.user-username {
  color: #94a3b8;
  font-size: 10px;
  margin-top: 3px;
}

.user-role {
  align-items: center;
  display: inline-flex;
  font-size: 11px;
  font-weight: 600;
  gap: 4px;
  margin-top: 4px;
}

.role-admin {
  color: #7c3aed;
}

.role-manager {
  color: #2563eb;
}

.role-employee {
  color: #64748b;
}

/* Information */

.info-panel {
  background: #f7f9fb;
  border: 1px solid #edf1f4;
  border-radius: 5px;
  margin-top: 11px;
  overflow: hidden;
}

.info-row {
  align-items: center;
  display: flex;
  justify-content: space-between;
  min-height: 29px;
  padding: 0 8px;
}

.info-row + .info-row {
  border-top: 1px solid #e9edf1;
}

.info-label {
  color: #7c8798;
  font-size: 9px;
}

.info-value {
  color: #374151;
  font-size: 9px;
  font-weight: 600;
}

/* Contact */

.contact-section {
  margin-top: 9px;
}

.contact-row {
  align-items: center;
  color: #566274;
  display: flex;
  font-size: 10px;
  gap: 6px;
  line-height: 1.5;
  min-height: 21px;
  overflow: hidden;
}

.contact-row .q-icon {
  color: #475569;
  flex-shrink: 0;
}

.contact-row span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Selection */

.selection-bar {
  align-items: center;
  background: #172033;
  border-radius: 9px;
  bottom: 20px;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  left: 50%;
  padding: 9px 12px 9px 16px;
  position: fixed;
  transform: translateX(-50%);
  width: min(420px, calc(100vw - 30px));
  z-index: 5000;
}

.selection-bar .q-btn {
  color: #cbd5e1;
}

/* States */

.state-container {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 350px;
  text-align: center;
}

.empty-icon {
  align-items: center;
  background: #f1f5f9;
  border-radius: 18px;
  color: #94a3b8;
  display: flex;
  height: 70px;
  justify-content: center;
  width: 70px;
}

.state-title {
  color: #1e293b;
  font-size: 17px;
  font-weight: 700;
  margin-top: 15px;
}

.state-text {
  color: #94a3b8;
  font-size: 12px;
  margin-top: 4px;
}

.error-banner {
  background: #fff1f2;
  color: #be123c;
}

/* Dialog */

.user-dialog,
.view-dialog {
  border-radius: 15px;
  max-width: 94vw;
  overflow: hidden;
  width: 650px;
}

.dialog-header {
  align-items: flex-start;
  display: flex;
  justify-content: space-between;
  padding: 19px 21px;
}

.dialog-title {
  color: #172033;
  font-size: 18px;
  font-weight: 750;
}

.dialog-subtitle {
  color: #7c8798;
  font-size: 12px;
  margin-top: 3px;
}

.dialog-body {
  max-height: 70vh;
  overflow-y: auto;
  padding: 21px;
}

.account-preview {
  align-items: center;
  background: #f7faff;
  border: 1px solid #e7eef8;
  border-radius: 10px;
  display: flex;
  gap: 12px;
  margin-bottom: 21px;
  padding: 12px;
}

.preview-avatar {
  background: #e8f0ff;
  color: #2563eb;
  font-weight: 750;
}

.preview-name {
  color: #1e293b;
  font-size: 15px;
  font-weight: 700;
}

.preview-role {
  color: #64748b;
  font-size: 11px;
  margin-top: 2px;
}

.form-section-title {
  color: #475569;
  font-size: 11px;
  font-weight: 750;
  letter-spacing: 0.6px;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.field-help {
  color: #94a3b8;
  font-size: 10px;
  margin-left: 8px;
  margin-top: -3px;
}

.dialog-actions {
  padding: 13px 19px;
}

/* View */

.profile-header {
  align-items: center;
  display: flex;
  gap: 16px;
}

.profile-avatar {
  background: #eef2ff;
  color: #2563eb;
  font-weight: 750;
}

.profile-avatar img {
  height: 100%;
  object-fit: cover;
  width: 100%;
}

.profile-name {
  color: #172033;
  font-size: 19px;
  font-weight: 750;
}

.profile-username {
  color: #94a3b8;
  font-size: 12px;
  margin: 2px 0 5px;
}

.profile-role {
  align-items: center;
  display: inline-flex;
  font-size: 11px;
  font-weight: 650;
  gap: 4px;
}

.view-details {
  display: grid;
  gap: 9px;
  grid-template-columns: 1fr 1fr;
  margin-top: 20px;
}

.view-detail {
  background: #f8fafc;
  border-radius: 8px;
  padding: 11px;
}

.view-detail span {
  color: #94a3b8;
  display: block;
  font-size: 9px;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.view-detail strong {
  color: #334155;
  display: block;
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Transition */

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translate(
    -50%,
    20px
  );
}

/* Tablet */

@media (max-width: 1250px) {
  .users-grid {
    grid-template-columns: repeat(
      3,
      minmax(0, 1fr)
    );
  }
}

/* Small laptop */

@media (max-width: 950px) {
  .users-grid {
    grid-template-columns: repeat(
      2,
      minmax(0, 1fr)
    );
  }
}

@media (max-width: 1100px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Mobile */

@media (max-width: 650px) {
  .users-page {
    padding: 15px !important;
  }

  .page-header {
    align-items: flex-start;
  }

  .page-title {
    font-size: 23px;
  }

  .header-actions {
    align-self: flex-start;
  }

  .add-user-btn {
    min-height: 36px;
  }

  .summary-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .summary-card {
    min-height: 78px;
    padding: 12px 14px;
  }

  .summary-icon {
    height: 40px;
    width: 40px;
  }

  .summary-value {
    font-size: 21px;
  }

  .toolbar {
    align-items: stretch;
    flex-direction: column;
  }

  .search-wrapper,
  .filter-select {
    width: 100%;
  }

  .users-grid {
    gap: 12px;
    grid-template-columns: 1fr;
  }

  .user-card {
    padding: 12px;
  }

  .view-details {
    grid-template-columns: 1fr;
  }

  .dialog-body {
    max-height: 72vh;
  }
}

/* Dark Mode */

.body--dark .page-title,
.body--dark .user-name,
.body--dark .summary-item strong,
.body--dark .state-title,
.body--dark .dialog-title,
.body--dark .preview-name,
.body--dark .profile-name {
  color: #e5e7eb;
}

.body--dark .page-subtitle,
.body--dark .eyebrow,
.body--dark .summary-label,
.body--dark .user-username,
.body--dark .info-label,
.body--dark .dialog-subtitle,
.body--dark .preview-role,
.body--dark .profile-username,
.body--dark .state-text {
  color: #94a3b8;
}

.body--dark .summary-row,
.body--dark .user-card {
  background: #111827;
  border-color: #263244;
  box-shadow: none;
}

.body--dark .user-card:hover {
  border-color: #3b4a60;
}

.body--dark .summary-card {
  background: #111827;
  border-color: #263244;
  box-shadow: none;
}

.body--dark .summary-card:hover {
  border-color: #3b4a60;
}

.body--dark .summary-label { color: #94a3b8; }
.body--dark .summary-value { color: #e5e7eb; }
.body--dark .summary-caption { color: #718096; }
.body--dark .summary-icon--users { background: rgba(37, 99, 235, 0.12); }
.body--dark .summary-icon--active { background: rgba(16, 185, 129, 0.12); }
.body--dark .summary-icon--admin { background: rgba(124, 58, 237, 0.12); }
.body--dark .summary-icon--manager { background: rgba(234, 88, 12, 0.12); }

.body--dark .summary-divider {
  background: #334155;
}

.body--dark .info-panel {
  background: #182131;
  border-color: #263244;
}

.body--dark .info-row + .info-row {
  border-color: #263244;
}

.body--dark .info-value {
  color: #cbd5e1;
}

.body--dark .contact-row {
  color: #aab4c3;
}

.body--dark .contact-row .q-icon {
  color: #94a3b8;
}

.body--dark .status-active {
  background: rgba(
    16,
    185,
    129,
    0.12
  );
}

.body--dark .status-inactive {
  background: rgba(
    251,
    146,
    60,
    0.12
  );
}

.body--dark .empty-icon {
  background: #182131;
}

.body--dark .error-banner {
  background: rgba(
    244,
    63,
    94,
    0.12
  );
}

.body--dark .user-dialog,
.body--dark .view-dialog {
  background: #111827;
}

.body--dark .account-preview,
.body--dark .view-detail {
  background: #182131;
  border-color: #263244;
}

.body--dark .form-section-title {
  color: #cbd5e1;
}

.body--dark .profile-role {
  color: #93c5fd;
}
</style>
