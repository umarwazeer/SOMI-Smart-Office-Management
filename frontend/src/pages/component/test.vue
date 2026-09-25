<template>
  <div class="row q-pa-md q-gutter-md">
    <q-card class="col-4">
      <q-form @submit="submitForm" class="q-pa-md q-gutter-md">
        <q-input
          v-model="employee.emp_name"
          dense
          outlined
          label="Name"
        ></q-input>
        <q-input v-model="employee.emp_id" dense outlined label="ID"></q-input>
        <div class="">
          <q-select
            filled
            v-model="model"
            map-options
            :options="options"
            option-label="label"
            option-value="value"
            label="COUNTRY"
            color="primary"
            clearable
            options-selected-class="text-deep-orange"
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <q-img
                    :src="scope.opt.imgSrc"
                    alt="Option Image"
                    style="width: 30px; height: 30px"
                    class="option-image"
                  />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>

        <q-input
          v-model="employee.emp_age"
          dense
          outlined
          label="Age"
          type="number"
        ></q-input>
        <q-select
          class="col-2"
          label="Department"
          :options="options"
          transition-show="flip-up"
          transition-hide="flip-down"
          emit-value
          clearable
          map-options
          option-value="dep_id"
          option-label="name"
          v-model="dep"
          dense
          outlined
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-italic text-grey">
                {No options slot}
              </q-item-section>
            </q-item>
          </template>
          <template v-slot:append>
            <q-btn
              round
              dense
              flat
              color="primary"
              icon="add"
              @click="prompt = true"
              @click.stop
            />
          </template>
          <template
            v-slot:option="{
              itemProps,
              itemEvents,
              opt,
              selected,
              toggleOption,
            }"
          >
            <q-item v-bind="itemProps" v-on="itemEvents">
              <q-item-section>
                <q-item-label v-html="opt.name"></q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn
                  icon="delete"
                  round
                  color="red"
                  dense
                  @click.stop="delDepartment(opt.id)"
                  flat
                />
              </q-item-section>
            </q-item>
            <q-separator style="height: 1px" class="q-mx-xs" color="grey" />
          </template>
        </q-select>
        <q-input
          v-model="employee.emp_email"
          dense
          outlined
          label="Email"
        ></q-input>
        <q-uploader
          label="Upload Image"
          color="primary"
          v-model="imageData"
          accept="image/*"
          @change="onImageUpload"
        >
          <template v-slot:file="{ ref, reset }">
            <q-btn
              ref="pickBtn"
              color="primary"
              label="Select File"
              @click="ref.click()"
            />
            <q-btn color="primary" label="Clear" @click="reset" />
          </template>
        </q-uploader>
        <q-btn label="Submit" type="submit" color="primary"></q-btn>
      </q-form>
    </q-card>
    <div class="col">
      <q-table
        :rows="rows"
        :columns="columns"
        row-key="emp_id"
        :rows-per-page-options="[5, 10, 20]"
        pagination
      >
        <template v-slot:body-cell-thumbnail="props">
          <q-tr :props="props">
            <q-td :props="props">
              <q-avatar
                v-if="col.name == 'Image'"
                size="100px"
                class="shadow-10"
              >
                <img
                  :src="props.row.thumbnail"
                  width="50"
                  height="50"
                  alt="Item Image"
                />
              </q-avatar>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { QTable, QTr, QTd } from "quasar";
import "quasar/dist/quasar.css";

export default {
  data() {
    return {
      employee: {
        emp_name: "",
        emp_id: "",
        emp_age: "",
        emp_email: "",
      },
      model: null,
      // options: [
      //   {
      //     label: "Egypt(ET)",
      //     value: "egypt",
      //     imgSrc: require("src/assets/flags/ad.svg"),
      //   },
      //   {
      //     label: "Greece(GR)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/gr.svg"),
      //   },
      //   {
      //     label: "Afghanistan(Af)",
      //     value: "antarctica",
      //     imgSrc: require("src/assets/flags/af.svg"),
      //   },
      //   {
      //     label: "Australia(AT)",
      //     value: "australia",
      //     imgSrc: require("src/assets/flags/at.svg"),
      //   },
      //   {
      //     label: "American-Samoa(AM)",
      //     value: "australia",
      //     imgSrc: require("src/assets/flags/am.svg"),
      //   },
      //   {
      //     label: "Pakistan(PK)",
      //     value: "pakistan",
      //     imgSrc: require("src/assets/flags/pk.svg"),
      //   },
      //   {
      //     label: "Antarctica(AQ)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/ac.svg"),
      //   },

      //   {
      //     label: "Taiwan(TW)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/tw.svg"),
      //   },
      //   {
      //     label: "India(IN)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/in.svg"),
      //   },
      //   {
      //     label: "Norway(TW)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/no.svg"),
      //   },
      //   {
      //     label: "Cook(CK)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/ck.svg"),
      //   },
      //   {
      //     label: " Argentina(AR)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/ar.svg"),
      //   },
      //   {
      //     label: "Azerbaijan(AZ)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/az.svg"),
      //   },
      //   {
      //     label: "Bulgaria(Bg)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/bv.svg"),
      //   },
      //   {
      //     label: "Cambodia(CD)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/cd.svg"),
      //   },
      //   {
      //     label: "Brazil(BR)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/br.svg"),
      //   },
      //   {
      //     label: "China(Ch)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/ch.svg"),
      //   },
      //   {
      //     label: "Ireland(IR)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/ir.svg"),
      //   },
      //   {
      //     label: "Jordan(JO)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/jo.svg"),
      //   },
      //   {
      //     label: "Bangladesh(BD)",
      //     value: "afghanistan",
      //     imgSrc: require("src/assets/flags/bd.svg"),
      //   },
      // ],
      imageData: null,
      employees: [],
      rows: [
        {
          emp_id: 1,
          emp_age: 22,
          thumbnail: "/quasar-project/src/assets/",
          emp_name: "Thumbnail",
        },
      ],
      columns: [
        {
          name: "emp_name",
          required: true,
          label: "Name",
          align: "left",
          field: "emp_name",
          sortable: true,
        },
        {
          name: "emp_id",
          required: true,
          label: "ID",
          align: "left",
          field: "emp_id",
          sortable: true,
        },
        {
          name: "emp_age",
          required: true,
          label: "Age",
          align: "left",
          field: "emp_age",
          sortable: true,
        },
        {
          name: "emp_email",
          required: true,
          label: "Email",
          align: "left",
          field: "emp_email",
          sortable: true,
        },
        {
          name: "umar khan",
          required: true,
          label: "Employee_Image",
          align: "left",
          field: "thumbnail",
          sortable: true,
        },
      ],
    };
  },
  methods: {
    async submitForm() {
      const formData = new FormData();
      formData.append("emp_name", this.employee.emp_name);
      formData.append("emp_id", this.employee.emp_id);
      formData.append("emp_age", this.employee.emp_age);
      formData.append("emp_email", this.employee.emp_email);
      formData.append("emp_image", this.imageData);
      console.log("formData", this.formData);
      console.log("employee", this.employee);
      try {
        await axios.post(
          "http://127.0.0.1:2222/api/employees",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
          console.log(formData)
        );
        this.getEmployees();
        this.clearForm();
      } catch (error) {
        console.error(error);
      }
    },
    async getEmployees() {
      try {
        const response = await axios.get("http://127.0.0.1:2222/api/employees");
        this.employees = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    clearForm() {
      this.employee.emp_name = "";
      this.employee.emp_id = "";
      this.employee.emp_age = "";
      this.employee.emp_email = "";
      this.imageData = null;
    },
    onImageUpload(files) {
      if (files.length > 0) {
        const file = files[0];
        const reader = new FileReader();
        reader.onloadend = () => {
          this.imageData = reader.result;
        };
        reader.readAsDataURL(file);
      }
    },
  },
  mounted() {
    this.getEmployees();
  },
};
</script>
