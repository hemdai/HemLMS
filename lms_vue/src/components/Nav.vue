<template>
  <nav
    class="navbar is-info"
    role="navigation"
    aria-label="main navigation"
    style="min-height: 5rem"
  >
    <div class="navbar-brand">
      <a class="navbar-item is-size-4" href="/">HemLMS</a>
    </div>
    <div id="navbar-item" class="navbar-menu">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item">Home </router-link>
        <router-link to="/about" class="navbar-item">About </router-link>
        <router-link class="navbar-item" to="/courses">Courses</router-link>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.user.isAuthenticated">
              <router-link
                to="/dashboard/my-account"
                class="button is-primary"
                >{{ $store.state.user.first_name }}</router-link
              >
              <router-link to="/dashboard/my-account" class="button is-info">
                My Account
              </router-link>
              <router-link
                to="/dashboard/create-course"
                class="button is-primary"
              >
                Create Course</router-link
              >
            </template>
            <template v-else>
              <a href="/signup" class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a href="/login" class="button is-light"> Log in </a>
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
