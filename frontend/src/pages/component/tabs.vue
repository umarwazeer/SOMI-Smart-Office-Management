<template>
  <div class="row q-px-md q-pl-xl text-cyan-10 q-pb-md q-gutter-md" >
 <q-btn push class=" q-py-md" style="width:300px;" rounded>
    <q-icon name="group_add"  size="3rem" class="q-pr-md " />
      <label class=" q-pr-lg text-capitalize" style="align:left">Add New Employee</label>
      <q-icon name="keyboard_arrow_right"/>
    </q-btn>

    <q-btn push to="/LeavePage" class="text-cyan-10" style="width:300px;" rounded>
      <q-icon name="time_to_leave" size="3rem" class="q-gutter-md q-pr-lg q-pt-md" style="align-right:20px" />
      <label class="text-capitalize">Add Leave Request</label>
      <q-icon name="keyboard_arrow_right" style="align-right:20px" />
    </q-btn>

    <q-btn push to="/list_dep" class="text-cyan-10 q-py-md" style="width:300px;" rounded>
      <q-icon name="local_fire_department"  size="3rem" class="q-gutter-md q-pr-lg q-pt-md" />
      <label class="text-capitalize">Add New Department</label>
    </q-btn>

    <q-btn push class="q-py-md text-cyan-10" style="width:300px;" rounded-borders>
      <q-icon name="add" />
      <label class="text-capitalize">Add Request</label>
    </q-btn>

      <q-btn push class="q-mt-lg  q-py-md" style="width:300px;" rounded>
      <q-icon name="add" />
      <label>Add Request</label>
    </q-btn>

      <q-btn push class="q-py-md" style="width:300px;" rounded>
      <q-icon name="add" />
      <label>Add Request</label>
    </q-btn>
  </div>

</template>

<script>
export default {
  data() {
    return {
      loading: false,
      filter: "",
      rowCount: 10,
      columns: [
        {
          name: "desc",
          required: true,
          label: "Type",
          align: "left",
          field: (row) => row.name,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "calories",
          align: "left",
          label: "description",
          field: "calories",
          sortable: true,
        },
        {
          name: "fat",
          label: "Created at",
          align: "left",
          field: "fat",
          sortable: true,
        },
        { name: "carbs", label: "Priority", align: "left", field: "carbs" },
        { name: "protein", label: "Status", align: "left", field: "protein" },
        { name: "sodium", label: "Asigned to", align: "left", field: "sodium" },
        {
          name: "sodium",
          label: "Active User",
          align: "left",
          field: "sodium",
        },
      ],
      rows: [
        {
          id: 10,
          name: "time of request",
          calories: "please fix a printer on second floor",
          fat: "11/23/22 4:09 am",
          carbs: "Heigh",
          protein: "Aproved",
          sodium: "ali liaqat",
        },
        {
          id: 9,
          name: "vacation request",
          calories: " vacation from 23/04/22",
          fat: "12/04/23 3:12 am",
          carbs: "medium",
          protein: "Pending",
          sodium: "hussan joker",
        },
        {
          id: 10,
          name: "time of request",
          calories: "please fix a printer on second floor",
          fat: "11/23/22 4:09 am",
          carbs: "Heigh",
          protein: "Aproved",
          sodium: "ali liaqat",
        },
      ],
      original: [
        {
          name: "Frozen Yogurt",
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          sodium: 87,
          calcium: "14%",
          iron: "1%",
        },
        {
          name: "Ice cream sandwich",
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          sodium: 129,
          calcium: "8%",
          iron: "1%",
        },
        {
          name: "Eclair",
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          sodium: 337,
          calcium: "6%",
          iron: "7%",
        },
        {
          name: "Cupcake",
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          sodium: 413,
          calcium: "3%",
          iron: "8%",
        },
        {
          name: "Gingerbread",
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          sodium: 327,
          calcium: "7%",
          iron: "16%",
        },
        {
          name: "Jelly bean",
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          sodium: 50,
          calcium: "0%",
          iron: "0%",
        },
        {
          name: "Lollipop",
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          sodium: 38,
          calcium: "0%",
          iron: "2%",
        },
        {
          name: "Honeycomb",
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          sodium: 562,
          calcium: "0%",
          iron: "45%",
        },
        {
          name: "Donut",
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          sodium: 326,
          calcium: "2%",
          iron: "22%",
        },
        {
          name: "KitKat",
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          sodium: 54,
          calcium: "12%",
          iron: "6%",
        },
      ],
    };
  },

  methods: {
    // emulate fetching data from server
    addRow() {
      this.loading = true;
      setTimeout(() => {
        const index = Math.floor(Math.random() * (this.data.length + 1)),
          row = this.original[Math.floor(Math.random() * this.original.length)];
        if (this.data.length === 0) {
          this.rowCount = 0;
        }
        row.id = ++this.rowCount;
        const addRow = { ...row }; // extend({}, row, { name: `${row.name} (${row.__count})` })
        this.data = [
          ...this.data.slice(0, index),
          addRow,
          ...this.data.slice(index),
        ];
        this.loading = false;
      }, 500);
    },

    removeRow() {
      this.loading = true;
      setTimeout(() => {
        const index = Math.floor(Math.random() * this.data.length);
        this.data = [
          ...this.data.slice(0, index),
          ...this.data.slice(index + 1),
        ];
        this.loading = false;
      }, 500);
    },
  },
};
</script>
