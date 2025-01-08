<template>
  <div>
    <input type="file" @change="onFileChange" />
    <button type="button" class="button is-info is-rounded" @click="uploadFile">
      Upload
    </button>
    <div v-if="uploadedFileUrl">
      <p>Uploaded File:</p>
      <img
        v-if="isImage(uploadedFileUrl)"
        :src="$config.STATIC_PATH + uploadedFileUrl"
        alt="Uploaded File"
      />
      <a v-else :href="$config.STATIC_PATH + uploadedFileUrl" target="_blank"
        >Download File</a
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    documentType: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      selectedFile: null,
      uploadedFileUrl: null, // URL for the uploaded file
      url: {
        courseImage: "/course/images",
        coursePdf: "/courses/upload-course-pdf",
      },
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    getUrl(uuid) {
      return this.url[this.documentType] + "/" + uuid;
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file");
        return;
      }
      const uuid = crypto.randomUUID();
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      try {
        const response = await axios.post(this.getUrl(uuid), formData);
        this.uploadedFileUrl = response.data.url; // Save the returned URL
        console.log("File uploaded successfully:", response.data.url);

        this.$emit("fileUploaded", { id: uuid, path: this.uploadedFileUrl });
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    },
    isImage(url) {
      const imageExtensions = [".jpg", ".jpeg", ".png", ".gif"];
      return imageExtensions.some((ext) => url.toLowerCase().endsWith(ext));
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
