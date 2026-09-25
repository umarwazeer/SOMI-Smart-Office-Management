<template>
  <div>
    <div class="q-pa-md q-gutter-sm">
      <div class="q-pa-md q-gutter-md">
        <q-item-section class="items-center q-gutter-md">
          <input
            type="file"
            ref="fileInput"
            style="display: none"
            @change="captureImage"
          />
          <q-img
            :src="capturedImage"
            spinner-color="white"
            v-if="capturedImage"
            alt="Captured Image"
            style="height: 170px; width: 240px"
          />
          <q-btn
            push
            color="teal"
            label="Change image"
            @click="openFileInput"
          />
        </q-item-section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      capturedImage: null,
    };
  },
  methods: {
    openFileInput(event) {
      this.$refs.fileInput.click();
      // console.log(this.capturedImage);
      event.preventDefault();

      const formData = new FormData();
      formData.append("image", this.selectedImage);

      axios
        .post("http://127.0.0.1:5000/employee", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // Handle the response from the API
        })
        .catch((error) => {
          // Handle the error
        });
    },
    captureImage(event) {
      console.log(this.capturedImage);
      const file = event.target.files[0];
      const reader = new FileReader();
      console.log(reader);

      reader.onload = () => {
        this.capturedImage = reader.result;
        // console.log(this.capturedImage)
      };

      if (file) {
        reader.readAsDataURL(file);
        console.log(file);
      }
    },
  },
};
</script>
