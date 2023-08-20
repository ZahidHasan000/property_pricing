import http from "./http.common";

// const create = data => http.post("/register", data);
const create = data => http.post("/predict", data);

const UserDataService = {
    create
};

export default UserDataService;