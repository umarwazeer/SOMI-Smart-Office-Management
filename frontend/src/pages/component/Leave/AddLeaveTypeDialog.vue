<template>
  <q-dialog
    v-model="dialogVisible"
    persistent
  >
    <q-card class="leave-type-dialog">
      <!-- Header -->
      <q-card-section class="dialog-header">
        <div class="row items-center no-wrap">
          <div class="dialog-icon">
            <q-icon name="category" size="23px" />
          </div>

          <div class="q-ml-md">
            <div class="text-h6 text-weight-bold text-grey-9">
              Add Leave Type
            </div>

            <div class="text-caption text-grey-6 q-mt-xs">
              Create a leave category for your organization.
            </div>
          </div>

          <q-space />

          <q-btn
            flat
            round
            dense
            icon="close"
            color="grey-7"
            :disable="saving"
            @click="closeDialog"
          />
        </div>
      </q-card-section>

      <q-separator />

      <!-- Form -->
      <q-card-section class="q-pa-md q-pa-lg-lg">
        <div class="row q-col-gutter-md">
          <!-- Name -->
          <div class="col-12">
            <q-input
              ref="nameInput"
              v-model.trim="form.name"
              outlined
              dense
              autofocus
              label="Leave Type Name"
              placeholder="e.g. Casual Leave"
              maxlength="100"
              :rules="[requiredRule]"
              :disable="saving"
              @keyup.enter="submit"
            >
              <template v-slot:prepend>
                <q-icon
                  name="label_outline"
                  color="primary"
                />
              </template>
            </q-input>
          </div>

          <!-- Default Days -->
          <div class="col-12 col-sm-6">
            <q-input
              v-model.number="form.default_days"
              type="number"
              outlined
              dense
              label="Default Days"
              hint="Optional annual allowance"
              min="0"
              :disable="saving"
            >
              <template v-slot:prepend>
                <q-icon
                  name="event_note"
                  color="primary"
                />
              </template>
            </q-input>
          </div>

          <!-- Active -->
          <div class="col-12 col-sm-6">
            <div class="active-option">
              <q-toggle
                v-model="form.is_active"
                color="primary"
                label="Active"
                :disable="saving"
              />

              <div class="text-caption text-grey-6 q-ml-sm">
                Available for new leave requests
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="col-12">
            <q-input
              v-model.trim="form.description"
              type="textarea"
              outlined
              autogrow
              rows="3"
              label="Description"
              placeholder="Optional description for this leave type..."
              maxlength="500"
              counter
              :disable="saving"
            >
              <template v-slot:prepend>
                <q-icon
                  name="notes"
                  color="primary"
                />
              </template>
            </q-input>
          </div>
        </div>

        <!-- Error -->
        <q-banner
          v-if="errorMessage"
          rounded
          class="bg-red-1 text-negative q-mt-md"
        >
          <template v-slot:avatar>
            <q-icon name="error_outline" />
          </template>

          {{ errorMessage }}

          <template v-slot:action>
            <q-btn
              flat
              dense
              label="Dismiss"
              color="negative"
              @click="errorMessage = ''"
            />
          </template>
        </q-banner>
      </q-card-section>

      <q-separator />

      <!-- Actions -->
      <q-card-actions
        align="right"
        class="q-pa-md"
      >
        <q-btn
          flat
          no-caps
          label="Cancel"
          color="grey-7"
          :disable="saving"
          @click="closeDialog"
        />

        <q-btn
          unelevated
          no-caps
          label="Add Leave Type"
          icon="add"
          color="primary"
          :loading="saving"
          @click="submit"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'AddLeaveTypeDialog',

  emits: [
    'add-leave-type'
  ],

  data () {
    return {
      dialogVisible: false,
      saving: false,
      errorMessage: '',

      form: {
        name: '',
        description: '',
        default_days: 0,
        is_active: true
      }
    }
  },

  methods: {
    openDialog () {
      this.resetForm()
      this.dialogVisible = true

      this.$nextTick(() => {
        this.$refs.nameInput?.focus()
      })
    },

    closeDialog () {
      if (this.saving) {
        return
      }

      this.dialogVisible = false
      this.resetForm()
    },

    resetForm () {
      this.form = {
        name: '',
        description: '',
        default_days: 0,
        is_active: true
      }

      this.errorMessage = ''
    },

    requiredRule (value) {
      return (
        Boolean(value?.trim()) ||
        'Leave type name is required.'
      )
    },

    validateForm () {
      const name = this.form.name?.trim()

      if (!name) {
        this.errorMessage =
          'Please enter a leave type name.'

        this.$q.notify({
          type: 'warning',
          message:
            'Please enter a leave type name.'
        })

        return false
      }

      const defaultDays =
        Number(this.form.default_days)

      if (
        !Number.isFinite(defaultDays) ||
        defaultDays < 0
      ) {
        this.errorMessage =
          'Default days must be zero or greater.'

        this.$q.notify({
          type: 'warning',
          message:
            'Default days must be zero or greater.'
        })

        return false
      }

      this.form.default_days =
        Math.floor(defaultDays)

      return true
    },

    async submit () {
      this.errorMessage = ''

      if (!this.validateForm()) {
        return
      }

      this.saving = true

      try {
        /*
         * The parent Leave page is responsible for
         * communicating with the Django API.
         *
         * This keeps the dialog reusable and prevents
         * duplicate API logic.
         */
        this.$emit(
          'add-leave-type',
          {
            name: this.form.name.trim(),
            description:
              this.form.description?.trim() || '',
            default_days:
              this.form.default_days,
            is_active:
              this.form.is_active
          }
        )

        this.dialogVisible = false
        this.resetForm()
      } catch (error) {
        console.error(
          'Failed to add leave type:',
          error
        )

        this.errorMessage =
          'Unable to add leave type.'

        this.$q.notify({
          type: 'negative',
          message:
            'Unable to add leave type.'
        })
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.leave-type-dialog {
  width: 100%;
  max-width: 520px;
  border-radius: 16px;
  overflow: hidden;
}

.dialog-header {
  padding: 18px 20px;
  background: #ffffff;
}

.dialog-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
}

.active-option {
  min-height: 40px;
  display: flex;
  align-items: center;
  padding-top: 2px;
}

@media (max-width: 599px) {
  .leave-type-dialog {
    width: calc(100vw - 24px);
    border-radius: 14px;
  }

  .dialog-header {
    padding: 16px;
  }
}
</style>
