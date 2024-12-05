<template>
  <form v-on:submit.prevent="submitComment()">
    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <input
          class="input"
          type="text"
          placeholder="Name"
          v-model="comment.name"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Content</label>
      <div class="control">
        <textarea class="textarea" v-model="comment.content"></textarea>
      </div>
    </div>
    <div class="notification is-danger" v-if="errors.length">
      <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
    </div>
    <div class="field">
      <div class="control">
        <button class="button is-link">Submit</button>
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  props: ["course", "activeLesson"],
  name: "AddComments",
  data() {
    return {
      comment: {
        name: "",
        content: "",
      },
      errors: [],
    };
  },
  methods: {
    submitComment() {
      this.errors = [];
      if (!this.comment.name) {
        this.errors.push("Name is required");
      }
      if (!this.comment.content) {
        this.errors.push("Content is required");
      }
      if (!this.errors.length) {
        axios
          .post(
            `/courses/${this.$route.params.slug}/${this.activeLesson.slug}/comments`,
            this.comment
          )
          .then((response) => {
            this.comment.name = "";
            this.comment.content = "";
            this.$emit("submitComment", response.data);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
};
</script>
