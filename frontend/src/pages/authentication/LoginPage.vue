<template>
  <q-page class="somi-login-page">
    <div class="login-background">
      <div class="background-orb orb-one"></div>
      <div class="background-orb orb-two"></div>
      <div class="background-grid"></div>
    </div>

    <div class="login-wrapper">
      <!-- LEFT BRANDING PANEL -->
      <section class="brand-panel">
        <div class="brand-content">
          <div class="brand-logo">
            <div class="logo-mark">
              <q-icon name="hub" size="34px" />
            </div>

            <div>
              <div class="brand-name">SOMI</div>
              <div class="brand-subtitle">
                Smart Office Management & Intelligence
              </div>
            </div>
          </div>

          <div class="brand-message">
            <div class="eyebrow">
              <span class="eyebrow-line"></span>
              SMARTER WORKSPACE
            </div>

            <h1>
              Manage your office.
              <span>Smarter.</span>
            </h1>

            <p>
              A modern workspace platform designed to simplify
              employees, departments, attendance and everyday
              office operations.
            </p>
          </div>

          <div class="feature-list">
            <div class="feature-item">
              <div class="feature-icon">
                <q-icon name="groups" />
              </div>

              <div>
                <div class="feature-title">Workforce Management</div>
                <div class="feature-text">
                  Manage employees and organizational information.
                </div>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <q-icon name="insights" />
              </div>

              <div>
                <div class="feature-title">Smart Insights</div>
                <div class="feature-text">
                  Turn office data into useful information.
                </div>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <q-icon name="security" />
              </div>

              <div>
                <div class="feature-title">Secure Access</div>
                <div class="feature-text">
                  Role-based access for your organization.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="brand-footer">
          © {{ currentYear }} SOMI. Smart office management.
        </div>
      </section>

      <!-- LOGIN PANEL -->
      <section class="login-panel">
        <div class="login-card">
          <!-- Mobile branding -->
          <div class="mobile-brand">
            <div class="mobile-logo">
              <q-icon name="hub" size="28px" />
            </div>

            <div>
              <div class="mobile-brand-name">SOMI</div>
              <div class="mobile-brand-subtitle">
                Smart Office Management
              </div>
            </div>
          </div>

          <div class="login-header">
            <div class="welcome-label">WELCOME BACK</div>

            <h2>Sign in to SOMI</h2>

            <p>
              Enter your credentials to access your workspace.
            </p>
          </div>

          <q-form
            ref="loginForm"
            class="login-form"
            @submit.prevent="submitLogin"
          >
            <!-- USERNAME -->
            <div class="field-wrapper">
              <label class="field-label">Username</label>

              <q-input
                v-model="credentials.username"
                outlined
                placeholder="Enter your username"
                autocomplete="username"
                :rules="[
                  val => !!val || 'Username is required'
                ]"
                class="somi-input"
                hide-bottom-space
              >
                <template #prepend>
                  <q-icon name="person_outline" />
                </template>
              </q-input>
            </div>

            <!-- PASSWORD -->
            <div class="field-wrapper">
              <label class="field-label">Password</label>

              <q-input
                v-model="credentials.password"
                outlined
                placeholder="Enter your password"
                autocomplete="current-password"
                :type="isPwd ? 'password' : 'text'"
                :rules="[
                  val => !!val || 'Password is required'
                ]"
                class="somi-input"
                hide-bottom-space
              >
                <template #prepend>
                  <q-icon name="lock_outline" />
                </template>

                <template #append>
                  <q-icon
                    :name="isPwd ? 'visibility_off' : 'visibility'"
                    class="password-toggle cursor-pointer"
                    @click="isPwd = !isPwd"
                  />
                </template>
              </q-input>
            </div>

            <!-- OPTIONS -->
            <div class="login-options">
              <q-checkbox
                v-model="credentials.remember"
                label="Remember me"
                dense
                color="primary"
              />

              <button
                type="button"
                class="forgot-password"
                @click="forgotPassword"
              >
                Forgot password?
              </button>
            </div>

            <!-- LOGIN BUTTON -->
            <q-btn
              type="submit"
              label="Sign In"
              icon-right="arrow_forward"
              unelevated
              no-caps
              class="login-button full-width"
              :loading="loading"
            />

            <!-- REGISTER -->
            <div class="register-section">
              <span>Don't have an account?</span>

              <router-link to="/SignUp">
                Create account
              </router-link>
            </div>
          </q-form>

          <div class="security-note">
            <q-icon name="verified_user" size="16px" />
            <span>Your connection is protected and secure.</span>
          </div>
        </div>
      </section>
    </div>
  </q-page>
</template>

<script>
import AuthenticationService from './AuthenticationService'

export default {
  name: 'LoginPage',

  data () {
    return {
      loading: false,

      credentials: {
        username: '',
        password: '',
        remember: false
      },

      isPwd: true
    }
  },

  computed: {
    currentYear () {
      return new Date().getFullYear()
    }
  },

  methods: {
    async submitLogin () {
      this.loading = true

      try {
        const response = await AuthenticationService.login({
          username: this.credentials.username,
          password: this.credentials.password
        })

        const accessToken = response.data?.access
        const refreshToken = response.data?.refresh

        if (!accessToken || !refreshToken) {
          throw new Error('Authentication tokens were not returned by the server.')
        }

        AuthenticationService.setToken(accessToken)
        AuthenticationService.setRefreshToken(refreshToken)

        this.$q.notify({
          type: 'positive',
          message: 'Login successful!',
          position: 'top-right'
        })

        this.$router.push('/emp-dashboard')
      } catch (error) {
        console.error('Login error:', error)

        let message = 'Invalid username or password.'

        if (error.response) {
          if (error.response.status === 400) {
            message = 'Please check your username and password.'
          } else if (error.response.status === 401) {
            message = 'Invalid username or password.'
          } else if (error.response.status >= 500) {
            message = 'Server error. Please try again later.'
          }
        } else if (error.message) {
          message = error.message
        }

        this.$q.notify({
          type: 'negative',
          message,
          position: 'top-right'
        })
      } finally {
        this.loading = false
      }
    },

    forgotPassword () {
      this.$q.notify({
        type: 'info',
        message: 'Password recovery will be available soon.',
        position: 'top-right'
      })
    }
  }
}
</script>

<style scoped>
.somi-login-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: #f5f7fb;
}

.login-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.background-grid {
  position: absolute;
  inset: 0;
  opacity: 0.035;
  background-image:
    linear-gradient(rgba(15, 23, 42, 1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(15, 23, 42, 1) 1px, transparent 1px);
  background-size: 45px 45px;
}

.background-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
}

.orb-one {
  width: 420px;
  height: 420px;
  background: rgba(37, 99, 235, 0.08);
  top: -180px;
  right: -100px;
}

.orb-two {
  width: 360px;
  height: 360px;
  background: rgba(14, 165, 233, 0.07);
  bottom: -180px;
  left: -100px;
}

.login-wrapper {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(420px, 1fr) minmax(440px, 0.85fr);
  max-width: 1500px;
  margin: 0 auto;
}

/* =========================
   BRAND PANEL
========================= */

.brand-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 58px 70px;
  color: white;
  overflow: hidden;
  background:
    radial-gradient(
      circle at 85% 15%,
      rgba(59, 130, 246, 0.35),
      transparent 32%
    ),
    linear-gradient(
      145deg,
      #0b1220 0%,
      #101c35 52%,
      #12345c 100%
    );
}

.brand-panel::after {
  content: '';
  position: absolute;
  width: 520px;
  height: 520px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 50%;
  right: -260px;
  bottom: -240px;
}

.brand-content {
  position: relative;
  z-index: 2;
  max-width: 610px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-mark {
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.3);
}

.brand-name {
  font-size: 27px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: 2px;
}

.brand-subtitle {
  margin-top: 5px;
  color: rgba(255, 255, 255, 0.62);
  font-size: 11px;
  letter-spacing: 0.4px;
}

.brand-message {
  margin-top: 105px;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #60a5fa;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
}

.eyebrow-line {
  width: 28px;
  height: 2px;
  border-radius: 2px;
  background: #3b82f6;
}

.brand-message h1 {
  max-width: 570px;
  margin: 18px 0 22px;
  font-size: clamp(40px, 4vw, 60px);
  line-height: 1.08;
  letter-spacing: -2px;
  font-weight: 750;
}

.brand-message h1 span {
  display: block;
  color: #60a5fa;
}

.brand-message p {
  max-width: 520px;
  margin: 0;
  color: rgba(255, 255, 255, 0.65);
  font-size: 15px;
  line-height: 1.8;
}

.feature-list {
  margin-top: 55px;
  display: flex;
  flex-direction: column;
  gap: 19px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 14px;
}

.feature-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #60a5fa;
  background: rgba(59, 130, 246, 0.12);
  border: 1px solid rgba(96, 165, 250, 0.12);
}

.feature-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  font-weight: 700;
}

.feature-text {
  margin-top: 2px;
  color: rgba(255, 255, 255, 0.48);
  font-size: 11px;
}

.brand-footer {
  position: relative;
  z-index: 2;
  color: rgba(255, 255, 255, 0.35);
  font-size: 11px;
}

/* =========================
   LOGIN PANEL
========================= */

.login-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px 70px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(20px);
}

.login-card {
  width: 100%;
  max-width: 455px;
}

.login-header {
  margin-bottom: 32px;
}

.welcome-label {
  margin-bottom: 9px;
  color: #2563eb;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.8px;
}

.login-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 34px;
  line-height: 1.2;
  font-weight: 750;
  letter-spacing: -1px;
}

.login-header p {
  margin: 10px 0 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

.login-form {
  width: 100%;
}

.field-wrapper {
  margin-bottom: 19px;
}

.field-label {
  display: block;
  margin-bottom: 8px;
  color: #334155;
  font-size: 13px;
  font-weight: 650;
}

.somi-input :deep(.q-field__control) {
  min-height: 52px;
  border-radius: 12px;
  background: #ffffff;
}

.somi-input :deep(.q-field__control:before) {
  border-color: #e2e8f0;
}

.somi-input :deep(.q-field__control:hover:before) {
  border-color: #94a3b8;
}

.somi-input :deep(.q-field__control:after) {
  border-color: #2563eb;
}

.somi-input :deep(.q-field__prepend) {
  color: #94a3b8;
}

.somi-input :deep(input) {
  color: #0f172a;
  font-size: 14px;
}

.somi-input :deep(input::placeholder) {
  color: #a0aec0;
}

.password-toggle {
  color: #94a3b8;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #2563eb;
}

.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 7px 0 25px;
}

.login-options :deep(.q-checkbox__label) {
  color: #64748b;
  font-size: 12px;
}

.forgot-password {
  padding: 0;
  border: 0;
  background: transparent;
  color: #2563eb;
  cursor: pointer;
  font-family: inherit;
  font-size: 12px;
  font-weight: 650;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  min-height: 52px;
  border-radius: 12px;
  color: white;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.2);
  font-size: 14px;
  font-weight: 700;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.26);
}

.register-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-top: 24px;
  color: #64748b;
  font-size: 13px;
}

.register-section a {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}

.register-section a:hover {
  text-decoration: underline;
}

.security-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 42px;
  color: #94a3b8;
  font-size: 11px;
}

.security-note .q-icon {
  color: #22c55e;
}

.mobile-brand {
  display: none;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 1050px) {
  .brand-panel {
    padding: 45px 45px;
  }

  .login-panel {
    padding: 40px;
  }

  .brand-message {
    margin-top: 75px;
  }

  .feature-list {
    margin-top: 40px;
  }
}

@media (max-width: 850px) {
  .login-wrapper {
    display: block;
    max-width: 600px;
    padding: 25px;
  }

  .brand-panel {
    display: none;
  }

  .login-panel {
    min-height: calc(100vh - 50px);
    padding: 40px 30px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.94);
    box-shadow: 0 25px 70px rgba(15, 23, 42, 0.08);
  }

  .mobile-brand {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 11px;
    margin-bottom: 50px;
  }

  .mobile-logo {
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    color: white;
    background: linear-gradient(135deg, #2563eb, #38bdf8);
  }

  .mobile-brand-name {
    color: #0f172a;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 1.5px;
  }

  .mobile-brand-subtitle {
    margin-top: 2px;
    color: #64748b;
    font-size: 9px;
  }
}

@media (max-width: 500px) {
  .somi-login-page {
    background: #f5f7fb;
  }

  .login-wrapper {
    padding: 12px;
  }

  .login-panel {
    min-height: calc(100vh - 24px);
    padding: 30px 20px;
    border-radius: 20px;
  }

  .mobile-brand {
    margin-bottom: 38px;
  }

  .login-header h2 {
    font-size: 29px;
  }

  .login-header p {
    font-size: 13px;
  }

  .login-options {
    align-items: flex-start;
  }

  .register-section {
    flex-wrap: wrap;
  }

  .security-note {
    margin-top: 32px;
  }
}
</style>
