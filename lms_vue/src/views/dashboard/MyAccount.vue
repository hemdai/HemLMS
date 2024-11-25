<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">My Account</h1>
      </div>
    </div>

    <section class="section">
      <button @click="logout()" class="button is-danger">Log Out</button>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
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
