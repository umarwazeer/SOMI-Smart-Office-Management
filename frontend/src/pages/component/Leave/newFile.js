import axios from "axios";

// import addDep from './addDep.vue';
export default (await import('vue')).defineComponent({
components: { leavePage },
// components: { addDep },
data() {
return {
addLeave: false,
filter: "",
selected: [],
columns: [
{
name: "no",
required: true,
label: "S.No",
align: "left",
field: (row) => row.no,
format: (val) => `${val}`,
sortable: true,
},
{
name: "id",
align: "left",
label: "Dep_Id",
field: "id",
sortable: true,
},
{ name: "name", align: "left", label: "Dep_Name", field: "name" },
{
name: "Action",
align: "right",
label: "Action",
field: "Action",
sortable: false,
},
],
rows: [],
};
},
mounted() {
// if (localStorage.getItem("data") !== null) {
//   let users = JSON.parse(localStorage.getItem("data"));
//   this.rows = users;
//   // const newlist = users
//   console.log(users);
// }
this.get_department();
},
methods: {
get_department() {
axios.get("http://127.0.0.1:2024/department").then((res) => {
for (let i = 0; i < res.data.length; i++) {
console.log("i", i);
this.rows = res.data;


}
console.log("innerLoop", i);

// let a = res.data.map((index) => {
//   // let b = 0;
//   let ind =+ index
//   console.log("ind", index.name)
// })
// console.log("hello umakhan", a)
});
},
del(id) {
axios
.delete("http://127.0.0.1:2024/department/" + id)
.then((response) => {
console.log(response.data.name);
alert(id + "record delete  successfully.. ");
this.get_department();
})
.catch((error) => {
console.log(error);
this.$q.notify({
type: "negative",
message: `Something went wrong when trying to verify`,
});
});
},
edit(row_id) {
// this.item = this.rows.row_id.data;
let count = 0;
// for(count = 0; count< 10; count++){
//   let b =+ count +1
//   console.log("count", b)
// }
// axios
//   .put("http://127.0.0.1:2024/department", this.item)
//   .then((response) => {
//       this.$router.push("/list_dep");
//     this.$q.notify({
//       type: "positive",
//       message: "your data successfully added",
//     });
//     console.log(this.item);
//   })
//   .catch((error) => {
//     alert(error);
//     console.log(error.data);
//   });
},
},
});
