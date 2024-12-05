<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Courses</h1>
      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-2">
            <aside class="menu">
              <p class="menu-label">Categories</p>

              <ul class="menu-list">
                <li
                  v-bind:class="{ 'is-active': !activeCategory }"
                  @click="setActiveCategory(null)"
                >
                  <a>All Courses</a>
                </li>
                <li
                  v-for="category in categories"
                  v-bind:key="category.id"
                  @click="setActiveCategory(category)"
                  :class="{ 'is-active': category.id == activeCategory }"
                >
                  <a>{{ category.title }}</a>
                </li>
              </ul>
            </aside>
          </div>

          <div class="column is-10">
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
                  <ul class="pagination-list">
                    <li>
                      <a class="pagination-link" aria-label="Goto page 1">1</a>
                    </li>
                    <li>
                      <a
                        class="pagination-link is-current"
                        aria-label="Page 2"
                        aria-current="page"
                        >2</a
                      >
                    </li>
                    <li>
                      <a class="pagination-link" aria-label="Goto page 3">3</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
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
      categories: [],
      activeCategory: null,
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
    setActiveCategory(category) {
      this.activeCategory = category;
      this.getCourses();
    },
    getCategories() {
      axios
        .get("categories/")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getCourses() {
      let url = "courses/";
      if (this.activeCategory) {
        console.log("active category", this.activeCategory);
        url += "?category_slug=" + this.activeCategory.slug;
      }
      axios
        .get(url)
        .then((response) => {
          this.courses = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
