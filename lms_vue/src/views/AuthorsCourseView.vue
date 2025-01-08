<template>
  <div class="card">
    <div class="card-image">
      <figure class="image is-4by3">
        <img
          :src="$config.STATIC_PATH + authorCourse.image_path"
          alt="Placeholder image"
        />
      </figure>
    </div>
    <div class="card-content">
      <div class="media">
        <span class="icon">
          <i class="fas fa-info-circle"></i>
        </span>
        <div class="media-content">
          <p class="is-size-5">{{ authorCourse.title }}</p>
        </div>
      </div>
      <div class="content">
        <p>
          {{ authorCourse.short_description }}
        </p>
        <router-link
          :to="{
            name: 'CourseDetailView',
            params: { slug: authorCourse.slug },
          }"
          >Learn more</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AuthorsCourseView",
  props: ["authorCourse"],
};
</script>
