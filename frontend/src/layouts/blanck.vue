<template>
<q-layout view="lHh Lpr lFf">
     <q-page-container>
    <router-view /> <!-- Your QPage components go here -->
  </q-page-container>
  </q-layout>

</template>
<script>

import { defineComponent } from "vue";
import { ref } from 'vue'

export default defineComponent({
  name: "App",
  setup () {
    return {
      showing: ref(false)
    }
  }
});
</script>
<style>
.q-toolbar-title{
  margin-left: 30px;
}
.q-toolbar {
    /* position: relative; */
    justify-content: space-around;
    /* padding: 0px 35px;
    width: 100%; */
    /* padding-top: 0px; */

}
.q-gutter-md i{
  display: none;
}
@media (max-width: 600px) {
   .item {
    display: none;
   }
   .q-toolbar i{
    display: block;
   }
}
.q-toolbar i {
  font-size: 21px;
  font-weight: 800px;

}
</style>
