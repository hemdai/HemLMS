<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">My Account</h1>
      </div>
    </div>

    <section class="section">
      <div class="columns is-multiline">
        <div class="column is-12">
          <h2 class="subtitle is-size-3">Your Active Courses</h2>
        </div>

        <div
          class="column is-4"
          v-for="course in courses"
          v-bind:key="course.id"
        >
          <!-- plce pour card item -->
          <CourseItemView :course="course" />
        </div>

        <!-- fin de column -->
      </div>
      <button @click="logout()" class="button is-danger">Log Out</button>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import CourseItemView from "../CourseItemView.vue";

export default {
  data() {
    return {
      courses: [],
    };
  },
  components: {
    CourseItemView,
  },
  mounted() {
    axios
      .get("active/get-active-courses/")
      .then((response) => {
        this.courses = response.data.records;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    async logout() {
      console.log("logout");
      await axios.get("logout/").then((response) => {
        console.log(response.data);
      });
      axios.defaults.headers.common["Authorization"] = "";
      this.$store.commit("removeToken");
      this.$store.commit("removeUserName");
      this.$router.push("/");
    },
  },
};
</script>
