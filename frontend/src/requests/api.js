import request from "./index"

export const postLogin = (params) => request.post("/login", params);
export const postRegister = (params) => request.post("/register", params);
export const postSearch = (params) => request.post("/search", params);
export const postFavor = (params) => request.post("/get_favors", params);
export const postEditFavor = (params) => request.post("/edit_favor", params);
export const findUser = (params) => request.post("/find_user", params);
export const changePassword = (params) => request.post("/change_password", params);
export const deleteAccount = (params) => request.post("/delete_account", params);
export const postStatistic = (params) => request.post("/statistic", params);