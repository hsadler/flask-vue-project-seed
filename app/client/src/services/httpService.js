
import axios from 'axios'

const HOST = 'http://localhost:8000'

class HttpService {
  get (url) {
    return axios.get(HOST + url).then(res => {
      return res.data
    })
  }
  post (url, options) {
    return axios.post(HOST + url, options).then(res => {
      return res.data
    })
  }
}

export default new HttpService()
