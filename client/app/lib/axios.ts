import axios from 'axios';

const baseurl = 'http://localhost:5000'

axios.defaults.baseURL = baseurl

const api = axios.create({
  baseURL: baseurl,
  timeout: 10000,
});

export default api;
