<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Create Course</h1>
      </div>
    </div>

    <section class="section">
      <div class="mb-6 px-6 py-4 has-background-black">
        <h2 class="subtitle">Meta Information</h2>
        <div class="field">
          <label class="label">Title</label>
          <input type="text" class="input" v-model="form.title" />
        </div>
        <div class="field">
          <label class="label">Short Description</label>
          <textarea
            class="textarea"
            v-model="form.short_description"
          ></textarea>
        </div>

        <div class="field">
          <label class="label">Long Description</label>
          <textarea class="textarea" v-model="form.long_description"></textarea>
        </div>

        <div>
          <label class="label">Course Picture Upload</label>
            <UploadDocument documentType="courseImage" @fileUploaded="onFileUploaded"></UploadDocument>
            <hr>
        </div>

        <div class="field">
          <div class="select is-multiple">
            <select multiple size="10" v-model="form.categories">
              <option
                v-for="category in categories"
                v-bind:value="category.id"
                v-bind:key="category.id"
              >
                {{ category.title }}
              </option>
            </select>
          </div>
        </div>

        <div class="mb-6 px-6 py-4 has-background-black">
          <h2 class="subtitle">Lessons</h2>
          <div
            v-for="(lesson, index) in form.lessons"
            v-bind:key="index"
            class="mb-6"
          >
            <h3 class="subtitle is-size-6">Lesson</h3>
            <div class="field">
              <label>Title</label>
              <input
                type="text"
                class="input"
                v-model="lesson.title"
                :name="`form.lessons[${index}][title]`"
              />
            </div>
            <div class="field">
              <label class="label">Video URL</label>
              <input
                type="text"
                class="input"
                v-model="lesson.video_url"
                :name="`form.lessons[${index}][video_url]`"
              ></input>
            </div>

            <div class="field">
              <label class="label">Shrort Description</label>
              <textarea
                class="textarea"
                v-model="lesson.short_description"
                :name="`form.lessons[${index}][short_description]`"
              ></textarea>
            </div>

            <div class="field">
              <label class="label">long Description</label>
              <textarea
                class="textarea"
                v-model="lesson.long_description"
                :name="`form.lessons[${index}][long_description]`"
              ></textarea>
            </div>
          </div>
          <hr />

          <button class="button is-info" @click="addLesson()">
            Add Lesson
          </button>
        </div>

        <div class="field buttons">
          <button class="button is-success" @click="submitForm('draft')">
            Save as Draft
          </button>
          <button class="button is-info" @click="submitForm('in_review')">
            Submit for review
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import UploadDocument from "@/components/UploadDocument.vue";
import axios from "axios";
export default {
  components: { UploadDocument },
  data() {
    return {
      form: {
        title: "",
        short_description: "",
        long_description: "",
        status: "",
        lessons: [],
        image_path: "",
        image_uuid: "",
      },
      categories: [],
    };
  },
  mounted() {
    this.getCategories();
  },
  methods: {
    onFileUploaded(uploadObject) {
      this.form.image_path = uploadObject.path
      this.form.image_uuid = uploadObject.id
    },
    getCategories() {
      axios
        .get("categories/")
        .then((response) => {
          console.log(response.data, "the categories");
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitForm(status) {
      this.form.status = status;
      console.log(this.form);
      axios
        .post("create/courses", this.form)
        .then((response) => {
          this.$router.push("/dashboard/my-courses");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addLesson() {
      this.form.lessons.push({
        title: "",
        short_description: "",
        long_description: "",
        video_url: "",
      });
    },
  },
};
</script>
