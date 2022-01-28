<template>
  <div class="edit-wall-message-container">

    <h1>Wall Message</h1>

    <section class="wall-message-display" v-if="!editingWallMessage">

      <div class="wall-message">
        <p>{{ wallMessage.message }}</p>
        <p>~ {{ wallMessage.attribution }}</p>
      </div>

      <button @click="editingWallMessage = !editingWallMessage">edit</button>

    </section>

    <section class="wall-message-edit" v-if="editingWallMessage">

      <div class="wall-message">
        <p>
          <input
            v-model="messageBody"
            :placeholder="wallMessage.message"
          >
        </p>
        <p>
          <span>~ </span>
          <input
            v-model="messageAttribution"
            :placeholder="wallMessage.attribution"
          >
        </p>
      </div>

      <button @click="updateWallMessage()">update</button>

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
      wallMessage: {},
      editingWallMessage: false,
      messageBody: null,
      messageAttribution: null
    }
  },
  methods: {
    async updateWallMessage () {
      const url = '/api/wall-messages/update-message'
      const options = {
        message_uuid: this.wallMessage.uuid,
        message_body: this.messageBody,
        message_attribution: this.messageAttribution
      }
      this.wallMessage = await this.httpService.post(url, options)
      this.editingWallMessage = false
    }
  },
  async created () {
    const messageId = this.$route.params.uuid
    const url = `/api/wall-messages/find-one?message_uuid=${messageId}`
    this.wallMessage = await this.httpService.get(url)
  }
}
</script>

<style scoped lang="scss">
  div.edit-wall-message-container {

    div.wall-message {
      width: 300px;
      margin: 10px auto;
      padding: 0 20px;
      text-align: left;
      border: 1px solid gray;
    }

  }
</style>
