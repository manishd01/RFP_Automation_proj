import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // your FastAPI backend
  // or baseURL: "http://127.0.0.1:8000"
});

export default api;
