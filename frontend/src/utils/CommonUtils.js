import { LOGIN_TOKEN } from "../constants";

export function extractKeys(item) {
    return Object.keys(item).map((key) => ({
        title: key.charAt(0).toUpperCase() + key.slice(1),
        dataIndex: key,
        key,
    }));
}

export function parseLoginToken() {
    let tokenObj = localStorage.getItem(LOGIN_TOKEN);
    if (tokenObj) {
        return JSON.parse(tokenObj);
    }
    return null;
}
