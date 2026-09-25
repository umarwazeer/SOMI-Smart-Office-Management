<template>
  <q-card class="department-dialog-card">
    <q-card-section class="dialog-header">
      <div class="row items-center justify-between">
        <div>
          <div class="text-h6 text-weight-bold">
            {{ isEditing ? 'Edit Department' : 'Add Department' }}
          </div>

          <div class="text-caption text-grey-6 q-mt-xs">
            {{
              isEditing
                ? 'Update department information'
                : 'Create a new department'
            }}
          </div>
        </div>

        <q-btn
          flat
          round
          dense
          icon="close"
          color="grey-7"
          :disable="loading"
          @click="onCancel"
        />
      </div>
    </q-card-section>

    <q-separator />

    <q-form
      ref="departmentForm"
      @submit.prevent="onSubmit"
    >
      <q-card-section class="q-gutter-md">
        <q-input
          v-model="newDep.name"
          outlined
          label="Department Name *"
          placeholder="e.g. Human Resources"
          :rules="[
            val => !!val?.trim() || 'Department name is required'
          ]"
          :disable="loading"
        >
          <template v-slot:prepend>
            <q-icon name="business" />
          </template>
        </q-input>

        <q-input
          v-model="newDep.code"
          outlined
          label="Department Code *"
          placeholder="e.g. HR"
          maxlength="20"
          :rules="[
            val => !!val?.trim() || 'Department code is required'
          ]"
          :disable="loading"
        >
          <template v-slot:prepend>
            <q-icon name="tag" />
          </template>
        </q-input>

        <q-input
          v-model="newDep.description"
          outlined
          type="textarea"
          label="Description"
          placeholder="Brief description of this department"
          autogrow
          maxlength="500"
          counter
          :disable="loading"
        >
          <template v-slot:prepend>
            <q-icon name="description" />
          </template>
        </q-input>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          flat
          label="Cancel"
          color="grey-7"
          no-caps
          :disable="loading"
          @click="onCancel"
        />

        <q-btn
          unelevated
          :label="isEditing ? 'Save Changes' : 'Create Department'"
          color="primary"
          no-caps
          type="submit"
          :loading="loading"
        />
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
export default {
  name: 'addDep',

  props: {
    newDep: {
      type: Object,
      required: true
    },

    isEditing: {
      type: Boolean,
      default: false
    },

    loading: {
      type: Boolean,
      default: false
    }
  },

  emits: ['addDep', 'cancel'],

  methods: {
    async onSubmit () {
      const valid = await this.$refs.departmentForm.validate()

      if (!valid) {
        return
      }

      this.$emit('addDep')
    },

    onCancel () {
      if (this.loading) {
        return
      }

      this.$emit('cancel')
    }
  }
}
</script>

<style scoped>
.department-dialog-card {
  width: 520px;
  max-width: 95vw;
  border-radius: 16px;
  overflow: hidden;
}

.dialog-header {
  padding: 22px 24px;
}

@media (max-width: 600px) {
  .department-dialog-card {
    width: 100%;
    border-radius: 12px;
  }

  .dialog-header {
    padding: 18px;
  }
}
</style>
