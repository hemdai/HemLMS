<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">
          {{ account.first_name + " " + account.last_name }}
        </h1>
      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <!-- init de column -->
          <div
            class="column is-4"
            v-for="course in courses"
            v-bind:key="course.id"
          >
            <!-- plce pour card item -->
            <CourseItemView :course="course" />
          </div>
          <!-- fin de column -->
          <div class="column is-12">
            <nav class="pagination">
              <a class="pagination-previous">Previous</a>
              <a class="pagination-next">Next page</a>
            </nav>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import CourseItemView from "./CourseItemView.vue";
export default {
  data() {
    return {
      courses: [],
      account: {},
    };
  },
  components: {
    CourseItemView,
  },
  async mounted() {
    document.title = "Courses - LMS";
    await axios
      .get("categories/")
      .then((response) => {
        this.categories = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
    this.getCourses();
  },
  methods: {
    getCourses() {
      axios
        .get(`authors/courses/${this.$route.params.id}/`)
        .then((response) => {
          this.courses = response.data.courses_data;
          this.account = response.data.account;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
