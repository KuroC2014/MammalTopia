import React, { useEffect, useState, startTransition } from 'react';
import { Avatar, Breadcrumb, Dropdown, Layout, Menu, theme, Spin } from 'antd';
import { useLocation, useNavigate } from "react-router-dom";
import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
import BeforeRouterEnter from '../utils/NavigationUtils';
import { LOGIN_TOKEN } from '../constants';
const { Header, Content } = Layout;

const items = [
    {
        key: '/home',
        label: 'Home',
    },
    {
        key: '/favor',
        label: 'Favor',
    },
    {
        key: '/statistic',
        label: 'Statistic',
    },
    {
        key: '/map',
        label: 'Map',
    },
    {
        key: '/profile',
        label: 'Profile',
    }
]

function MainPage() {
    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();

    const navigateTo = useNavigate();
    const location = useLocation();

    const [loginToken, setLoginToken] = useState(null);
    const [selectedPage, setSelectedPage] = useState(location.pathname);

    useEffect(() => {
        const handleStorageChange = () => {
            const token = localStorage.getItem(LOGIN_TOKEN);
            setLoginToken(token || null);
        };

        window.addEventListener('storage', handleStorageChange);
        handleStorageChange();

        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, [localStorage.getItem(LOGIN_TOKEN)]);

    useEffect(() => {
        setSelectedPage(location.pathname);
    }, [location.pathname]);

    const handleMenuClick = (e) => {
        startTransition(() => {
            navigateTo(e.key);
        });
    };

    const handleLogout = (e) => {
        startTransition(() => {
            localStorage.removeItem(LOGIN_TOKEN);
            navigateTo('/login');
            setSelectedPage('/login');
        });
    };
    
    const changeBreadcrumbTopic = (key) => {
        return key.charAt(1).toUpperCase() + key.slice(2);
    }

    return (
        <Layout>
            <Header style={{ display: 'flex', alignItems: 'center' }}>
                <Menu
                    theme="dark"
                    mode="horizontal"
                    onClick={handleMenuClick}
                    selectedKeys={[selectedPage]}
                    items={items}
                    style={{ flex: 1, minWidth: 0 }}
                />
                {
                    loginToken && (
                    <Dropdown overlay={
                        <Menu>
                            <Menu.Item key="logout" icon={ <LogoutOutlined/> } onClick={handleLogout}>
                                Logout
                            </Menu.Item>
                        </Menu>
                    } trigger={['click']}>
                        <Avatar style={{ backgroundColor: '#FFAD33' }} icon={ <UserOutlined />} />
                    </Dropdown>)
                }
            </Header>
            <Content style={{ padding: '0 48px', marginBottom: 20}}>
                <Breadcrumb style={{ margin: '16px 0' }}>
                    <Breadcrumb.Item>MammalTopia</Breadcrumb.Item>
                    <Breadcrumb.Item>{changeBreadcrumbTopic(selectedPage)}</Breadcrumb.Item>
                </Breadcrumb>
                <div
                    style={{
                        background: colorBgContainer,
                        minHeight: 720,
                        padding: 24,
                        borderRadius: borderRadiusLG,
                        display: 'flex',
                        justifyContent: 'center',
                    }}
                >
                    <BeforeRouterEnter/>
                </div>
            </Content>
        </Layout>
    );
}

export default MainPage;