<template>
<div class="row q-pa-md">
 <div class="col-12 col-md-8 q-pa-md">
            <q-card-section class="">
              <div
                class="
                  text-h4
                  text-center
                  text-italic
                  text-weight-bolder
                  text-secondary
                "
              >
                Logout
              </div>
            </q-card-section>
            <q-card-section class="q-pt-md q-mb-md">
              <q-input
                dense
                type="text"
                class="q-pa-md"
                v-model="list.userName"
                label="User Name"
              />
              <q-input
                dense
                type="password"
                class="q-pa-md"
                v-model="list.password"
                label="Password"
              />
            </q-card-section>

            <q-card-actions class="q-pa-md text-white">
              <q-btn
                flat
                label="submit"
                to="/"
                @click="logout"
                rounded
                class="window-width bg-secondary"
                v-close-popup
              />
              <div class="text-black q-pa-sm">create your account ?</div>
              <q-btn class="text-primary" flat>Sign In</q-btn>
            </q-card-actions>
          </div>
</div>
   
</template>
<script>
import { } from 'vue'

export default {
}
</script>
