<template>
  <div class="card">
    <div class="card-image">
      <figure class="image is-4by3">
        <img
          :src="$config.STATIC_PATH + course.image_path"
          alt="Placeholder image"
        />
      </figure>
    </div>
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="is-size-5">{{ course.title }}</p>
        </div>
      </div>
      <div class="content">
        <p>
          {{ course.short_description }}
        </p>
        <router-link
          :to="{
            name: 'CourseDetailView',
            params: { slug: course.slug },
          }"
          >Learn more</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CourseItemView",
  props: ["course"],
};
</script>
