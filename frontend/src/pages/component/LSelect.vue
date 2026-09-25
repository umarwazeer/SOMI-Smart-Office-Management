<template>
        <q-select
                class="col-2"
                label="Department"
                transition-show="flip-up"
                transition-hide="flip-down"
                emit-value
                clearable
                map-options
                option-value="dep_id"
                option-label="name"
                v-model="item.dep_id"
                dense
                outlined
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      {No options slot please add Departments}
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:append >
                  <q-btn
                    round
                    dense
                    flat
                    color="primary"
                    icon="add"
                    @click="$emit('prompt')"
                    @click.stop
                  />
                </template>
                <templates
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
                  <q-separator
                    style="height: 1px"
                    class="q-mx-xs"
                    color="grey"
                  />
                </templates>
              </q-select>
<!--
              <q-dialog v-model="prompt" >
              <q-card>
                <div class="col-6-md" style="width: 350px">
                  <h3>this just test dailog...</h3>
                  <addDep/>
                  <add-dep :newDep="this.newDep" @addDep="addDep" @add-department="addDep"  :title="title" />
                </div>
              </q-card>
              </q-dialog> -->
</template>
<script>
// import { ref } from 'vue';
import axios from "axios";
import { Notify } from "quasar";
import { ref } from "vue";
import apiMaker from './department/api'
import AddDep from "./department/addDep.vue"


export default{
    components: {
      AddDep,
    },
    props:{
      prompt: {
      type: Boolean,
      default: false,
    },
    },


    data(){
      return{
        options:[],
        prompt: false,
        item:{
          dep_id:'',
        },
        newDep: {
        id : Math.floor(Math.random() * 1000000 + 1),
        name: "",
      },
      }
    },
    mounted(){
     this.getDep()
    },
    methods:{
      getDep(){
        apiMaker.getDepartment().then((res) => {
           this.options = res.data
           console.log( "res.data", res.data)
           console.log( "this.option", this.options)
           })

      },

      addDep(){ apiMaker.createDepartment(this.newDep).then((response) => {
        if(response.status == 201){
          this.newDep.name = ""
           this.$q.notify({
              type: "positive",
              position: "top",
              message: "your data successfully added",
            });
        }
             this.newDep.id = Math.floor(Math.random() * 1000000 + 1),
             console.log(this.newDep);

          })
          .catch((error) => {
            alert(error);
            console.log(error.data);
          });
    },

    //   get_department() {
    //   axios.get("http://127.0.0.1:2024/department").then((res) => {
    //     this.options = res.data;
    //     console.log("department", this.options);
    //   });
    // },
    // delDepartment(id) {
    //   axios
    //     .delete("http://127.0.0.1:2024/department/" + id)
    //     .then((response) => {
    //       console.log(response.data.name);
    //       this.get_department();
    //       this.$q.notify({
    //         type: "positive",
    //         message: `This is a "positive" type notification.`,
    //       });
    //     })
    //     .catch((error) => {
    //       console.error({ error: error });
    //     });
    //   console.log("delete department.." + id);
    //   alert(id);
    // },
    }
}

</script>
