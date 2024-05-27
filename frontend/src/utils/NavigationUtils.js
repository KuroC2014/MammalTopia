import { useEffect } from 'react';
import { useRoutes, useLocation, useNavigate } from "react-router-dom";
import { message } from 'antd';
import routers from '../routers/Routers';
import { LOGIN_TOKEN } from '../constants';

function ToLogin() {
    const navigateTo = useNavigate();
    useEffect(() => {
        navigateTo("/login");
        message.warning("You are not logged in, please visit after login!");
    }, [])
    return (
        <div>
        </div>
    );
}

function ToHome() {
    const navigateTo = useNavigate();
    useEffect(() => {
        navigateTo("/home");
        message.warning("You are already logged in!");
    }, [])
    return (
        <div>
        </div>
    );
}

function BeforeRouterEnter() {
    const outlet = useRoutes(routers);
  
    const location = useLocation();
    // localStorage.setItem(LOGIN_TOKEN, JSON.stringify({username: 'zhangsan', userId: 1, email: 'zhangsan@gmail.com'}));
    let token = localStorage.getItem(LOGIN_TOKEN);
    console.log("login token: " + token);
    if (location.pathname === "/login" && token) {
        return <ToHome />
    }
    if (location.pathname !== "/login" && location.pathname !== "/register" && !token){
        return <ToLogin />
    }
    return outlet
}

export default BeforeRouterEnter;