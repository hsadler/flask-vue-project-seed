<template>
  <div class="wall-messages-container">

    <h1>Wall Messages</h1>

    <section class="messages-section">
      <div
        class="wall-message"
        v-for="(message, index) in wallMessages"
        :key="index"
        @click="goToEditMessage(message)"
      >
        <p>{{ message.message }}</p>
        <p>~ {{ message.attribution }}</p>
      </div>
    </section>

    <section class="add-message-section">
      <input type="text" name="message" v-model="messageBody">
      <input type="text" name="attribution" v-model="messageAttribution">
      <button @click="addMessage()">
        add message
      </button>
    </section>

  </div>
</template>

<script>
import services from '@/services'

export default {
  name: 'WallMessages',
  props: {},
  data () {
    return {
      httpService: services.use('httpService'),
      wallMessages: [],
      messageBody: null,
      messageAttribution: null
    }
  },
  methods: {
    addMessage () {
      var url = '/api/wall-messages/add-message'
      var options = {
        message: this.messageBody,
        attribution: this.messageAttribution
      }
      this.httpService.post(url, options).then((res) => {
        this.wallMessages.push(res)
      })
    },
    goToEditMessage (message) {
      this.$router.push({
        name: 'EditWallMessage',
        params: { id: message.id }
      })
    }
  },
  created () {
    var url = '/api/wall-messages/get-all'
    this.httpService.get(url).then((res) => {
      this.wallMessages = res
    })
  }
}
</script>

<style scoped lang="scss">
  div.wall-messages-container {

    section.messages-section {
      div.wall-message {
        width: 300px;
        margin: 10px auto;
        padding: 0 20px;
        text-align: left;
        border: 1px solid gray;
        cursor: pointer;
      }
    }

    section.add-message-section {
      margin-bottom: 300px;
    }

  }
</style>
