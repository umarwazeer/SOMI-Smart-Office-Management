<template>
  <q-page class="somi-signup-page">
    <div class="signup-background">
      <div class="background-orb orb-one"></div>
      <div class="background-orb orb-two"></div>
      <div class="background-grid"></div>
    </div>

```
<div class="signup-wrapper">
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
          JOIN SOMI
        </div>

        <h1>
          Build a
          <span>smarter workplace.</span>
        </h1>

        <p>
          Create your SOMI account and bring your office
          operations into one intelligent workspace.
        </p>
      </div>

      <div class="benefit-list">
        <div class="benefit-item">
          <div class="benefit-number">01</div>
          <div>
            <div class="benefit-title">One Connected Workspace</div>
            <div class="benefit-text">
              Keep important office information organized in one place.
            </div>
          </div>
        </div>

        <div class="benefit-item">
          <div class="benefit-number">02</div>
          <div>
            <div class="benefit-title">Simple & Efficient</div>
            <div class="benefit-text">
              Reduce repetitive work and manage everyday operations easily.
            </div>
          </div>
        </div>

        <div class="benefit-item">
          <div class="benefit-number">03</div>
          <div>
            <div class="benefit-title">Ready to Grow</div>
            <div class="benefit-text">
              A flexible platform for modern organizational needs.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="brand-footer">
      © {{ currentYear }} SOMI. Smart office management.
    </div>
  </section>

  <!-- SIGNUP PANEL -->
  <section class="signup-panel">
    <div class="signup-card">

      <!-- MOBILE BRANDING -->
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

      <!-- HEADER -->
      <div class="signup-header">
        <div class="welcome-label">GET STARTED</div>

        <h2>Create your account</h2>

        <p>
          Set up your account to access the SOMI workspace.
        </p>
      </div>

      <!-- FORM -->
      <q-form
        ref="signupForm"
        class="signup-form"
        @submit.prevent="register"
      >
        <!-- USERNAME -->
        <div class="field-wrapper">
          <label class="field-label">Username</label>

          <q-input
            v-model="user.username"
            outlined
            placeholder="Choose a username"
            autocomplete="username"
            :rules="[
              val => !!val || 'Username is required',
              val => val.length >= 3 || 'Username must be at least 3 characters'
            ]"
            class="somi-input"
            hide-bottom-space
          >
            <template #prepend>
              <q-icon name="person_outline" />
            </template>
          </q-input>
        </div>

        <!-- EMAIL -->
        <div class="field-wrapper">
          <label class="field-label">Email address</label>

          <q-input
            v-model="user.email"
            outlined
            type="email"
            placeholder="Enter your email address"
            autocomplete="email"
            :rules="[
              val => !!val || 'Email is required',
              val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Enter a valid email address'
            ]"
            class="somi-input"
            hide-bottom-space
          >
            <template #prepend>
              <q-icon name="mail_outline" />
            </template>
          </q-input>
        </div>

        <!-- PASSWORD -->
        <div class="field-wrapper">
          <label class="field-label">Password</label>

          <q-input
            v-model="user.password"
            outlined
            placeholder="Create a secure password"
            autocomplete="new-password"
            :type="isPwd ? 'password' : 'text'"
            :rules="[
              val => !!val || 'Password is required',
              val => val.length >= 8 || 'Password must be at least 8 characters'
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

        <!-- CONFIRM PASSWORD -->
        <div class="field-wrapper">
          <label class="field-label">Confirm password</label>

          <q-input
            v-model="user.confirmPassword"
            outlined
            placeholder="Re-enter your password"
            autocomplete="new-password"
            :type="isConfirmPwd ? 'password' : 'text'"
            :rules="[
              val => !!val || 'Please confirm your password',
              val => val === user.password || 'Passwords do not match'
            ]"
            class="somi-input"
            hide-bottom-space
          >
            <template #prepend>
              <q-icon name="lock_reset" />
            </template>

            <template #append>
              <q-icon
                :name="isConfirmPwd ? 'visibility_off' : 'visibility'"
                class="password-toggle cursor-pointer"
                @click="isConfirmPwd = !isConfirmPwd"
              />
            </template>
          </q-input>
        </div>

        <!-- TERMS -->
        <div class="terms-section">
          <q-checkbox
            v-model="acceptTerms"
            dense
            color="primary"
            :rules="[
              val => val || 'You must accept the terms'
            ]"
          />

          <span>
            I agree to the
            <button
              type="button"
              class="terms-link"
              @click="showTerms"
            >
              terms and conditions
            </button>
          </span>
        </div>

        <!-- CREATE ACCOUNT -->
        <q-btn
          type="submit"
          label="Create Account"
          icon-right="arrow_forward"
          unelevated
          no-caps
          class="signup-button full-width"
          :loading="loading"
        />

        <!-- LOGIN LINK -->
        <div class="login-section">
          <span>Already have an account?</span>

          <router-link to="/LoginPage">
            Sign in
          </router-link>
        </div>
      </q-form>

      <!-- SECURITY -->
      <div class="security-note">
        <q-icon name="verified_user" size="16px" />
        <span>Your information is protected and secure.</span>
      </div>
    </div>
  </section>
</div>
```

  </q-page>
</template>

<script>
import AuthenticationService from './AuthenticationService'

export default {
  name: 'SignUpPage',

  data () {
    return {
      loading: false,

      user: {
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
      },

      isPwd: true,
      isConfirmPwd: true,
      acceptTerms: false
    }
  },

  computed: {
    currentYear () {
      return new Date().getFullYear()
    }
  },

  methods: {
    async register () {
      const valid = await this.$refs.signupForm.validate()

      if (!valid) {
        return
      }

      if (!this.acceptTerms) {
        this.$q.notify({
          type: 'warning',
          message: 'Please accept the terms and conditions.',
          position: 'top-right'
        })

        return
      }

      this.loading = true

      try {
        const payload = {
          email: this.user.email,
          username: this.user.username,
          password: this.user.password
        }

        const response = await AuthenticationService.register(payload)

        if (response.status === 201 || response.status === 200) {
          this.$q.notify({
            type: 'positive',
            message: 'Account created successfully!',
            position: 'top-right'
          })

          this.$router.push('/LoginPage')
        }
      } catch (error) {
        console.error('Registration error:', error)

        let message = 'Registration failed. Please try again.'

        if (error.response && error.response.data) {
          const data = error.response.data

          if (typeof data === 'string') {
            message = data
          } else if (data.detail) {
            message = data.detail
          } else if (data.username) {
            message = Array.isArray(data.username)
              ? data.username[0]
              : data.username
          } else if (data.email) {
            message = Array.isArray(data.email)
              ? data.email[0]
              : data.email
          }
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

    showTerms () {
      this.$q.dialog({
        title: 'SOMI Terms & Conditions',
        message:
          'By creating a SOMI account, you agree to use the system responsibly and keep your account credentials secure.',
        ok: {
          label: 'Close',
          unelevated: true
        }
      })
    }
  }
}
</script>

<style scoped>
.somi-signup-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: #f5f7fb;
}

.signup-background {
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

.signup-wrapper {
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

.benefit-list {
  margin-top: 55px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.benefit-number {
  min-width: 34px;
  color: #60a5fa;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1px;
  padding-top: 2px;
}

.benefit-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  font-weight: 700;
}

.benefit-text {
  max-width: 390px;
  margin-top: 3px;
  color: rgba(255, 255, 255, 0.48);
  font-size: 11px;
  line-height: 1.5;
}

.brand-footer {
  position: relative;
  z-index: 2;
  color: rgba(255, 255, 255, 0.35);
  font-size: 11px;
}

/* =========================
   SIGNUP PANEL
========================= */

.signup-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 45px 70px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(20px);
}

.signup-card {
  width: 100%;
  max-width: 455px;
}

.signup-header {
  margin-bottom: 28px;
}

.welcome-label {
  margin-bottom: 9px;
  color: #2563eb;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.8px;
}

.signup-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 32px;
  line-height: 1.2;
  font-weight: 750;
  letter-spacing: -1px;
}

.signup-header p {
  margin: 10px 0 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

.signup-form {
  width: 100%;
}

.field-wrapper {
  margin-bottom: 16px;
}

.field-label {
  display: block;
  margin-bottom: 7px;
  color: #334155;
  font-size: 13px;
  font-weight: 650;
}

.somi-input :deep(.q-field__control) {
  min-height: 50px;
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

.terms-section {
  display: flex;
  align-items: flex-start;
  gap: 2px;
  margin: 7px 0 22px;
  color: #64748b;
  font-size: 11px;
  line-height: 1.5;
}

.terms-section :deep(.q-checkbox) {
  margin-top: -5px;
}

.terms-link {
  padding: 0;
  border: 0;
  background: transparent;
  color: #2563eb;
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  font-weight: 650;
}

.terms-link:hover {
  text-decoration: underline;
}

.signup-button {
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

.signup-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.26);
}

.login-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-top: 22px;
  color: #64748b;
  font-size: 13px;
}

.login-section a {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}

.login-section a:hover {
  text-decoration: underline;
}

.security-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 34px;
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
    padding: 45px;
  }

  .signup-panel {
    padding: 40px;
  }

  .brand-message {
    margin-top: 75px;
  }

  .benefit-list {
    margin-top: 40px;
  }
}

@media (max-width: 850px) {
  .signup-wrapper {
    display: block;
    max-width: 600px;
    padding: 25px;
  }

  .brand-panel {
    display: none;
  }

  .signup-panel {
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
    margin-bottom: 38px;
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
  .somi-signup-page {
    background: #f5f7fb;
  }

  .signup-wrapper {
    padding: 12px;
  }

  .signup-panel {
    min-height: calc(100vh - 24px);
    padding: 28px 20px;
    border-radius: 20px;
  }

  .mobile-brand {
    margin-bottom: 32px;
  }

  .signup-header h2 {
    font-size: 28px;
  }

  .signup-header p {
    font-size: 13px;
  }

  .login-section {
    flex-wrap: wrap;
  }

  .security-note {
    margin-top: 28px;
  }
}
</style>
