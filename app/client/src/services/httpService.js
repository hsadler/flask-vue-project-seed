
import axios from 'axios'

const API_HOST = 'http://localhost:8000'

class HttpService {
  get (url) {
    return axios.get(API_HOST + url).then(res => {
      return res.data
    })
  }
  post (url, options) {
    return axios.post(API_HOST + url, options).then(res => {
      return res.data
    })
  }
}

export default new HttpService()
