<template>
  <div class="signup">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Sign UP</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-4 is-offset-4">
            <form v-on:submit.prevent="submitForm">
              <div class="field">
                <label class="label">First Name</label>
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    placeholder="Adhikari"
                    v-model="first_name"
                  />
                </div>
              </div>

              <div class="field">
                <label class="label">Last Name</label>
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    placeholder="Hemanta"
                    v-model="last_name"
                  />
                </div>
              </div>

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

              <div class="field">
                <label class="label">Confirm Password</label>
                <div class="control">
                  <input
                    class="input"
                    type="password"
                    placeholder="Password"
                    v-model="confirmPassword"
                  />
                </div>
              </div>

              <div class="has-text-danger" v-if="errors.length">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
              </div>

              <br />
              <button class="button is-primary">Sign Up</button>
            </form>
            <hr />
            Already have an account?
            <RouterLink to="/login">Click here to Login</RouterLink>
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
      first_name: "",
      last_name: "",
      confirmPassword: "",
      errors: [],
    };
  },
  mounted() {
    document.title = "Sign Up - LMS";
  },
  methods: {
    submitForm() {
      this.errors = [];
      if (this.password !== this.confirmPassword) {
        this.errors.push("Passwords do not match");
      }
      if (!this.username) {
        this.errors.push("Username is required");
      }
      if (!this.password) {
        this.errors.push("Password is required");
      }
      if (!this.confirmPassword) {
        this.errors.push("Password is required");
      }

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
        };
        console.log("submitting form" + this.username + " " + this.password);
        axios
          .post("signup/", formData)
          .then((response) => {
            console.log(response);
            this.$router.push("/login");
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },
  },
};
</script>
