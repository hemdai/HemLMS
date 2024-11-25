<template>
  <div>
  <Nav/>

  <router-view/>

  <Footer/>
  </div>
</template>

<script>
import Nav from '@/components/Nav.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    Nav,
    Footer
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.user.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    }
    else {
      axios.defaults.headers.common['Authorization'] = ''
    }

  }
}

</script>

<style>
@import '../node_modules/bulma';
</style>
