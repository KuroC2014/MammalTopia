import React, { useState, startTransition } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { useNavigate } from "react-router-dom";
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { postLogin } from '../requests/api';
import { LOGIN_TOKEN } from '../constants';

function Login() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const navigateTo = useNavigate();

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };
    
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        postLogin({
            username: username,
            password: password,
        }).then((data) => {
            console.log('here: ' + JSON.stringify(data))
            localStorage.setItem(LOGIN_TOKEN, JSON.stringify({
                username: data.username, 
                userId: data.userId, 
                email: data.email
            }));
            message.success(`User ${data.username} login successfully!`);
            navigateTo('/home');
        }).catch((err) => {
            message.error(`User failed to login!`);
        });
    };

    return (
        <Card title="Login" style={{ width: 400, height: 300 }}>
            <Form>
                <Form.Item>
                    <Input
                        prefix={<UserOutlined />}
                        placeholder="Username"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                </Form.Item>
                <Form.Item>
                    <Input.Password
                        prefix={<LockOutlined />}
                        placeholder="Password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" block onClick={handleSubmit}>
                        Login
                    </Button>
                </Form.Item>
            </Form>
            <Button type="link" onClick={e => {
                e.preventDefault();
                startTransition(() => {
                    navigateTo('/register');
                });
            }}>
                Register
            </Button>
        </Card>
    );
}

export default Login;