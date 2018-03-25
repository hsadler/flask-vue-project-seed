<template>
  <div class="home-container">
    <p>Home page</p>
    <button @click="getApiRandomNumber()">
      get a random number from the Flask backend
    </button>
    <p>{{ httpResponse ? httpResponse : 'nothing yet' }}</p>
  </div>
</template>

<script>
import services from '@/services'

export default {
  name: 'HomePage',
  props: {},
  data () {
    return {
      httpService: services.use('httpService'),
      httpResponse: null
    }
  },
  methods: {
    getApiRandomNumber () {
      this.httpService.get('/api/random').then((res) => {
        if (res.randomNumber) {
          this.httpResponse = res.randomNumber
        } else {
          this.httpResponse = 'failed response...'
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">
  div.home-container {
    button {
      font-size: 14px;
    }
  }
</style>
