<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">The Title of the Course</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns content">
          <div class="column is -2">
            <h2>Table Content</h2>
            <ul>
              <li v-for="lesson in lessons" v-bind:key="lesson.id">
                <a @click="setActiveLesson(lesson)">{{ lesson.title }}</a>
              </li>
            </ul>
          </div>

          <div class="column is-10">
            <template v-if="$store.state.user.isAuthenticated">
              <template v-if="activeLesson">
                {{ activeLesson.long_description }}
                <hr>

                <article 
                  class="media box"
                  v-for="comment in comments"
                  v-bind:key="comment.id"
                  >
                  <div class="media-content">
                    <div class="content">
                      <p>
                        <strong>{{ comment.name }}</strong> - {{ comment.created_at }}
                        <br>
                        {{ comment.content }}
                      </p>
                    </div>
                    </div>

                </article>

                <form v-on:submit.prevent="submitComment()">
                  <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                      <input class="input" type="text" placeholder="Name" v-model="comment.name">
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
              </template v-else>
              {{ course_detail.long_description }}
            </template>
            <template v-else>
              <h2>Not Authenticated</h2>
              <p>
                You are not authenticated. Please log in to view this content.
              </p>
            </template>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      course_detail: {},
      lessons: [],
      comments: [],
      activeLesson: null,
      errors : [],
      comment: {
        name: "",
        content: "",
      }
    };
  },
  mounted() {
    const slug = this.$route.params.slug;
    axios
      .get(`courses/${slug}`)
      .then((response) => {
        console.log(response.data);
        this.course_detail = response.data.course_detail;
        this.lessons = response.data.lessons;
      })
      .catch((error) => {
        console.log(error);
      });
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
              .post(`/courses/${this.course_detail.slug}/${this.activeLesson.slug}/comments`, this.comment)
              .then((response) => {
                this.comment.name = "";
                this.comment.content = "";
                this.comments.push(response.data);
              })
              .catch((error) => {
                console.log(error);
              });
      }
    },
     setActiveLesson(lesson) {
    this.activeLesson = lesson;
    this.getComments();
    },
  getComments() {
    axios
      .get(`/courses/${this.course_detail.slug}/${this.activeLesson.slug}/comments`)
      .then((response) => {
        console.log("the comments",response.data);
        this.comments = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }
  },
};
</script>
