import axios from "axios";

console.log(process.env.REACT_APP_POST_BASE_URL);

const instance = axios.create({
  baseURL: `${process.env.REACT_APP_POST_BASE_URL}`,
  headers: {
    // 'X-Custom-Header': 'sample-MERN',
    "Content-type": "application/json"
  }
});

export default instance;