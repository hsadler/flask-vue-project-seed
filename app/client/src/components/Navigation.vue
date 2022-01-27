<template>
  <div class="navigation-container">
    <router-link to="/">Home</router-link> |
    <router-link to="/wall-messages">Wall Messages</router-link>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  props: {}
}
</script>

<!--
<style scoped lang="scss">
  div.navigation-container {
    padding: 30px;
    a {
      font-weight: bold;
      color: #2c3e50;
      &.router-link-exact-active {
        color: #42b983;
      }
    }
  }
</style>
-->