<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 600px">
      <q-tabs
        v-model="tab"
        inline-label
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
      </q-tabs>
      </div>
      </div>
        <!-- <q-page> -->
    <!-- <q-input v-model="search" debounce="500" label="Search" /> -->
    <!-- <q-table :data="row" :columns="Columns" :filter="filter" /> -->
  <!-- </q-page> -->

 </template>    
<script>
export default {
  data() {
    return {
      search: '',
      rows: [
        { name: 'John', age: 25 },
        { name: 'Jane', age: 30 },
        { name: 'Bob', age: 40 }
      ],
      Columns: [
        { name: 'name', label: 'Name', field: 'name' },
        { name: 'age', label: 'Age', field: 'age' },
        { name: 'age', label: 'email', field: 'age' },
        { name: 'age', label: 'email', field: 'age' },
        { name: 'age', label: 'email', field: 'age' },
        { name: 'age', label: 'email', field: 'age' },
        { name: 'age', label: 'email', field: 'age' },
      ]
    }
  },
  computed: {
    filter() {
      return row => {
        return row.name.toLowerCase().includes(this.search.toLowerCase())
      }
    }
  }
}
</script>
