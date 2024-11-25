<template>
  <div class="home">
    <div class="hero is-info is-medium">
      <div class="hero-body has-text-centered">
        <h1 class="title">Bienvenue sur Hridaan and HemLMS</h1>

        <h2 class="subtitle">La sytem du Apprendre le langue enline</h2>
        <h2>
          ici en cette system tu peux apprendre le course Lulu Hridaan Adhikari
        </h2>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"
                ><i class="far fa-clock"></i
              ></span>
              <h2 class="is-size-4 mt-4 mb-4">
                Apprendre la langue enline en vous meme
              </h2>
              <p>Apprendre la langue enline en vous meme</p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"
                ><i class="far fa-comments"></i
              ></span>
              <h2 class="is-size-4 mt-4 mb-4">
                Apprendre la langue dans une discussion
              </h2>
              <p>
                Apprendre la langue dans une discussion avec un autre
                utilisateur
              </p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"
                ><i class="fa fa-home"></i
              ></span>
              <h2 class="is-size-4 mt-4 mb-4">
                Apprendre la langue sur motre maison
              </h2>
              <p>Apprendre la langue sur motre maison, en vous meme</p>
            </div>
          </div>
          <div class="column is-12 has-text-centered">
            <a href="#" class="button is-info is-size-3 mt-6 mb-6"
              >Click to get started</a
            >
          </div>

          <!-- place pour les get-fast-cours -->
          <div
            class="column is-4"
            v-for="course in courses"
            v-bind:key="course.id"
          >
            <!-- plce pour card item -->
            <CourseItemView :course="course" />

            <!-- fin de card item -->
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
  name: "HomeView",
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
      .get("courses/get-front-courses/")
      .then((response) => {
        console.log(response.data);
        this.courses = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>
