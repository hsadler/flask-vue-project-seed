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
      const url = '/api/wall-messages/add-message'
      const options = {
        message: this.messageBody,
        attribution: this.messageAttribution
      }
      const newMessage = this.httpService.post(url, options)
      this.wallMessages.push(newMessage)
    },
    goToEditMessage (message) {
      this.$router.push({
        name: 'EditWallMessage',
        params: { uuid: message.uuid }
      })
    }
  },
  async created () {
    const url = '/api/wall-messages/get-all'
    this.wallMessages = await this.httpService.get(url)
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
