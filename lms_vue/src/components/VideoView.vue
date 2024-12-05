<template>
  <div class="video-container">
    <iframe
      width="100%"
      height="600"
      :src="'https://www.youtube.com/embed/' + youtube_id"
      allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
      frameborder="0"
      allowfullscreen
      class="video"
      title="YouTube video player"
    ></iframe>
  </div>
</template>

<script>
export default {
  props: ["youtube_id"],
  name: "VideoView",
};
</script>
