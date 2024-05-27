import React, { lazy } from "react"
import { Navigate } from "react-router-dom"

const Home = lazy(()=>import("../pages/Home"))
const Favor = lazy(()=>import("../pages/Favor"))
const Statistic = lazy(()=>import("../pages/Statistic"))
const WorldMap = lazy(()=>import("../pages/WorldMap"))
const Profile = lazy(()=>import("../pages/Profile"))
const Login = lazy(()=>import("../pages/Login"))
const Register = lazy(()=>import("../pages/Register"))


const routers = [
    {
        path:"/",
        element: <Navigate to="/home"/>,
    },
    {
        path:"/home",
        element: <Home/>,
    },
    {
        path:"/favor",
        element: <Favor/>,
    },
    {
        path: '/statistic',
        element: <Statistic/>,
    },
    {
        path: '/map',
        element: <WorldMap/>,
    },
    {
        path: '/profile',
        element: <Profile/>,
    },
    {
        path:"/login",
        element: <Login/>
    },
    {
        path:"/register",
        element: <Register/>
    },
    {
      path:"*",
      element:<Navigate to="/home"/>
    }
]

export default routers;