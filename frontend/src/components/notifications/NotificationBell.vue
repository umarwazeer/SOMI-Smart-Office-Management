<template>
  <div class="notification-bell">
    <q-btn
      flat
      round
      dense
      class="header-action notification-btn"
      icon="notifications_none"
      aria-label="Notifications"
    >
      <q-badge
        v-if="unreadCount > 0"
        color="negative"
        floating
        rounded
        class="notification-badge"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </q-badge>

      <q-menu
        ref="notificationMenu"
        anchor="bottom right"
        self="top right"
        :offset="[0, 10]"
        class="notification-menu"
      >
        <div class="notification-panel">
          <!-- Header -->
          <div class="notification-header">
            <div>
              <div class="notification-title">
                Notifications
              </div>

              <div class="notification-subtitle">
                <span v-if="unreadCount > 0">
                  {{ unreadCount }} unread notification{{ unreadCount > 1 ? 's' : '' }}
                </span>

                <span v-else>
                  You're all caught up
                </span>
              </div>
            </div>

            <q-btn
              v-if="unreadCount > 0"
              flat
              dense
              no-caps
              class="mark-all-btn"
              label="Mark all read"
              :loading="markingAll"
              @click="markAllAsRead"
            />
          </div>

          <q-separator />

          <!-- Loading -->
          <div
            v-if="loading"
            class="notification-loading"
          >
            <q-spinner-dots
              size="28px"
              color="primary"
            />

            <div>Loading notifications...</div>
          </div>

          <!-- Empty -->
          <div
            v-else-if="notifications.length === 0"
            class="notification-empty"
          >
            <q-icon
              name="notifications_none"
              size="42px"
            />

            <div class="empty-title">
              No notifications
            </div>

            <div class="empty-text">
              You don't have any notifications yet.
            </div>
          </div>

          <!-- Notifications -->
          <q-scroll-area
            v-else
            class="notification-scroll"
          >
            <div
              v-for="notification in notifications"
              :key="notification.id"
              class="notification-item"
              :class="{ 'notification-unread': !notification.is_read }"
              @click="handleNotificationClick(notification)"
            >
              <div
                class="notification-icon"
                :class="`notification-icon-${getTypeColor(notification.notification_type)}`"
              >
                <q-icon
                  :name="getTypeIcon(notification.notification_type)"
                  size="19px"
                />
              </div>

              <div class="notification-content">
                <div class="notification-item-top">
                  <div class="notification-item-title">
                    {{ notification.title }}
                  </div>

                  <div
                    v-if="!notification.is_read"
                    class="unread-dot"
                  />
                </div>

                <div class="notification-message">
                  {{ notification.message }}
                </div>

                <div class="notification-time">
                  {{ formatTime(notification.created_at) }}
                </div>
              </div>
            </div>
          </q-scroll-area>

          <!-- Footer -->
          <q-separator />

          <div class="notification-footer">
            <q-btn
              flat
              no-caps
              dense
              icon="refresh"
              label="Refresh"
              :loading="loading"
              @click="loadNotifications"
            />
          </div>
        </div>
      </q-menu>
    </q-btn>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'NotificationBell',

  data() {
    return {
      notifications: [],
      unreadCount: 0,
      loading: false,
      markingAll: false,
      refreshTimer: null
    }
  },

  mounted() {
    this.loadNotifications()

    this.refreshTimer = setInterval(() => {
      this.loadNotifications(true)
    }, 30000)
  },

  beforeUnmount() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
      this.refreshTimer = null
    }
  },

  methods: {
    async loadNotifications(silent = false) {
      if (!silent) {
        this.loading = true
      }

      try {
        const [notificationsResponse, countResponse] = await Promise.all([
          api.get('/notifications/'),
          api.get('/notifications/unread-count/')
        ])

        this.notifications = notificationsResponse.data || []

        this.unreadCount = Number(
          countResponse.data?.unread_count || 0
        )
      } catch (error) {
        console.error(
          'Failed to load notifications:',
          error
        )
      } finally {
        if (!silent) {
          this.loading = false
        }
      }
    },

    async markAsRead(notification) {
      if (notification.is_read) {
        return
      }

      try {
        await api.patch(
          `/notifications/${notification.id}/read/`
        )

        notification.is_read = true

        if (this.unreadCount > 0) {
          this.unreadCount--
        }
      } catch (error) {
        console.error(
          'Failed to mark notification as read:',
          error
        )
      }
    },

    async markAllAsRead() {
      if (this.unreadCount === 0) {
        return
      }

      this.markingAll = true

      try {
        await api.patch(
          '/notifications/mark-all-read/'
        )

        this.notifications.forEach(notification => {
          notification.is_read = true
        })

        this.unreadCount = 0
      } catch (error) {
        console.error(
          'Failed to mark all notifications as read:',
          error
        )
      } finally {
        this.markingAll = false
      }
    },

    async handleNotificationClick(notification) {
      await this.markAsRead(notification)

      const type = notification.notification_type

      if (type === 'LEAVE') {
        const userRole = this.$store.getters.userRole

        if (
          userRole === 'ADMIN' ||
          userRole === 'MANAGER'
        ) {
          this.$router.push('/Approver_leaves')
        } else {
          this.$router.push('/leavePage')
        }
      }

      if (type === 'TASK') {
        this.$router.push('/tasks')
      }

      if (type === 'PERFORMANCE') {
        this.$router.push('/performance')
      }

      if (type === 'PAYROLL') {
        this.$router.push('/payroll_report')
      }

      if (type === 'SYSTEM') {
        // System notifications do not require navigation.
      }

      this.$refs.notificationMenu?.hide()
    },

    getTypeIcon(type) {
      const icons = {
        LEAVE: 'event_busy',
        TASK: 'task_alt',
        PERFORMANCE: 'trending_up',
        PAYROLL: 'payments',
        SYSTEM: 'info'
      }

      return icons[type] || 'notifications'
    },

    getTypeColor(type) {
      const colors = {
        LEAVE: 'orange',
        TASK: 'blue',
        PERFORMANCE: 'purple',
        PAYROLL: 'green',
        SYSTEM: 'grey'
      }

      return colors[type] || 'grey'
    },

    formatTime(dateValue) {
      if (!dateValue) {
        return ''
      }

      const date = new Date(dateValue)

      if (Number.isNaN(date.getTime())) {
        return ''
      }

      const now = new Date()
      const difference = now.getTime() - date.getTime()

      const seconds = Math.floor(difference / 1000)
      const minutes = Math.floor(seconds / 60)
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (seconds < 60) {
        return 'Just now'
      }

      if (minutes < 60) {
        return `${minutes}m ago`
      }

      if (hours < 24) {
        return `${hours}h ago`
      }

      if (days < 7) {
        return `${days}d ago`
      }

      return date.toLocaleDateString([], {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.notification-bell {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.notification-btn {
  position: relative;
}

.notification-badge {
  min-width: 17px;
  height: 17px;
  padding: 0 4px;
  font-size: 9px;
  font-weight: 700;
  line-height: 17px;
}

.notification-panel {
  width: 380px;
  max-width: calc(100vw - 24px);
  overflow: hidden;
  border-radius: 14px;
}

.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 16px 17px 14px;
}

.notification-title {
  font-size: 15px;
  font-weight: 700;
  line-height: 1.2;
}

.notification-subtitle {
  margin-top: 4px;
  font-size: 11px;
  color: #7a8699;
}

.mark-all-btn {
  color: #225dcc;
  font-size: 11px;
  font-weight: 600;
}

.notification-scroll {
  height: 390px;
}

.notification-item {
  display: flex;
  gap: 11px;
  padding: 13px 16px;
  cursor: pointer;
  transition: background 0.18s ease;
}

.notification-item:hover {
  background: rgba(34, 93, 204, 0.05);
}

.notification-unread {
  background: rgba(34, 93, 204, 0.035);
}

.notification-icon {
  flex: 0 0 38px;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.notification-icon-orange {
  color: #d97706;
  background: rgba(245, 158, 11, 0.12);
}

.notification-icon-blue {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.11);
}

.notification-icon-purple {
  color: #7c3aed;
  background: rgba(124, 58, 237, 0.11);
}

.notification-icon-green {
  color: #16a34a;
  background: rgba(22, 163, 74, 0.11);
}

.notification-icon-grey {
  color: #64748b;
  background: rgba(100, 116, 139, 0.12);
}

.notification-content {
  min-width: 0;
  flex: 1;
}

.notification-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.notification-item-title {
  overflow: hidden;
  color: #263449;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-message {
  margin-top: 4px;
  color: #667085;
  font-size: 11px;
  line-height: 1.45;
}

.notification-time {
  margin-top: 5px;
  color: #98a2b3;
  font-size: 9.5px;
}

.unread-dot {
  flex: 0 0 7px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #225dcc;
}

.notification-loading,
.notification-empty {
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 30px 20px;
  text-align: center;
}

.notification-loading {
  gap: 9px;
  color: #7a8699;
  font-size: 11px;
}

.notification-empty {
  color: #98a2b3;
}

.notification-empty .q-icon {
  margin-bottom: 9px;
}

.empty-title {
  color: #475467;
  font-size: 13px;
  font-weight: 700;
}

.empty-text {
  margin-top: 4px;
  font-size: 10.5px;
}

.notification-footer {
  display: flex;
  justify-content: flex-end;
  padding: 8px 12px;
}

.notification-footer .q-btn {
  color: #667085;
  font-size: 10.5px;
}

/* Dark mode */
:global(.body--dark) .notification-item-title {
  color: #e5e7eb;
}

:global(.body--dark) .notification-message {
  color: #aeb7c4;
}

:global(.body--dark) .notification-subtitle,
:global(.body--dark) .notification-time {
  color: #8792a2;
}

:global(.body--dark) .empty-title {
  color: #d1d5db;
}

:global(.body--dark) .notification-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

:global(.body--dark) .notification-unread {
  background: rgba(96, 165, 250, 0.06);
}

/* Mobile */
@media (max-width: 600px) {
  .notification-panel {
    width: calc(100vw - 20px);
  }

  .notification-scroll {
    height: 350px;
  }
}
</style>
