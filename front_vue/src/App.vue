<template>
  <div>
  <nav class="navbar is-info" role="navigation" aria-label="main navigation" style="min-height: 5rem">
    <div class="navbar-brand">
      <a class="navbar-item is-size-4" href="/">HemLMS</a>
    </div>
    <div id="navbar-item" class="navbar-menu">
      <div class="navbar-start">
        <a href="/" class="navbar-item">Home</a>
        <a href="/about" class="navbar-item" >About</a>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary">
              <strong>Sign up</strong>
            </a>
            <a class="button is-light">
              Log in
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <router-view/>
  <footer class="footer">
    <p class="has-text-centered">Copyright (c) 2024, HemLMS</p>
  </footer>
  </div>
</template>

<script>
</script>

<style>
@import '../node_modules/bulma';
</style>
