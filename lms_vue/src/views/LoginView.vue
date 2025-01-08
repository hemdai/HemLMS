<template>
  <div class="signup">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Login</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-4 is-offset-4">
            <form v-on:submit.prevent="loginForm">
              <div class="field">
                <label class="label">Email</label>
                <div class="control">
                  <input
                    class="input"
                    type="email"
                    placeholder="Email"
                    v-model="username"
                  />
                </div>
              </div>

              <div class="field">
                <label class="label">Password</label>
                <div class="control">
                  <input
                    class="input"
                    type="password"
                    placeholder="Password"
                    v-model="password"
                  />
                </div>
              </div>
              <div class="has-text-danger" v-if="errors.length">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
              </div>
              <button class="button is-primary">Log In</button>
            </form>

            <hr />
            <button @click="loginWithGoogle">Login with Google</button>
            <hr />
            Dont have an account? No problem,
            <RouterLink to="/signup">Click here to Sign Up</RouterLink>
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
      username: "",
      password: "",
      errors: [],
    };
  },
  mounted() {
    document.title = "Login | HemLMS";
  },
  methods: {
    loginForm() {
      this.errors = [];
      if (!this.username) {
        this.errors.push("Username is required");
      }
      if (!this.password) {
        this.errors.push("Password is required");
      }
      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password,
        };
        console.log("loging in" + this.username + " " + this.password);
        axios
          .post("login/", formData)
          .then((response) => {
            console.log(response);
            const token = response.data.access_token;
            this.$store.commit("setUserName", response.data.first_name);
            this.$store.commit("setToken", token);
            axios.defaults.headers.common["Authorization"] = "Bearer " + token;

            localStorage.setItem("token", token);

            this.$router.push("/dashboard/my-account");
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },
    loginWithGoogle() {
      const authUrl = "http://localhost:5000/auth/login";
      window.location.href = authUrl;
    },
  },
};
</script>
