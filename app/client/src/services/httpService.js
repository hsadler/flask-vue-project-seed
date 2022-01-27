
import axios from 'axios'

class HttpService {
  get (url) {
    return axios.get(url).then(res => {
      return res.data
    })
  }
  post (url, options) {
    return axios.post(url, options).then(res => {
      return res.data
    })
  }
}

export default new HttpService()
